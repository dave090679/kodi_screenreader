# Kodi Screenreader - Build Files für Linux (Debian & Arch)

## Übersicht

Dieses Paket enthält alle notwendigen Build-Dateien zur Erstellung von Installationspaketen für Debian/Ubuntu und Arch Linux Distributionen.

**Komponenten:**
- **service.xbmc.tts** - Hauptscreenreader-Service
- **script.module.nvdacontrollerclient** - NVDA Integration
- **ruuk.addon.repository** - Addon-Repository
- **service.xbmc.tts.keyboard.xml** - Tastaturkonfiguration
- **ENABLED** - Aktivierungsflag

---

## Debian/Ubuntu Installation

### 1. Debian-Dateien vorbereiten

Erstellen Sie die folgende Verzeichnisstruktur im Repository-Root:

```
kodi_screenreader/
├── debian/
│   ├── control
│   ├── rules
│   ├── changelog
│   ├── compat
│   ├── copyright
│   ├── postinst
│   └── postrm
├── service.xbmc.tts/
├── script.module.nvdacontrollerclient/
├── ruuk.addon.repository/
├── service.xbmc.tts.keyboard.xml
├── ENABLED
└── LICENSE
```

### 2. Abhängigkeiten installieren

```bash
sudo apt-get update
sudo apt-get install build-essential debhelper dh-make git
```

### 3. Package bauen

```bash
cd kodi_screenreader
dpkg-buildpackage -us -uc
```

Ausgabe: `../kodi-screenreader_1.0.0-1_all.deb`

### 4. Installieren

```bash
sudo dpkg -i ../kodi-screenreader_1.0.0-1_all.deb
sudo apt-get install -f  # Falls Abhängigkeiten fehlen
```

---

## Arch Linux Installation

### 1. PKGBUILD vorbereiten

Kopieren Sie `PKGBUILD` in das Repository-Root-Verzeichnis.

### 2. Abhängigkeiten installieren

```bash
sudo pacman -S base-devel git
```

### 3. Package bauen und installieren

```bash
cd kodi_screenreader
makepkg -si
```

Oder nur bauen:
```bash
makepkg
```

Die Datei `kodi-screenreader-1.0.0-1-any.pkg.tar.zst` wird erstellt.

---

## Datei-Referenz

### debian/control
Paketmetadaten, Abhängigkeiten und Beschreibung. Wichtige Felder:
- `Depends: kodi (>= 18), python3`
- `Architecture: all` (plattformunabhängig)

### debian/rules
Debhelper-Build-Skript. Installiert Addons zu:
- `/usr/share/kodi/addons/`
- `/etc/kodi/userdata/`

### debian/changelog
Versionsverlauf. Format: `paket (version) verteilung; dringlichkeit`

### debian/postinst
Läuft nach Installation:
- Erstellt Verzeichnisse
- Setzt Kodi-Berechtigungen

### debian/postrm
Läuft nach Deinstallation:
- Cleanup bei vollständiger Entfernung (purge)

### PKGBUILD
Arch Linux Build-Skript mit:
- `pkgver()` - Git-basierte Versionierung
- `package()` - Installation zu systemweiten Verzeichnissen

---

## Post-Installation

### Kodi starten
```bash
# Debian/Ubuntu/Arch
kodi &

# oder mit systemd (falls Service existiert)
sudo systemctl start kodi
```

### Screenreader aktivieren
1. Kodi öffnen
2. **F12** drücken

### Verfügbare Tasten
| Taste | Funktion |
|-------|----------|
| **F1** | Text wiederholen |
| **F2** | Info anzeigen |
| **F3** | Item-Details |
| **F4** | Stoppen |
| **F6** | Einstellungen |
| **F12** | Screenreader an/aus |
| **Ctrl+NumPad±** | Lautstärke |

---

## Deinstallation

### Debian/Ubuntu
```bash
# Entfernen (Config bleibt)
sudo apt-get remove kodi-screenreader

# Vollständig entfernen (mit Config)
sudo apt-get purge kodi-screenreader
```

### Arch
```bash
# Entfernen
sudo pacman -R kodi-screenreader

# Mit Konfigurationen (manuell)
sudo rm -rf /etc/kodi/userdata/addon_data/service.xbmc.tts
```

---

## Troubleshooting

### Fehler: "kodi: command not found"
```bash
# Debian/Ubuntu
sudo apt-get install kodi

# Arch
sudo pacman -S kodi
```

### Fehler: "Permission denied" beim Zugriff auf /etc/kodi/
```bash
sudo chown -R $USER:$USER /etc/kodi/userdata/
```

### Addon wird nicht geladen
1. Stellen Sie sicher, dass Kodi mit der korrekten Konfiguration startet
2. Überprüfen Sie die Datei `ENABLED`
3. Starten Sie Kodi neu und prüfen Sie die Logs

---

## Weitere Optionen

### Lokale Pakete hochladen

Nachdem Sie das Paket gebaut haben:

**Debian Package Registry (PPAs):**
```bash
dput ppa:your-username/ppa ../kodi-screenreader_1.0.0-1_all.deb
```

**Arch Linux AUR (Arch User Repository):**
Erfordert `git` und AUR-Setup. Siehe: https://aur.archlinux.org/

---

## Lizensierung

- **service.xbmc.tts** & **ruuk.addon.repository**: GPL-2+
- **script.module.nvdacontrollerclient**: LGPL-2.1+

Die Dateien werden mit korrekten Lizenzen verpackt.

---

## Quellen

- [Debian Packaging Manual](https://www.debian.org/doc/manuals/debmake-doc/)
- [Arch Linux Packaging](https://wiki.archlinux.org/title/PKGBUILD)
- [Kodi Add-on Development](https://kodi.wiki/view/Add-on_development)

