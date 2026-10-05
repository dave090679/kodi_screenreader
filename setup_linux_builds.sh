#!/bin/bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERSION="$(python3 "$REPO_ROOT/packaging/addon_version.py")"

required_files=(
  "$REPO_ROOT/kodi_screenreader.spec"
  "$REPO_ROOT/PKGBUILD"
  "$REPO_ROOT/debian/rules"
  "$REPO_ROOT/debian/postinst"
  "$REPO_ROOT/debian/changelog"
  "$REPO_ROOT/packaging/addon_version.py"
  "$REPO_ROOT/packaging/install-addon-tree.sh"
)

for file in "${required_files[@]}"; do
  [[ -f "$file" ]] || {
    echo "Fehlende Packaging-Datei: $file" >&2
    exit 1
  }
done

chmod +x \
  "$REPO_ROOT/debian/postinst" \
  "$REPO_ROOT/debian/postrm" \
  "$REPO_ROOT/packaging/install-addon-tree.sh"

echo "Packaging-Dateien sind vorhanden und auf Addon-Version $VERSION ausgerichtet."
echo "Die Build-Skripte paketieren jetzt den aktuellen Checkout ueber packaging/install-addon-tree.sh"
echo "und schliessen generierte __pycache__-/pyc-Artefakte aus."
