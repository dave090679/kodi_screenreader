# -*- coding: utf-8 -*-
import base
import os
import subprocess
import sys
from lib import util

# Text is passed as an argument instead of being formatted into the script,
# so quotes and backslashes need no escaping.
_OUTPUT_SCRIPT = [
    '-e', 'on run argv',
    '-e', 'set spokenText to item 1 of argv',
    '-e', 'tell application "VoiceOver" to output spokenText',
    '-e', 'end run',
]

# Created by macOS when "Allow VoiceOver to be controlled with AppleScript" is enabled
_APPLESCRIPT_ENABLED_FLAG = '/private/var/db/Accessibility/.VoiceOverAppleScriptEnabled'


class VoiceOverBackend(base.SimpleTTSBackendBase):
    """Sends text to a running VoiceOver.

    Requires "Allow VoiceOver to be controlled with AppleScript" in VoiceOver Utility.
    """
    provider = 'voiceover'
    displayName = 'VoiceOver'
    canStreamWav = False

    def init(self):
        self.setMode(base.SimpleTTSBackendBase.ENGINESPEAK)

    def _output(self, text):
        try:
            subprocess.call(['osascript'] + _OUTPUT_SCRIPT + ['--', text])
        except Exception:
            util.ERROR('VoiceOver: osascript failed', hide_tb=True)

    def runCommandAndSpeak(self, text):
        self._output(text)

    def stop(self):
        self._output('')

    @staticmethod
    def available():
        if sys.platform != 'darwin' or util.isATV2(): return False
        if not os.path.exists(_APPLESCRIPT_ENABLED_FLAG): return False
        try:
            return subprocess.call(['pgrep', '-xq', 'VoiceOver']) == 0
        except Exception:
            return False
