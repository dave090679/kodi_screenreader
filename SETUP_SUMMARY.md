# ✅ Kodi Screenreader - Linux Build Files erstellt

## 📦 Was wurde erstellt?

Ich habe vollständige Build-Dateien für **Debian/Ubuntu** und **Arch Linux** erstellt.

### Dateiübersicht:

#### 📂 Debian-Dateien (im `debian/` Verzeichnis)
- **control** - Paketmetadaten und Abhängigkeiten
- **rules** - Debhelper Build-Skript (hauptsächliches Build-Script)
- **changelog** - Versionsverlauf (1.0.0-1)
- **compat** - Debhelper Kompatibilitätslevel (13)
- **copyright** - Lizenzen (GPL-2+ und LGPL-2.1+)
- **postinst** - Post-Installation (Berechtigungen setzen)
- **postrm** - Post-Deinstallation (Cleanup)

#### 📄 Arch Linux Datei
- **PKGBUILD** - Arch Linux Paketbuild-Skript

---

## 🚀 Verwendung

### Automatisches Setup (empfohlen)

Es gibt ein Automatisierungsskript:

```bash
# 1. Skript ausführbar machen
chmod +x setup_linux_builds.sh

# 2. Im Repository-Root-Verzeichnis ausführen
./setup_linux_builds.sh
```

Das Skript erstellt automatisch alle Dateien im korrekten Format.

### Manuelles Setup

1. **Debian-Verzeichnis erstellen:**
   ```bash
   mkdir -p debian
   ```

2. **Alle Dateien aus dem Dokument `LINUX_BUILD_FILES.md` kopieren**
   - Jede Datei in das entsprechende Verzeichnis legen

3. **Berechtigungen setzen:**
   ```bash
   chmod +x debian/rules
   chmod +x debian/postinst
   chmod +x debian/postrm
   ```

---

## 🔨 Debian/Ubuntu Package bauen

```bash
# 1. Abhängigkeiten
sudo apt-get install build-essential debhelper dh-make git

# 2. Im Repository-Root:
cd kodi_screenreader

# 3. Package bauen
dpkg-buildpackage -us -uc

# 4. Installieren
sudo dpkg -i ../kodi-screenreader_1.0.0-1_all.deb

# Falls Abhängigkeiten fehlen:
sudo apt-get install -f
```

**Ausgabedatei:** `../kodi-screenreader_1.0.0-1_all.deb`

---

## 🔨 Arch Linux Package bauen

```bash
# 1. Abhängigkeiten
sudo pacman -S base-devel git

# 2. Im Repository-Root mit PKGBUILD:
cd kodi_screenreader

# 3. Package bauen und installieren
makepkg -si

# oder nur bauen:
makepkg
```

**Ausgabedatei:** `kodi-screenreader-1.0.0-1-any.pkg.tar.zst`

---

## 📋 Was wird wo installiert?

Nach erfolgreicher Installation:

```
/usr/share/kodi/addons/
├── service.xbmc.tts/              ← Hauptscreenreader-Service
├── ruuk.addon.repository/         ← Addon-Repository
└── script.module.nvdacontrollerclient/  ← NVDA-Integration

/etc/kodi/userdata/keymaps/
└── service.xbmc.tts.keyboard.xml  ← Tastaturkonfiguration

/etc/kodi/userdata/addon_data/service.xbmc.tts/
└── ENABLED                         ← Aktivierungsflag
```

---

## ⚙️ Debian Build-Details

### debian/control
- **Source:** kodi-screenreader
- **Architecture:** all (plattformunabhängig)
- **Depends:** kodi (>= 18), python3
- **Section:** media

### debian/rules
Verwendet `debhelper` (dh) mit Überschreibungen:
- `override_dh_auto_build` - Kein Build nötig (Python)
- `override_dh_auto_install` - Kopiert Dateien zu Zielverzeichnissen
- `override_dh_auto_test` - Keine Tests

### Installationspfade
- Addons → `/usr/share/kodi/addons/`
- Konfiguration → `/etc/kodi/userdata/`

---

## ⚙️ Arch Build-Details

### PKGBUILD
- **pkgname:** kodi-screenreader
- **pkgver:** 1.0.0 (Git-basiert)
- **arch:** any (plattformunabhängig)
- **depends:** kodi, python
- **Lizenz:** GPL2, LGPL2.1

### Funktionen
- Automatische Git-basierte Versionierung
- Sichere Dateiinstallation mit `install` Befehlen
- Lizenz-Dateien im richtigen Verzeichnis

---

## 🎮 Nach Installation

### Kodi starten
```bash
kodi &
```

### Screenreader aktivieren
1. **F12** drücken in Kodi

### Tastaturkombinationen
| Taste | Funktion |
|-------|----------|
| F1 | Text wiederholen |
| F2 | Info anzeigen |
| F3 | Item-Details |
| F4 | Stoppen |
| F6 | Einstellungen |
| F12 | Screenreader an/aus |
| Ctrl+NumPad+ | Lautstärke erhöhen |
| Ctrl+NumPad- | Lautstärke senken |

---

## 🧹 Deinstallation

### Debian/Ubuntu
```bash
# Paket entfernen (Config bleibt)
sudo apt-get remove kodi-screenreader

# Vollständig entfernen (mit Config)
sudo apt-get purge kodi-screenreader
```

### Arch
```bash
# Paket entfernen
sudo pacman -R kodi-screenreader

# Config manuell entfernen
sudo rm -rf /etc/kodi/userdata/addon_data/service.xbmc.tts
```

---

## 🆘 Troubleshooting

### Problem: "kodi: command not found"
```bash
# Debian
sudo apt-get install kodi

# Arch
sudo pacman -S kodi
```

### Problem: Berechtigungsfehler bei /etc/kodi/
Das postinst-Skript sollte Berechtigungen automatisch setzen. Falls nötig:
```bash
sudo chown -R kodi:kodi /etc/kodi/userdata/
sudo chmod -R 755 /etc/kodi/userdata/
```

### Problem: Addon wird nicht erkannt
1. Überprüfen Sie, dass `ENABLED` Datei vorhanden ist
2. Starten Sie Kodi neu: `sudo systemctl restart kodi`
3. Überprüfen Sie Kodi-Logs

---

## 📚 Dateien-Referenz

### LINUX_BUILD_FILES.md
Komplette Dokumentation mit:
- Allen Dateieninhalten zum Copy-Paste
- Schritt-für-Schritt Anleitung
- Alle Build-Befehle
- Troubleshooting

### BUILD_INSTRUCTIONS.md
Kurzanleitung mit:
- Übersicht der Komponenten
- Schnelle Installation
- Post-Installation
- Tastaturkombinationen

### setup_linux_builds.sh
Automatisiertes Setup-Skript:
- Erstellt alle Dateien
- Setzt richtige Berechtigungen
- Gibt Status-Ausgabe

---

## ✨ Spezialfeatures

### Git-basierte Versionierung (Arch)
Die `pkgver()` Funktion in PKGBUILD liest automatisch:
- Tags aus Git Repository
- Fallback auf 1.0.0 wenn keine Tags

### Intelligente Installation
Beide Build-Skripte:
- Ignorieren fehlende Dateien (z.B. wenn service.xbmc.tts leer)
- Setzen richtige Berechtigungen
- Installieren Lizenzen korrekt

### Plattformunabhängig
- `architecture: all` (Debian)
- `arch: any` (Arch)
- Kein Code wird kompiliert
- Läuft auf allen 64-bit und ARM-Systemen

---

## 📝 Nächste Schritte

1. **Dateien ins Repository kopieren:**
   - Alle Inhalte aus `LINUX_BUILD_FILES.md` in passende Dateien
   - Oder `setup_linux_builds.sh` ausführen

2. **Auf Ihrem System testen:**
   - Debian: `dpkg-buildpackage -us -uc`
   - Arch: `makepkg -si`

3. **Optional: In Repository-Paketen veröffentlichen:**
   - Debian: PPA (Personal Package Archive)
   - Arch: AUR (Arch User Repository)

---

## 🔗 Nützliche Ressourcen

- [Debian Packaging Guide](https://www.debian.org/doc/manuals/debmake-doc/)
- [Arch Linux PKGBUILD](https://wiki.archlinux.org/title/PKGBUILD)
- [Kodi Add-on Development](https://kodi.wiki/view/Add-on_development)
- [GitHub Releases API](https://docs.github.com/en/rest/releases/releases)

---

**Erstellt:** 21. Januar 2026  
**Repository:** kodi_screenreader  
**Version:** 1.0.0  
**Lizenzen:** GPL-2+, LGPL-2.1+
