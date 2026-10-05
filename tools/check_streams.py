#!/usr/bin/env python3
"""Checks every stream in the channel list of the accessibility setup add-on.

Usage: python3 tools/check_streams.py [path/to/list.m3u]
Exits with status 1 if a stream is unreachable. Most streams are geo-blocked
outside Germany, so run it from a German connection.
"""
import os
import sys
import urllib.request

DEFAULT = os.path.join(os.path.dirname(__file__), '..', 'service.accessibility.setup',
                       'resources', 'channels', 'oeffentlich-rechtlich.m3u')


def check(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'Kodi', 'Range': 'bytes=0-2047'})
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            head = response.read(2048)
            content_type = response.headers.get('Content-Type', '')
    except Exception as e:
        return str(e)
    if head.startswith(b'#EXTM3U') or content_type.startswith('audio/'):
        return None
    return 'unexpected content ({0})'.format(content_type or 'unknown')


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
    name = None
    failed = 0
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#EXTINF'):
                name = line.rsplit(',', 1)[-1]
            elif line and not line.startswith('#'):
                error = check(line)
                print('{0:4} {1}{2}'.format('OK' if not error else 'FAIL', name, ': ' + error if error else ''))
                failed += bool(error)
    print('{0} unreachable'.format(failed))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
