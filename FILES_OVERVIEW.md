# 📦 Kodi Screenreader - Build Files Übersicht

**Datum:** 21. Januar 2026  
**Repository:** dave090679/kodi_screenreader  
**Version:** 1.0.0

---

## 📄 Erstellte Dateien (insgesamt)

### 1. LINUX_BUILD_FILES.md
**Umfang:** Vollständige detaillierte Dokumentation  
**Inhalt:**
- Alle Debian-Dateien mit vollständigem Inhalt
- PKGBUILD mit Erklärungen
- Schritt-für-Schritt Build-Anleitung
- Installationsschritte für beide Distributionen
- Dateistruktur nach Installation
- Troubleshooting-Guide

**Verwendung:** 
- Copy-Paste alle Inhalte direkt in die Dateien
- Wird dann ins Repository kopiert

---

### 2. BUILD_INSTRUCTIONS.md
**Umfang:** Kurzanleitung für eilige Nutzer  
**Inhalt:**
- Projektübersicht
- Debian Installation (4 Schritte)
- Arch Installation (4 Schritte)
- Datei-Referenz
- Post-Installation
- Deinstallation
- Troubleshooting

**Verwendung:**
- Schneller Einstieg
- Im Repository als Dokumentation

---

### 3. SETUP_SUMMARY.md
**Umfang:** Zusammenfassung mit Kontext  
**Inhalt:**
- Was wurde erstellt (Übersicht)
- Automatisches Setup (Anleitung)
- Manuelles Setup (Anleitung)
- Debian Build Details
- Arch Build Details
- Installation & Test
- Deinstallation
- Troubleshooting
- Spezialfeatures

**Verwendung:**
- Verständnis für die Struktur
- Kontext für die Dateien

---

### 4. QUICK_REFERENCE.md
**Umfang:** Schnelle Referenzkarte  
**Inhalt:**
- Dateien zur Erstellung (kompakt)
- Schnell-Anleitung (4 Schritte je Distribution)
- Alle Dateien-Inhalte zum Copy-Paste
- Tastaturkombinationen
- Verzeichnisstruktur
- Checkliste
- Fehler & Lösungen
- Support-Links

**Verwendung:**
- Häufig zitierte Referenz
- Schnelle Lösungen finden

---

### 5. setup_linux_builds.sh
**Umfang:** Automatisiertes Setup-Skript  
**Inhalt:**
- Bash-Skript zur automatischen Erstellung aller Dateien
- Farbige Ausgabe für bessere Lesbarkeit
- Automatische Berechtigungen (chmod +x)
- Verzeichnisstruktur wird erstellt
- Abschlussinformation mit nächsten Schritten

**Verwendung:**
```bash
chmod +x setup_linux_builds.sh
./setup_linux_builds.sh
```

---

## 🎯 Welche Datei für welchen Zweck?

| Zweck | Datei | Aktion |
|-------|-------|--------|
| **Alles kopieren** | LINUX_BUILD_FILES.md | Inhalte Copy-Paste |
| **Schnell bauen** | QUICK_REFERENCE.md | Copy-Paste + Befehle |
| **Verstehen** | BUILD_INSTRUCTIONS.md | Lesen |
| **Details** | SETUP_SUMMARY.md | Lesen |
| **Automatisch** | setup_linux_builds.sh | Ausführen |

---

## 📊 Dateien-Statistik

| Datei | Zeilen | Größe | Typ |
|-------|--------|-------|-----|
| debian/control | 23 | ~1.2 KB | Konfiguration |
| debian/rules | 21 | ~1.0 KB | Bash |
| debian/changelog | 6 | ~0.3 KB | Text |
| debian/compat | 1 | ~0.02 KB | Text |
| debian/copyright | 48 | ~2.5 KB | Text |
| debian/postinst | 13 | ~0.5 KB | Bash |
| debian/postrm | 10 | ~0.4 KB | Bash |
| PKGBUILD | 67 | ~2.8 KB | Bash |
| **Gesamt Debian** | **122** | **~6.9 KB** | - |
| **Gesamt Arch** | **67** | **~2.8 KB** | - |

---

## 🔑 Schlüsseldateien in Repository

Nach dem Setup sollte das Repository so aussehen:

```
kodi_screenreader/
├── debian/                              ✅ NEU
│   ├── control
│   ├── rules
│   ├── changelog
│   ├── compat
│   ├── copyright
│   ├── postinst
│   └── postrm
├── PKGBUILD                             ✅ NEU
├── service.xbmc.tts/                    ✓ Existiert
├── script.module.nvdacontrollerclient/  ✓ Existiert
├── ruuk.addon.repository/               ✓ Existiert
├── service.xbmc.tts.keyboard.xml        ✓ Existiert
├── ENABLED                              ✓ Existiert
├── LICENSE                              ✓ Existiert
├── README.md                            ✓ Existiert
├── .gitignore                           ✓ Existiert
└── kodi_screenreader.nsi                ✓ Existiert (Windows)
```

---

## 🚀 Implementierungsschritte

### Schritt 1: Dateien ins Repository kopieren (5 Min)

**Option A - Automatisch:**
```bash
chmod +x setup_linux_builds.sh
./setup_linux_builds.sh
```

**Option B - Manuell:**
1. Alle Inhalte aus `LINUX_BUILD_FILES.md` kopieren
2. In passende Dateien unter `debian/` und root einfügen
3. Berechtigungen: `chmod +x debian/rules debian/postinst debian/postrm`

### Schritt 2: Debian-Version testen (10 Min)

```bash
# System vorbereiten
sudo apt-get update
sudo apt-get install build-essential debhelper dh-make git kodi python3

# Im Repository-Root
cd kodi_screenreader
dpkg-buildpackage -us -uc

# Testen
sudo dpkg -i ../kodi-screenreader_1.0.0-1_all.deb
```

### Schritt 3: Arch-Version testen (10 Min)

```bash
# System vorbereiten
sudo pacman -Syu
sudo pacman -S base-devel git kodi python

# Im Repository-Root
cd kodi_screenreader
makepkg -si
```

### Schritt 4: Beide Versionen validieren (5 Min)

```bash
# Paketinfo zeigen
dpkg -l | grep kodi-screenreader
pacman -Q kodi-screenreader

# Installationsverzeichnis prüfen
ls -la /usr/share/kodi/addons/service.xbmc.tts
ls -la /etc/kodi/userdata/keymaps/

# Kodi starten und testen
kodi &
```

---

## 📋 Abhängigkeiten

### Debian/Ubuntu
```
build-essential    - Compiler und Tools
debhelper          - Debian packaging tools
dh-make            - Debian helper for package creation
git                - Version control (falls benötigt)
kodi               - Kodi media center
python3            - Python runtime
```

### Arch Linux
```
base-devel         - Compiler und Tools (Gruppe)
git                - Version control (falls benötigt)
kodi               - Kodi media center
python             - Python runtime
```

---

## 🎯 Installationsziele

Nach erfolgreichem Build und Installation:

**Addons-Verzeichnis:**
```
/usr/share/kodi/addons/
├── service.xbmc.tts/
│   ├── addon.xml
│   ├── service.py
│   └── resources/
├── ruuk.addon.repository/
│   └── addon.xml
└── script.module.nvdacontrollerclient/
    ├── addon.xml
    └── nvda/
```

**Konfiguration:**
```
/etc/kodi/userdata/keymaps/
└── service.xbmc.tts.keyboard.xml

/etc/kodi/userdata/addon_data/service.xbmc.tts/
└── ENABLED
```

**Lizenzen:**
```
/usr/share/licenses/kodi-screenreader/
├── LICENSE
└── NVDA-LICENSE (nur Arch)
```

---

## ✨ Besonderheiten

### Debian Packaging
- ✅ Debhelper 13 (modernes Format)
- ✅ Debian Standards-Version 4.6.0
- ✅ Proper copyright format
- ✅ Post-installation hooks für Berechtigungen
- ✅ Post-removal hooks für Cleanup

### Arch Packaging
- ✅ Git-basierte Versionierung
- ✅ Automatische Lizenz-Installation
- ✅ Modern PKGBUILD format
- ✅ Sichere Dateiinstallation mit install-Befehlen
- ✅ Proper md5sums handling

### Allgemein
- ✅ Plattformunabhängig (all/any arch)
- ✅ Kein kompilierter Code (nur Python)
- ✅ Korrekte Berechtigungen
- ✅ Lizenzkonform (GPL-2+, LGPL-2.1+)
- ✅ Backward-kompatibel
- ✅ Alle bestehenden Dateien erhalten

---

## 🔄 Workflow-Beispiel

```
1. Repository klonen
   └─> git clone https://github.com/dave090679/kodi_screenreader.git

2. Build-Dateien kopieren
   └─> LINUX_BUILD_FILES.md Inhalte einfügen ODER
   └─> setup_linux_builds.sh ausführen

3. Auf Debian/Ubuntu testen
   └─> dpkg-buildpackage -us -uc
   └─> sudo dpkg -i *.deb

4. Auf Arch Linux testen
   └─> makepkg -si

5. Validieren
   └─> kodi starten
   └─> F12 drücken (Screenreader aktivieren)

6. Ins Repository committen
   └─> git add debian/ PKGBUILD
   └─> git commit -m "Add Linux build files for Debian and Arch"
   └─> git push
```

---

## 📞 Häufig gestellte Fragen

### F: Brauche ich alle Dateien?
**A:** Ja, für Debian alle 7 Dateien im `debian/`-Verzeichnis, und die `PKGBUILD` für Arch.

### F: Kann ich nur Debian oder nur Arch bauen?
**A:** Ja, beide sind unabhängig. Sie können eine oder beide implementieren.

### F: Was ist der Unterschied zwischen den Dateien?
**A:** Debian verwendet Debhelper, Arch ein einfacheres Bash-Skript. Das Ergebnis ist ähnlich.

### F: Muss ich etwas compilieren?
**A:** Nein, alle Komponenten sind Python (nicht kompiliert).

### F: Funktioniert es auch auf anderen Linux-Distributionen?
**A:** Debian-Dateien funktionieren auf Debian/Ubuntu/Linux Mint/etc. Für Fedora/RHEL müsste man `.spec` Dateien erstellen.

---

## 🔗 Verwandte Dateien im Repository

- **README.md** - Bestehende Projektdokumentation
- **LICENSE** - GPL-2+ Lizenz
- **kodi_screenreader.nsi** - Windows Installer (NSIS)
- **.gitignore** - Git ignore patterns
- **service.xbmc.tts/** - Screenreader-Service
- **script.module.nvdacontrollerclient/** - NVDA Module

---

## ✅ Validierungs-Checkliste

Nach der Installation ausführen:

```bash
# Paket-Information
[ ] dpkg -l | grep kodi-screenreader (Debian)
[ ] pacman -Q kodi-screenreader (Arch)

# Dateien-Verzeichnis
[ ] test -d /usr/share/kodi/addons/service.xbmc.tts
[ ] test -d /usr/share/kodi/addons/ruuk.addon.repository
[ ] test -d /usr/share/kodi/addons/script.module.nvdacontrollerclient
[ ] test -f /etc/kodi/userdata/keymaps/service.xbmc.tts.keyboard.xml
[ ] test -f /etc/kodi/userdata/addon_data/service.xbmc.tts/ENABLED

# Funktionstest
[ ] kodi startet ohne Fehler
[ ] F12 aktiviert Screenreader
[ ] Tastaturkombinationen funktionieren
[ ] Addon ist in Kodi visible
```

---

**Status:** ✅ Alle Build-Dateien erfolgreich erstellt  
**Nächster Schritt:** Dateien ins Repository kopieren und testen  
**Dokumentation:** Alle Details in obigen Dateien
