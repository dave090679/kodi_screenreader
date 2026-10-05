#!/bin/bash
# Removes the Kodi screenreader from all user profiles and the system.
# Run: sudo "/Library/Application Support/Kodi Screenreader/uninstall.sh"
# Speech settings in userdata/addon_data/service.xbmc.tts are kept.

ADDON_ID="service.xbmc.tts"

if [ "$(id -u)" -ne 0 ]; then
    echo "Bitte mit sudo ausfuehren / please run with sudo."
    exit 1
fi

if pgrep -xq Kodi; then
    echo "Kodi laeuft noch. Bitte Kodi zuerst beenden. / Please quit Kodi first."
    exit 1
fi

for home in /Users/*; do
    kodi="$home/Library/Application Support/Kodi"
    [ -d "$kodi" ] || continue
    rm -rf "$kodi/addons/$ADDON_ID"
    rm -f "$kodi/userdata/keymaps/$ADDON_ID.keyboard.xml"
    rm -f "$kodi/userdata/addon_data/$ADDON_ID/ENABLED"
    for db in "$kodi/userdata/Database"/Addons*.db; do
        [ -f "$db" ] && sqlite3 "$db" "DELETE FROM installed WHERE addonID = '$ADDON_ID';" 2>/dev/null
    done
    echo "Entfernt fuer $(basename "$home")"
done

rm -rf "/Library/Application Support/Kodi Screenreader"
pkgutil --forget de.dave090679.kodi-screenreader >/dev/null 2>&1
echo "Kodi Screenreader wurde deinstalliert."
