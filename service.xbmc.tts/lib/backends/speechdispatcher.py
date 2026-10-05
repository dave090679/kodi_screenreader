# -*- coding: utf-8 -*-
import locale
import re
import subprocess

from base import ThreadedTTSBackend
from lib import util


class SpeechDispatcherTTSBackend(ThreadedTTSBackend):
    """Speech Dispatcher backend using the spd-say CLI available on Linux."""

    provider = 'Speech-Dispatcher'
    displayName = 'Speech Dispatcher'
    volumeConstraints = (-100,0,100,True)
    volumeExternalEndpoints = (0,200)
    volumeStep = 5
    volumeSuffix = '%'
    settings = {
                    'module':None,
                    'voice':None,
                    'speed':0,
                    'pitch':0,
                    'volume':100
    }
    applicationName = 'XBMC'
    connectionName = 'XBMC'

    def init(self):
        self.updateMessage = None
        self.update()

    def _baseArgs(self):
        args = ['spd-say', '-N', self.applicationName, '-n', self.connectionName]
        module = self.setting('module')
        if module:
            args.extend(('-o', module))
        voice = self.setting('voice')
        if voice:
            args.extend(('-y', voice))
        language = locale.getdefaultlocale()[0]
        if language:
            args.extend(('-l', language.split('_', 1)[0]))
        args.extend((
            '-r', str(self.setting('speed')),
            '-p', str(self.setting('pitch')),
            '-i', str(self.setting('volume') - 100),
        ))
        return args

    def threadedSay(self,text,interrupt=False):
        try:
            subprocess.run(
                self._baseArgs() + ['-w', text],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                text=True,
            )
        except (OSError, subprocess.CalledProcessError):
            self.flagAsDead('Speech Dispatcher unavailable')
            util.ERROR('SpeechDispatcherTTSBackend.threadedSay()',hide_tb=True)

    def stop(self):
        try:
            subprocess.run(
                ['spd-say', '-N', self.applicationName, '-n', self.connectionName, '-C'],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                text=True,
            )
        except OSError:
            util.ERROR('SpeechDispatcherTTSBackend.stop()',hide_tb=True)

    def volumeUp(self):
        # Returning the spoken confirmation synchronously can deadlock this backend.
        self.updateMessage = ThreadedTTSBackend.volumeUp(self)

    def volumeDown(self):
        # Returning the spoken confirmation synchronously can deadlock this backend.
        self.updateMessage = ThreadedTTSBackend.volumeDown(self)

    def getUpdateMessage(self):
        msg = self.updateMessage
        self.updateMessage = None
        return msg

    def update(self):
        msg = self.getUpdateMessage()
        if msg: self.say(msg,interrupt=True)

    @classmethod
    def settingList(cls,setting,*args):
        if setting == 'module':
            out = subprocess.check_output(['spd-say', '-O'], text=True, errors='ignore')
            return [(m,m) for m in out.splitlines() if m and m.strip() != 'OUTPUT MODULES']
        elif setting == 'voice':
            command = ['spd-say']
            module = cls.setting('module')
            if module:
                command.extend(('-o', module))
            command.append('-L')
            out = subprocess.check_output(command, text=True, errors='ignore')
            voices = []
            for line in out.splitlines():
                line = line.strip()
                if not line or line.startswith('NAME'):
                    continue
                parts = re.split(r'\s{2,}', line, maxsplit=2)
                if parts:
                    voices.append((parts[0], parts[0]))
            return voices

    @staticmethod
    def available():
        return util.commandIsAvailable('spd-say')
