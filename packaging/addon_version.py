#!/usr/bin/env python3
"""Prints the version of the service.xbmc.tts addon."""
import re
import sys
from pathlib import Path

addon_xml = Path(__file__).resolve().parent.parent / "service.xbmc.tts" / "addon.xml"
match = re.search(r'<addon\b[^>]*?\sversion="([^"]+)"', addon_xml.read_text(encoding="utf-8"), re.S)
if not match:
    sys.exit("Addon-Version nicht gefunden in %s" % addon_xml)
print(match.group(1))