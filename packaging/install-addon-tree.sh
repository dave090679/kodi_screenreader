#!/bin/bash
# Installs the addon tree into a package root: install-addon-tree.sh <destdir>
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
dest="${1:?usage: install-addon-tree.sh <destdir>}"
addons=(service.xbmc.tts service.accessibility.setup)

for addon in "${addons[@]}"; do
    install -dm755 "$dest/usr/share/kodi/addons/$addon"
    (cd "$repo_root/$addon" && find . -type d \( -name __pycache__ \) -prune -o -type f ! -name '*.pyc' -print0) |
    while IFS= read -r -d '' file; do
        install -Dm644 "$repo_root/$addon/$file" "$dest/usr/share/kodi/addons/$addon/$file"
    done
done

install -Dm644 "$repo_root/service.xbmc.tts.keyboard.xml" \
    "$dest/etc/kodi/userdata/keymaps/service.xbmc.tts.keyboard.xml"
install -Dm644 "$repo_root/ENABLED" \
    "$dest/etc/kodi/userdata/addon_data/service.xbmc.tts/ENABLED"