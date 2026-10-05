# -*- coding: utf-8 -*-
import xbmc

from resources.lib import setup

if __name__ == '__main__':
    # Give Kodi a moment to finish loading the home screen before switching skins
    if not xbmc.Monitor().waitForAbort(3):
        setup.run()
