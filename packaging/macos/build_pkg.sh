#!/bin/bash
# Builds the macOS installer: dist/kodi_screenreader_macos_<version>.pkg
#
# Optional: SIGN_IDENTITY="Developer ID Installer: ..." to sign the package.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo="$(cd "$here/../.." && pwd)"
addon_id="service.xbmc.tts"
pkg_id="de.dave090679.kodi-screenreader"
# First version attribute after the XML declaration is the addon version
version="$(grep -v '^<?xml' "$repo/$addon_id/addon.xml" | grep -m1 -o 'version="[^"]*"' | cut -d'"' -f2)"
# PKG_VERSION overrides it for installer-only releases, e.g. PKG_VERSION=1.0.8.1
version="${PKG_VERSION:-$version}"

build="$repo/build/macos"
dist="$repo/dist"
payload="$build/payload/Library/Application Support/Kodi Screenreader"
rm -rf "$build"
mkdir -p "$payload" "$build/resources" "$dist"

# Payload: addon, keymap and enable marker, installed into each user's Kodi profile by postinstall
rsync -a --exclude '__pycache__' --exclude '*.pyc' --exclude '.DS_Store' \
    "$repo/$addon_id/" "$payload/$addon_id/"
rsync -a --exclude '__pycache__' --exclude '*.pyc' --exclude '.DS_Store' \
    "$repo/service.accessibility.setup/" "$payload/service.accessibility.setup/"
cp "$repo/$addon_id.keyboard.xml" "$repo/ENABLED" "$payload/"
cp "$here/uninstall.sh" "$payload/"
chmod 755 "$payload/uninstall.sh"

cp -R "$here/resources/." "$build/resources/"
cp "$repo/LICENSE" "$build/resources/LICENSE.txt"
sed "s/__VERSION__/$version/" "$here/Distribution.xml" > "$build/Distribution.xml"
chmod 755 "$here/scripts/postinstall"

pkgbuild \
    --root "$build/payload" \
    --scripts "$here/scripts" \
    --identifier "$pkg_id" \
    --version "$version" \
    --install-location / \
    --ownership recommended \
    "$build/kodi-screenreader-component.pkg"

sign_args=()
[ -n "${SIGN_IDENTITY:-}" ] && sign_args=(--sign "$SIGN_IDENTITY")

out="$dist/kodi_screenreader_macos_$version.pkg"
productbuild \
    --distribution "$build/Distribution.xml" \
    --resources "$build/resources" \
    --package-path "$build" \
    "${sign_args[@]+"${sign_args[@]}"}" \
    "$out"

echo "Built $out"
