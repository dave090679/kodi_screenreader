# -*- coding: utf-8 -*-
import xbmcgui

from resources.lib import setup

if __name__ == '__main__':
    # Started by hand from the add-on list: run every step again
    if xbmcgui.Dialog().yesno(setup.T(30000), setup.T(30105)):
        if not setup.run(force=True):
            xbmcgui.Dialog().ok(setup.T(30000), setup.T(30106))
