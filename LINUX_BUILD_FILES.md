# Kodi Screenreader - Linux Build Files

Dieses Dokument enthält die kompletten Build-Dateien für Debian und Arch Linux.

## 1. Debian Build Files

### Schritt 1: Verzeichnisstruktur erstellen

```bash
mkdir -p debian
```

### Schritt 2: Dateien erstellen

#### debian/control
```
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
```

#### debian/rules
```
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
```

#### debian/changelog
```
kodi-screenreader (1.0.0-1) unstable; urgency=medium

  * Initial Debian release
  * Package Kodi screenreader addon for Linux distributions
  * Includes TTS support and NVDA integration
  * Provides accessible keyboard navigation for Kodi

 -- Dave <dave090679@users.noreply.github.com>  Mon, 21 Jan 2026 12:00:00 +0000
```

#### debian/compat
```
13
```

#### debian/copyright
```
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
```

#### debian/postinst
```
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
```

#### debian/postrm
```
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
```

### Schritt 3: Build-Befehle

```bash
# Abhängigkeiten installieren
sudo apt-get install build-essential debhelper dh-make git

# Im Repository-Verzeichnis:
dpkg-buildpackage -us -uc

# Ergebnis in ../kodi-screenreader_1.0.0-1_all.deb

# Installation:
sudo dpkg -i ../kodi-screenreader_1.0.0-1_all.deb
```

---

## 2. Arch Linux Build File

### Datei: PKGBUILD

```
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
```

### Build-Befehle

```bash
# Abhängigkeiten installieren
sudo pacman -S base-devel git

# PKGBUILD in Repository-Verzeichnis kopieren
cp PKGBUILD .

# Package bauen und installieren
makepkg -si

# oder nur bauen ohne Installation
makepkg
```

---

## 3. Installation & Verwendung

### Nach Debian-Installation

```bash
# Kodi neustarten
sudo systemctl restart kodi

# oder manuell
kodi &
```

### Nach Arch-Installation

```bash
# Kodi starten
kodi &

# oder systemd Service nutzen falls installiert
sudo systemctl start kodi
```

### Screenreader aktivieren

1. Kodi starten
2. **F12** drücken zum Aktivieren des Screenreaders
3. Weitere Tastenkombinationen siehe README.md

---

## 4. Dateistruktur nach Installation

```
/usr/share/kodi/addons/
├── service.xbmc.tts/
│   └── (Screenreader-Service-Dateien)
├── ruuk.addon.repository/
│   └── addon.xml
└── script.module.nvdacontrollerclient/
    └── (NVDA integration files)

/etc/kodi/userdata/keymaps/
└── service.xbmc.tts.keyboard.xml

/etc/kodi/userdata/addon_data/service.xbmc.tts/
└── ENABLED

/usr/share/licenses/kodi-screenreader/
├── LICENSE
└── NVDA-LICENSE (Arch only)
```

---

## 5. Troubleshooting

### Problem: Package-Abhängigkeiten nicht gefunden

**Debian/Ubuntu:**
```bash
sudo apt-get update
sudo apt-get install kodi python3
```

**Arch:**
```bash
sudo pacman -Syu kodi python
```

### Problem: Keine Berechtigung für /etc/kodi/

Die postinst-Skripte setzen Berechtigungen automatisch. Falls nötig manuell:

```bash
sudo chown -R kodi:kodi /etc/kodi/userdata/keymaps/
sudo chmod -R 755 /etc/kodi/userdata/
```

### Problem: ENABLED-Datei fehlend

Falls die Datei `ENABLED` im Root-Verzeichnis fehlt, erstellen Sie sie:

```bash
touch ENABLED
```

---

## 6. Weitere Ressourcen

- [Debian Packaging Guide](https://www.debian.org/doc/manuals/debmake-doc/)
- [Arch Linux PKGBUILD Guide](https://wiki.archlinux.org/title/PKGBUILD)
- [Kodi Add-ons Documentation](https://kodi.wiki/view/Add-on_development)
- [Kodi Screenreader Repository](https://github.com/dave090679/kodi_screenreader)
