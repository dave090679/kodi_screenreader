# -*- coding: utf-8 -*-
import os
import re
import subprocess
import sys

from lib import util
from base import ThreadedTTSBackend

# Matches lines of `say -v '?'`, e.g.
#   "Anna                de_DE    # Hallo! Ich heiße Anna."              (older macOS)
#   "Anna (Deutsch (Deutschland)) de_DE    # Hallo! Ich heiße Anna."     (macOS 14+)
_VOICE_LINE_RE = re.compile(r'^(?P<name>.+?)\s+(?P<locale>[a-z]{2,3}(?:[_-][A-Za-z0-9]+)*)\s+#')
_LANG_SUFFIX_RE = re.compile(r'\s*\((?:[^()]|\([^()]*\))*\)$')
# The service uses '...' as a pause marker; `say` reads it as "dot" at the start of an utterance
_PAUSE_RE = re.compile(r'\s*\.{2,}\s*')
_PAUSE = ' [[slnc 250]] '


class OSXSayTTSBackend(ThreadedTTSBackend):
    """Speaks via the macOS `say` command.

    Uses one subprocess per utterance so speech can be interrupted
    immediately by terminating the process.
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
        ThreadedTTSBackend.__init__(self)

    def init(self):
        self.update()

    def update(self):
        self.voice = self.setting('voice')
        self.rate = self.setting('speed')
        self.volume = self.setting('volume')

    def _args(self, text, out_file=None):
        args = ['say']
        if self.voice:
            args += ['-v', self.voice]
        if self.rate:
            args += ['-r', str(self.rate)]
        if out_file:
            args += ['-o', out_file, '--file-format=WAVE', '--data-format=LEI16@22050']
        text = _PAUSE_RE.sub(_PAUSE, text).strip()
        if text.startswith('[[slnc'):
            text = text[len(_PAUSE.strip()):].strip()
        if self.volume is not None and self.volume < 100:
            # `say` has no volume option, but honours the embedded speech command [[volm]]
            text = '[[volm {0:.2f}]] {1}'.format(max(self.volume, 0) / 100.0, text)
        # '--' keeps text starting with '-' from being parsed as an option
        return args + ['--', text]

    def threadedSay(self, text):
        if not text: return
        self.process = subprocess.Popen(self._args(text))
        while self.process.poll() is None and self.active:
            util.sleep(10)

    def getWavStream(self, text):
        wav_path = os.path.join(util.getTmpfs(), 'speech.wav')
        subprocess.call(self._args(text, wav_path))
        return open(wav_path, 'rb')

    def isSpeaking(self):
        return (self.process and self.process.poll() is None) or ThreadedTTSBackend.isSpeaking(self)

    def stop(self):
        if not self.process: return
        try:
            self.process.terminate()
        except Exception:
            pass

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
