#!/bin/bash
# Automatisches Setup-Skript für Linux Build-Dateien
# Dieses Skript erstellt alle notwendigen Dateien für Debian und Arch Linux Builds

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "📦 Kodi Screenreader - Linux Build Files Setup"
echo "================================================"
echo ""

# Farben für Output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'  # No Color

# 1. Debian-Verzeichnis erstellen
echo -e "${BLUE}1. Erstelle Debian-Struktur...${NC}"
mkdir -p "$REPO_ROOT/debian"

# 2. Debian/control
echo -e "${BLUE}2. Schreibe debian/control...${NC}"
cat > "$REPO_ROOT/debian/control" << 'EOF'
Source: kodi-screenreader
Section: media
Priority: optional
Maintainer: Dave <dave090679@users.noreply.github.com>
Build-Depends: debhelper-compat (= 13)
Standards-Version: 4.6.0
Homepage: https://github.com/dave090679/kodi_screenreader
Vcs-Git: https://github.com/dave090679/kodi_screenreader.git
Vcs-Browser: https://github.com/dave090679/kodi_screenreader

Package: kodi-screenreader
Architecture: all
Depends: kodi (>= 18), python3
Description: Screenreader addon for Kodi media center
 kodi-screenreader provides audio output and keyboard control for the Kodi
 media center, making it accessible for visually impaired users. It includes
 Text-to-Speech (TTS) support and integration with assistive technologies
 like NVDA on Windows.
 .
 Features:
  - Text-to-Speech (TTS) audio output
  - Keyboard shortcuts for navigation and control
  - NVDA (Non-Visual Desktop Access) integration support
  - Kodi addon repository integration
EOF

# 3. Debian/rules
echo -e "${BLUE}3. Schreibe debian/rules...${NC}"
cat > "$REPO_ROOT/debian/rules" << 'EOF'
#!/usr/bin/make -f
%:
	dh $@

override_dh_auto_build:
	# No build required for Python addon

override_dh_auto_install:
	# Install addon files to Kodi addons directory
	mkdir -p debian/kodi-screenreader/usr/share/kodi/addons/service.xbmc.tts
	mkdir -p debian/kodi-screenreader/usr/share/kodi/addons/ruuk.addon.repository
	mkdir -p debian/kodi-screenreader/usr/share/kodi/addons/script.module.nvdacontrollerclient
	
	# Copy service.xbmc.tts files
	cp -r service.xbmc.tts/* debian/kodi-screenreader/usr/share/kodi/addons/service.xbmc.tts/ 2>/dev/null || true
	
	# Copy repository addon
	cp -r ruuk.addon.repository/* debian/kodi-screenreader/usr/share/kodi/addons/ruuk.addon.repository/
	
	# Copy NVDA controller client
	cp -r script.module.nvdacontrollerclient/* debian/kodi-screenreader/usr/share/kodi/addons/script.module.nvdacontrollerclient/
	
	# Copy keyboard mappings
	mkdir -p debian/kodi-screenreader/etc/kodi/userdata/keymaps
	cp service.xbmc.tts.keyboard.xml debian/kodi-screenreader/etc/kodi/userdata/keymaps/ 2>/dev/null || true
	
	# Copy ENABLED flag to addon_data directory
	mkdir -p debian/kodi-screenreader/etc/kodi/userdata/addon_data/service.xbmc.tts
	cp ENABLED debian/kodi-screenreader/etc/kodi/userdata/addon_data/service.xbmc.tts/ 2>/dev/null || true

override_dh_auto_test:
	# No tests required for this addon
EOF

chmod +x "$REPO_ROOT/debian/rules"

# 4. Debian/changelog
echo -e "${BLUE}4. Schreibe debian/changelog...${NC}"
cat > "$REPO_ROOT/debian/changelog" << 'EOF'
kodi-screenreader (1.0.0-1) unstable; urgency=medium

  * Initial Debian release
  * Package Kodi screenreader addon for Linux distributions
  * Includes TTS support and NVDA integration
  * Provides accessible keyboard navigation for Kodi

 -- Dave <dave090679@users.noreply.github.com>  Mon, 21 Jan 2026 12:00:00 +0000
EOF

# 5. Debian/compat
echo -e "${BLUE}5. Schreibe debian/compat...${NC}"
echo "13" > "$REPO_ROOT/debian/compat"

# 6. Debian/copyright
echo -e "${BLUE}6. Schreibe debian/copyright...${NC}"
cat > "$REPO_ROOT/debian/copyright" << 'EOF'
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: kodi-screenreader
Upstream-Contact: Dave <dave090679@users.noreply.github.com>
Source: https://github.com/dave090679/kodi_screenreader

Files: *
Copyright: 2014-2026 Dave and Contributors
License: GPL-2+

Files: script.module.nvdacontrollerclient/*
Copyright: NVDA Access Contributors
License: LGPL-2.1+

License: GPL-2+
 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.
 .
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 .
 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
 .
 On Debian systems, the complete text of the GPL version 2 can be
 found in `/usr/share/common-licenses/GPL-2'.

License: LGPL-2.1+
 This library is free software; you can redistribute it and/or
 modify it under the terms of the GNU Lesser General Public
 License as published by the Free Software Foundation; either
 version 2.1 of the License, or (at your option) any later version.
 .
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 Lesser General Public License for more details.
 .
 You should have received a copy of the GNU Lesser General Public
 License along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1335 USA
EOF

# 7. Debian/postinst
echo -e "${BLUE}7. Schreibe debian/postinst...${NC}"
cat > "$REPO_ROOT/debian/postinst" << 'EOF'
#!/bin/bash
set -e

# Link Kodi config directory to standard location
if [ ! -L "/etc/kodi/userdata/keymaps" ]; then
    mkdir -p /etc/kodi/userdata
fi

# Set proper permissions for Kodi
if command -v kodi >/dev/null 2>&1; then
    chown -R kodi:kodi /usr/share/kodi/addons/service.xbmc.tts 2>/dev/null || true
    chown -R kodi:kodi /usr/share/kodi/addons/script.module.nvdacontrollerclient 2>/dev/null || true
fi

exit 0
EOF

chmod +x "$REPO_ROOT/debian/postinst"

# 8. Debian/postrm
echo -e "${BLUE}8. Schreibe debian/postrm...${NC}"
cat > "$REPO_ROOT/debian/postrm" << 'EOF'
#!/bin/bash
set -e

# Cleanup on removal
if [ "$1" = "remove" ] || [ "$1" = "purge" ]; then
    # Remove configuration files if requested
    if [ "$1" = "purge" ]; then
        rm -rf /etc/kodi/userdata/addon_data/service.xbmc.tts 2>/dev/null || true
    fi
fi

exit 0
EOF

chmod +x "$REPO_ROOT/debian/postrm"

# 9. PKGBUILD für Arch Linux
echo -e "${BLUE}9. Schreibe PKGBUILD...${NC}"
cat > "$REPO_ROOT/PKGBUILD" << 'EOF'
# Maintainer: Dave <dave090679@users.noreply.github.com>
pkgname=kodi-screenreader
pkgver=1.0.0
pkgrel=1
pkgdesc="Screenreader addon for Kodi media center with TTS and NVDA support"
arch=('any')
url="https://github.com/dave090679/kodi_screenreader"
license=('GPL2' 'LGPL2.1')
depends=('kodi' 'python')
makedepends=('git')
source=("git+https://github.com/dave090679/kodi_screenreader.git")
md5sums=('SKIP')

pkgver() {
    cd "$pkgname"
    git describe --long --tags 2>/dev/null | sed 's/v//g;s/-/.r/;s/-/./' || echo "1.0.0"
}

prepare() {
    cd "$pkgname"
    # No preparation needed
}

build() {
    # No build required for Python addon
    cd "$pkgname"
}

package() {
    cd "$pkgname"
    
    # Install addon directories to system Kodi addons path
    install -dm755 "${pkgdir}/usr/share/kodi/addons"
    
    # Install service.xbmc.tts
    if [ -d "service.xbmc.tts" ]; then
        cp -r service.xbmc.tts "${pkgdir}/usr/share/kodi/addons/"
    fi
    
    # Install repository addon
    if [ -d "ruuk.addon.repository" ]; then
        cp -r ruuk.addon.repository "${pkgdir}/usr/share/kodi/addons/"
    fi
    
    # Install NVDA controller client module
    if [ -d "script.module.nvdacontrollerclient" ]; then
        cp -r script.module.nvdacontrollerclient "${pkgdir}/usr/share/kodi/addons/"
    fi
    
    # Install keyboard mappings
    install -dm755 "${pkgdir}/etc/kodi/userdata/keymaps"
    if [ -f "service.xbmc.tts.keyboard.xml" ]; then
        install -Dm644 service.xbmc.tts.keyboard.xml \
            "${pkgdir}/etc/kodi/userdata/keymaps/service.xbmc.tts.keyboard.xml"
    fi
    
    # Install addon activation flag
    install -dm755 "${pkgdir}/etc/kodi/userdata/addon_data/service.xbmc.tts"
    if [ -f "ENABLED" ]; then
        install -Dm644 ENABLED \
            "${pkgdir}/etc/kodi/userdata/addon_data/service.xbmc.tts/ENABLED"
    fi
    
    # Install license files
    install -Dm644 LICENSE "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
    
    if [ -f "script.module.nvdacontrollerclient/LICENSE.txt" ]; then
        install -Dm644 script.module.nvdacontrollerclient/LICENSE.txt \
            "${pkgdir}/usr/share/licenses/${pkgname}/NVDA-LICENSE"
    fi
}
EOF

echo ""
echo -e "${GREEN}✓ Alle Dateien wurden erfolgreich erstellt!${NC}"
echo ""
echo "📁 Debian-Dateien:"
ls -la "$REPO_ROOT/debian/"
echo ""
echo "📋 Arch Linux:"
ls -la "$REPO_ROOT/PKGBUILD"
echo ""
echo -e "${GREEN}Build-Verzeichnisstruktur:${NC}"
echo "kodi_screenreader/"
echo "├── debian/"
echo "│   ├── control"
echo "│   ├── rules"
echo "│   ├── changelog"
echo "│   ├── compat"
echo "│   ├── copyright"
echo "│   ├── postinst"
echo "│   └── postrm"
echo "├── PKGBUILD"
echo "├── service.xbmc.tts/"
echo "├── script.module.nvdacontrollerclient/"
echo "├── ruuk.addon.repository/"
echo "├── service.xbmc.tts.keyboard.xml"
echo "├── ENABLED"
echo "└── LICENSE"
echo ""
echo "🚀 Nächste Schritte:"
echo ""
echo "Für Debian/Ubuntu:"
echo "  1. cd $REPO_ROOT"
echo "  2. sudo apt-get install build-essential debhelper"
echo "  3. dpkg-buildpackage -us -uc"
echo "  4. sudo dpkg -i ../kodi-screenreader_1.0.0-1_all.deb"
echo ""
echo "Für Arch Linux:"
echo "  1. cd $REPO_ROOT"
echo "  2. sudo pacman -S base-devel"
echo "  3. makepkg -si"
echo ""
