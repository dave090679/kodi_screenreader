# -*- coding: utf-8 -*-
import ctypes
import ctypes.util
import os
import re
import subprocess
import sys

from lib import util
from .base import ThreadedTTSBackend

# Matches lines of `say -v '?'`, e.g.
#   "Anna                de_DE    # Hallo! Ich heiße Anna."              (older macOS)
#   "Anna (Deutsch (Deutschland)) de_DE    # Hallo! Ich heiße Anna."     (macOS 14+)
_VOICE_LINE_RE = re.compile(r'^(?P<name>.+?)\s+(?P<locale>[a-z]{2,3}(?:[_-][A-Za-z0-9]+)*)\s+#')
_LANG_SUFFIX_RE = re.compile(r'\s*\((?:[^()]|\([^()]*\))*\)$')
# The service uses '...' as a pause marker; `say` reads it as "dot" at the start of an utterance
_PAUSE_RE = re.compile(r'\s*\.{2,}\s*')
_PAUSE = ' [[slnc 250]] '


class _Synthesizer(object):
    """NSSpeechSynthesizer via the Objective-C runtime.

    The voice stays loaded, so speech starts at once. Every `say` process has
    to load it again first, which delays each utterance by almost a second.
    """

    def __init__(self, voice=None):
        objc = ctypes.cdll.LoadLibrary(ctypes.util.find_library('objc'))
        ctypes.cdll.LoadLibrary('/System/Library/Frameworks/AppKit.framework/AppKit')
        objc.objc_getClass.restype = ctypes.c_void_p
        objc.objc_getClass.argtypes = [ctypes.c_char_p]
        objc.sel_registerName.restype = ctypes.c_void_p
        objc.sel_registerName.argtypes = [ctypes.c_char_p]
        objc.objc_autoreleasePoolPush.restype = ctypes.c_void_p
        objc.objc_autoreleasePoolPop.argtypes = [ctypes.c_void_p]
        self._objc = objc
        self._send = {}

        synth_class = objc.objc_getClass(b'NSSpeechSynthesizer')
        self._string_class = objc.objc_getClass(b'NSString')
        if not synth_class or not self._string_class:
            raise RuntimeError('NSSpeechSynthesizer not available')
        synth = self._call(synth_class, 'alloc')
        self.synth = self._call(synth, 'init')
        if not self.synth:
            raise RuntimeError('NSSpeechSynthesizer could not be created')
        if voice:
            self.setVoice(voice)

    def _call(self, obj, selector, *args, restype=ctypes.c_void_p, argtypes=()):
        key = (restype, tuple(argtypes))
        func = self._send.get(key)
        if not func:
            func = ctypes.CFUNCTYPE(restype, ctypes.c_void_p, ctypes.c_void_p, *argtypes)(('objc_msgSend', self._objc))
            self._send[key] = func
        return func(obj, self._objc.sel_registerName(selector.encode('ascii')), *args)

    def _string(self, text):
        string = self._call(self._string_class, 'alloc')
        return self._call(string, 'initWithUTF8String:', text.encode('utf-8'), argtypes=(ctypes.c_char_p,))

    def _release(self, obj):
        if obj: self._call(obj, 'release', restype=None)

    def speak(self, text):
        string = self._string(text)
        try:
            return self._call(self.synth, 'startSpeakingString:', string, restype=ctypes.c_bool, argtypes=(ctypes.c_void_p,))
        finally:
            self._release(string)

    def isSpeaking(self):
        return self._call(self.synth, 'isSpeaking', restype=ctypes.c_bool)

    def stop(self):
        self._call(self.synth, 'stopSpeaking', restype=None)

    def setRate(self, rate):
        self._call(self.synth, 'setRate:', rate, restype=None, argtypes=(ctypes.c_float,))

    def setVolume(self, volume):
        self._call(self.synth, 'setVolume:', volume, restype=None, argtypes=(ctypes.c_float,))

    def setVoice(self, name):
        """Selects a voice by the name `say -v` uses; None selects the system voice."""
        identifier = self._voiceIdentifier(name) if name else None
        if name and not identifier:
            util.LOG('OSXSay: voice not found: {0}'.format(name))
        self._call(self.synth, 'setVoice:', identifier, restype=ctypes.c_bool, argtypes=(ctypes.c_void_p,))

    def _voiceIdentifier(self, name):
        pool = self._objc.objc_autoreleasePoolPush()
        try:
            key = self._string('VoiceName')
            try:
                voices = self._call(self._objc.objc_getClass(b'NSSpeechSynthesizer'), 'availableVoices')
                for i in range(self._call(voices, 'count', restype=ctypes.c_ulong)):
                    identifier = self._call(voices, 'objectAtIndex:', i, argtypes=(ctypes.c_ulong,))
                    attributes = self._call(self._objc.objc_getClass(b'NSSpeechSynthesizer'), 'attributesForVoice:', identifier, argtypes=(ctypes.c_void_p,))
                    voice_name = self._call(attributes, 'objectForKey:', key, argtypes=(ctypes.c_void_p,)) if attributes else None
                    if not voice_name: continue
                    # VoiceName carries the language, e.g. "Anna (German (Germany))"
                    voice_name = self._call(voice_name, 'UTF8String', restype=ctypes.c_char_p).decode('utf-8')
                    if _LANG_SUFFIX_RE.sub('', voice_name).strip() == name:
                        return self._call(identifier, 'retain')
            finally:
                self._release(key)
        finally:
            self._objc.objc_autoreleasePoolPop(pool)
        return None

    def close(self):
        self.stop()
        self._release(self.synth)
        self.synth = None


class OSXSayTTSBackend(ThreadedTTSBackend):
    """Speaks with the macOS system voices.

    Uses NSSpeechSynthesizer in-process; falls back to one `say` subprocess
    per utterance if the Objective-C runtime cannot be used.
    """
    provider = 'OSXSay'
    displayName = 'macOS Say'
    canStreamWav = True
    speedConstraints = (80, 200, 450, True)
    volumeConstraints = (0, 100, 100, True)
    volumeExternalEndpoints = (0, 100)
    volumeStep = 5
    volumeSuffix = '%'
    settings = {
        'voice': '',
        'speed': 200,
        'volume': 100,
    }

    def __init__(self):
        self.process = None
        self.synth = None
        ThreadedTTSBackend.__init__(self)

    def init(self):
        try:
            self.synth = _Synthesizer()
        except Exception:
            util.ERROR('OSXSay: NSSpeechSynthesizer failed, using the say command', hide_tb=True)
            self.synth = None
        self.update()

    def update(self):
        self.voice = self.setting('voice')
        self.rate = self.setting('speed')
        self.volume = self.setting('volume')
        if self.synth:
            self.synth.setVoice(self.voice)
            if self.rate: self.synth.setRate(self.rate)
            if self.volume is not None: self.synth.setVolume(max(self.volume, 0) / 100.0)

    def _text(self, text):
        text = _PAUSE_RE.sub(_PAUSE, text).strip()
        if text.startswith('[[slnc'):
            text = text[len(_PAUSE.strip()):].strip()
        return text

    def _args(self, text, out_file=None):
        args = ['say']
        if self.voice:
            args += ['-v', self.voice]
        if self.rate:
            args += ['-r', str(self.rate)]
        if out_file:
            args += ['-o', out_file, '--file-format=WAVE', '--data-format=LEI16@22050']
        text = self._text(text)
        if self.volume is not None and self.volume < 100:
            # `say` has no volume option, but honours the embedded speech command [[volm]]
            text = '[[volm {0:.2f}]] {1}'.format(max(self.volume, 0) / 100.0, text)
        # '--' keeps text starting with '-' from being parsed as an option
        return args + ['--', text]

    def threadedSay(self, text):
        if not text: return
        if self.synth:
            self.synth.speak(self._text(text))
            while self.active and self.synth and self.synth.isSpeaking():
                util.sleep(10)
            return
        self.process = subprocess.Popen(self._args(text))
        while self.process.poll() is None and self.active:
            util.sleep(10)

    def getWavStream(self, text):
        wav_path = os.path.join(util.getTmpfs(), 'speech.wav')
        subprocess.call(self._args(text, wav_path))
        return open(wav_path, 'rb')

    def isSpeaking(self):
        if self.synth and self.synth.isSpeaking(): return True
        return (self.process and self.process.poll() is None) or ThreadedTTSBackend.isSpeaking(self)

    def stop(self):
        if self.synth: self.synth.stop()
        if not self.process: return
        try:
            self.process.terminate()
        except Exception:
            pass

    def close(self):
        if not self.synth: return
        synth, self.synth = self.synth, None
        synth.close()

    @classmethod
    def settingList(cls, setting, *args):
        if setting == 'voice':
            return cls.voiceList()
        return None

    @staticmethod
    def voiceList():
        try:
            output = subprocess.check_output(['say', '-v', '?']).decode('utf-8', 'replace')
        except Exception:
            util.ERROR('OSXSay: could not list voices', hide_tb=True)
            return None
        voices = []
        seen = set()
        for line in output.splitlines():
            match = _VOICE_LINE_RE.match(line)
            if not match: continue
            label = match.group('name').strip()
            # Entries without a usable identifier are listed as "(null) - Name"
            if label.startswith('(null)'): continue
            name = _LANG_SUFFIX_RE.sub('', label).strip()
            if not name or name in seen: continue
            seen.add(name)
            voices.append((name, '{0} ({1})'.format(name, match.group('locale'))))
        return voices

    @staticmethod
    def available():
        return sys.platform == 'darwin' and not util.isATV2()
