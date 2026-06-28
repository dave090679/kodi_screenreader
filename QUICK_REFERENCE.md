# 🎯 Kodi Screenreader - Build Files Quick Reference

## 📂 Dateien zur Erstellung

### Debian-Dateien (7 Dateien)

```bash
debian/
├── control           # Paketmetadaten
├── rules            # Build-Skript (Debhelper)
├── changelog        # Versionsverlauf
├── compat           # Kompatibilitätslevel
├── copyright        # Lizenzen
├── postinst         # Nach Installation
└── postrm           # Nach Deinstallation
```

### Arch Linux-Datei (1 Datei)

```bash
├── PKGBUILD         # Arch Build-Skript
```

---

## ⚡ Schnell-Anleitung

### Debian/Ubuntu in 4 Schritten

```bash
# 1️⃣  Abhängigkeiten
sudo apt-get install build-essential debhelper

# 2️⃣  Bauen
dpkg-buildpackage -us -uc

# 3️⃣  Installieren
sudo dpkg -i ../kodi-screenreader_1.0.0-1_all.deb

# 4️⃣  Starten
kodi &
```

### Arch Linux in 4 Schritten

```bash
# 1️⃣  Abhängigkeiten
sudo pacman -S base-devel

# 2️⃣  Bauen
makepkg -si

# 3️⃣  (Installation passiert automatisch mit -i)

# 4️⃣  Starten
kodi &
```

---

## 📋 Dateien-Inhalt (Copy-Paste)

### debian/control
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
 media center, making it accessible for visually impaired users.
```

### debian/rules
```bash
#!/usr/bin/make -f
%:
	dh $@

override_dh_auto_build:
	# No build required

override_dh_auto_install:
	mkdir -p debian/kodi-screenreader/usr/share/kodi/addons
	install -dm755 debian/kodi-screenreader/usr/share/kodi/addons/service.xbmc.tts
	cp -a service.xbmc.tts/. debian/kodi-screenreader/usr/share/kodi/addons/service.xbmc.tts/
	if [ -d ruuk.addon.repository ]; then cp -a ruuk.addon.repository/. debian/kodi-screenreader/usr/share/kodi/addons/ruuk.addon.repository/; fi
	if [ -d script.module.nvdacontrollerclient ]; then cp -a script.module.nvdacontrollerclient/. debian/kodi-screenreader/usr/share/kodi/addons/script.module.nvdacontrollerclient/; fi

override_dh_auto_test:
	# No tests
```

### debian/changelog
```
kodi-screenreader (1.0.0-1) unstable; urgency=medium

  * Initial Debian release

 -- Dave <dave090679@users.noreply.github.com>  Mon, 21 Jan 2026 12:00:00 +0000
```

### debian/compat
```
13
```

### debian/copyright
```
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: kodi-screenreader
Source: https://github.com/dave090679/kodi_screenreader

Files: *
Copyright: 2014-2026 Dave and Contributors
License: GPL-2+

Files: script.module.nvdacontrollerclient/*
Copyright: NVDA Access Contributors
License: LGPL-2.1+
```

### debian/postinst
```bash
#!/bin/bash
set -e

mkdir -p /etc/kodi/userdata
command -v kodi >/dev/null 2>&1 && \
  chown -R kodi:kodi /usr/share/kodi/addons/service.xbmc.tts 2>/dev/null

exit 0
```

### debian/postrm
```bash
#!/bin/bash
set -e

if [ "$1" = "purge" ]; then
    rm -rf /etc/kodi/userdata/addon_data/service.xbmc.tts
fi

exit 0
```

### PKGBUILD (Arch)
```bash
# Maintainer: Dave <dave090679@users.noreply.github.com>
pkgname=kodi-screenreader
pkgver=1.0.0
pkgrel=1
pkgdesc="Screenreader addon for Kodi media center"
arch=('any')
url="https://github.com/dave090679/kodi_screenreader"
license=('GPL2' 'LGPL2.1')
depends=('kodi' 'python')
makedepends=('git')
source=("git+https://github.com/dave090679/kodi_screenreader.git")
md5sums=('SKIP')

package() {
    cd "$pkgname"
    
    install -dm755 "${pkgdir}/usr/share/kodi/addons"
    install -dm755 "${pkgdir}/usr/share/kodi/addons/service.xbmc.tts"
    cp -a service.xbmc.tts/. "${pkgdir}/usr/share/kodi/addons/service.xbmc.tts/"
    if [ -d "ruuk.addon.repository" ]; then install -dm755 "${pkgdir}/usr/share/kodi/addons/ruuk.addon.repository"; cp -a ruuk.addon.repository/. "${pkgdir}/usr/share/kodi/addons/ruuk.addon.repository/"; fi
    if [ -d "script.module.nvdacontrollerclient" ]; then install -dm755 "${pkgdir}/usr/share/kodi/addons/script.module.nvdacontrollerclient"; cp -a script.module.nvdacontrollerclient/. "${pkgdir}/usr/share/kodi/addons/script.module.nvdacontrollerclient/"; fi
    
    install -Dm644 LICENSE "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
}
```

---

## 🎮 Nach Installation

| Taste | Funktion |
|-------|----------|
| **F12** | Screenreader AN/AUS |
| **F1** | Text wiederholen |
| **F2** | Info |
| **F4** | Stoppen |
| **Ctrl+NumPad±** | Lautstärke |

---

## 🔍 Verzeichnisstruktur nach Installation

```
kodi_screenreader/
├── debian/                          # ← Debian-Dateien
│   ├── control
│   ├── rules
│   ├── changelog
│   ├── compat
│   ├── copyright
│   ├── postinst
│   └── postrm
├── PKGBUILD                         # ← Arch-Datei
├── service.xbmc.tts/                # Bestehend
├── script.module.nvdacontrollerclient/  # Bestehend
├── ruuk.addon.repository/           # Bestehend
├── service.xbmc.tts.keyboard.xml    # Bestehend
├── ENABLED                          # Bestehend
└── LICENSE                          # Bestehend
```

---

## ✅ Checkliste

### Debian Setup
- [ ] `mkdir -p debian`
- [ ] Alle 7 control/rules/changelog/etc. Dateien in `debian/` erstellt
- [ ] `chmod +x debian/rules debian/postinst debian/postrm`
- [ ] `sudo apt-get install build-essential debhelper`
- [ ] `dpkg-buildpackage -us -uc` erfolgreich
- [ ] `sudo dpkg -i ../kodi-screenreader_1.0.0-1_all.deb`

### Arch Setup
- [ ] PKGBUILD im Root-Verzeichnis
- [ ] `sudo pacman -S base-devel`
- [ ] `makepkg -si` erfolgreich

### Test
- [ ] `kodi` startet ohne Fehler
- [ ] **F12** aktiviert Screenreader
- [ ] Addon-Verzeichnis korrekt unter `/usr/share/kodi/addons/`

---

## 🚨 Fehler & Lösungen

| Fehler | Lösung |
|--------|--------|
| Command not found: dpkg-buildpackage | `sudo apt-get install build-essential debhelper` |
| Cannot access /etc/kodi | Script mit `sudo` ausführen oder: `sudo chown -R $(user):$(user) /etc/kodi` |
| Kodi nicht installiert | Debian: `sudo apt-get install kodi` \| Arch: `sudo pacman -S kodi` |
| Paket-Abhängigkeiten fehlen | Debian: `sudo apt-get install -f` \| Arch: `makepkg --syncdeps` |
| Permission denied debian/rules | `chmod +x debian/rules` |

---

## 📞 Support

- Debian: https://www.debian.org/doc/
- Arch: https://wiki.archlinux.org/title/Pacman
- Kodi: https://kodi.wiki/

---

**Status:** ✅ Alle Dateien erstellt  
**Kompatibilität:** Debian/Ubuntu, Arch Linux, andere RPM-basierte  
**Version:** 1.0.0  
**Datum:** 21. Januar 2026
