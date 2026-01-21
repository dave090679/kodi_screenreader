# 🗺️ Kodi Screenreader - Integration Roadmap

**Datum:** 21. Januar 2026  
**Repository:** dave090679/kodi_screenreader  
**Ziel:** Vollständige Linux Package Integration

---

## 📍 Aktuelle Situation

### Vorhandene Files
- ✅ Windows Installer (kodi_screenreader.nsi)
- ✅ Addon-Komponenten (service.xbmc.tts, etc.)
- ✅ Konfigurationen (keyboard mappings, ENABLED flag)
- ✅ Dokumentation (README, LICENSE)

### Fehlende Files
- ❌ Debian Build Files (debian/)
- ❌ Arch Linux Build File (PKGBUILD)
- ❌ Linux-spezifische Dokumentation

---

## 🎯 Was wird jetzt hinzugefügt

### Debian/Ubuntu Support
```
debian/
├── control          ✅ Neu: Paketmetadaten
├── rules            ✅ Neu: Debhelper Build
├── changelog        ✅ Neu: Versionsverlauf
├── compat           ✅ Neu: Kompatibilität
├── copyright        ✅ Neu: Lizenzen
├── postinst         ✅ Neu: Nach Installation
└── postrm           ✅ Neu: Nach Removal
```

### Arch Linux Support
```
PKGBUILD            ✅ Neu: Arch Paketbuild
```

### Dokumentation
```
├── LINUX_BUILD_FILES.md     ✅ Neu: Vollständige Details
├── BUILD_INSTRUCTIONS.md    ✅ Neu: Kurzanleitung
├── SETUP_SUMMARY.md         ✅ Neu: Zusammenfassung
├── QUICK_REFERENCE.md       ✅ Neu: Schnellreferenz
├── FILES_OVERVIEW.md        ✅ Neu: Übersicht
├── README_FIRST.md          ✅ Neu: Einstieg
├── INDEX.md                 ✅ Neu: Index
├── setup_linux_builds.sh    ✅ Neu: Auto-Setup
└── INTEGRATION_ROADMAP.md   ✅ Neu: Diese Datei
```

---

## 📋 Integrations-Schritte

### Phase 1: Vorbereitung (Sofort)
**Aufwand:** 10 Minuten

- [ ] Alle erstellten Dateien herunterladen
- [ ] `setup_linux_builds.sh` oder `LINUX_BUILD_FILES.md` lesen
- [ ] Systemabhängigkeiten installieren (debhelper, base-devel)

**Befehl:**
```bash
# Für Debian/Ubuntu
sudo apt-get install build-essential debhelper dh-make git

# Für Arch Linux
sudo pacman -S base-devel git
```

---

### Phase 2: Dateien einfügen (10 Minuten)

**Option A - Automatisch:**
```bash
chmod +x setup_linux_builds.sh
./setup_linux_builds.sh
```

**Option B - Manuell:**
1. `mkdir -p debian`
2. Alle Inhalte aus `LINUX_BUILD_FILES.md` kopieren
3. In entsprechende Dateien einfügen
4. `chmod +x debian/rules debian/postinst debian/postrm`
5. `PKGBUILD` ins Root-Verzeichnis

**Repository-Struktur danach:**
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
├── PKGBUILD
├── service.xbmc.tts/
├── script.module.nvdacontrollerclient/
├── ruuk.addon.repository/
├── service.xbmc.tts.keyboard.xml
├── ENABLED
├── LICENSE
├── README.md
├── kodi_screenreader.nsi
└── .gitignore
```

---

### Phase 3: Debian testen (15 Minuten)

**Linux-System mit Debian/Ubuntu:**

```bash
# 1. Repository klonen/pullen
git clone https://github.com/dave090679/kodi_screenreader.git
cd kodi_screenreader

# 2. Bauen
dpkg-buildpackage -us -uc

# 3. Installation testen
sudo dpkg -i ../kodi-screenreader_1.0.0-1_all.deb

# 4. Abhängigkeiten lösen (falls nötig)
sudo apt-get install -f

# 5. Validieren
dpkg -l | grep kodi-screenreader
ls -la /usr/share/kodi/addons/service.xbmc.tts
```

**Erwartetes Ergebnis:**
- ✅ Paket wird gebaut (../kodi-screenreader_1.0.0-1_all.deb)
- ✅ Installation ohne Fehler
- ✅ Dateien unter /usr/share/kodi/addons/

---

### Phase 4: Arch testen (15 Minuten)

**Linux-System mit Arch:**

```bash
# 1. Repository klonen/pullen
git clone https://github.com/dave090679/kodi_screenreader.git
cd kodi_screenreader

# 2. Bauen und installieren
makepkg -si

# 3. Validieren
pacman -Q kodi-screenreader
ls -la /usr/share/kodi/addons/service.xbmc.tts
```

**Erwartetes Ergebnis:**
- ✅ Paket wird gebaut (kodi-screenreader-1.0.0-1-any.pkg.tar.zst)
- ✅ Installation ohne Fehler
- ✅ Dateien unter /usr/share/kodi/addons/

---

### Phase 5: Kodi testen (5 Minuten)

**Beide Systeme (nach Installation):**

```bash
# 1. Kodi starten
kodi &

# 2. F12 drücken → Screenreader sollte aktivieren
# 3. F1, F2, F4, etc. testen → Funktionen sollten ansprechbar sein
# 4. Addon sollte unter Settings → Add-ons sichtbar sein

# Oder vom Terminal prüfen:
ls -la /usr/share/kodi/addons/service.xbmc.tts
test -f /etc/kodi/userdata/keymaps/service.xbmc.tts.keyboard.xml && echo "OK" || echo "Missing"
test -f /etc/kodi/userdata/addon_data/service.xbmc.tts/ENABLED && echo "OK" || echo "Missing"
```

**Erwartetes Ergebnis:**
- ✅ Kodi startet
- ✅ Screenreader lässt sich mit F12 aktivieren
- ✅ Alle Dateien sind installiert

---

### Phase 6: Git Integration (10 Minuten)

```bash
# 1. Dateien zum Index hinzufügen
git add debian/ PKGBUILD

# 2. Dokumentation committen (optional)
git add LINUX_BUILD_FILES.md BUILD_INSTRUCTIONS.md ...

# 3. Committen
git commit -m "Add Linux build files for Debian and Arch Linux

- Add debian/ directory with control, rules, changelog, etc.
- Add PKGBUILD for Arch Linux package
- Add comprehensive documentation for Linux builds
- Support for dpkg and pacman package managers"

# 4. Pushen
git push origin main
```

**Im Repository-README aktualisieren:**
```markdown
## Linux Installation

### Debian/Ubuntu
dpkg-buildpackage -us -uc
sudo dpkg -i ../kodi-screenreader_1.0.0-1_all.deb

### Arch Linux
makepkg -si

Siehe `QUICK_REFERENCE.md` oder `BUILD_INSTRUCTIONS.md` für Details.
```

---

### Phase 7: Optional - Distribution einrichten

#### PPA für Debian (Personal Package Archive)
```bash
# 1. PPA einrichten (https://launchpad.net/~your-username/+ppas)
# 2. Paket hochladen
dput ppa:your-username/kodi-screenreader ../kodi-screenreader_1.0.0-1_all.deb
# 3. Benutzer können dann installieren mit:
sudo apt-add-repository ppa:your-username/kodi-screenreader
sudo apt-get update
sudo apt-get install kodi-screenreader
```

#### AUR für Arch (Arch User Repository)
```bash
# 1. AUR-Account erstellen (https://aur.archlinux.org/)
# 2. PKGBUILD in AUR hochladen
# 3. Benutzer können dann installieren mit:
yay -S kodi-screenreader
# oder
makepkg -si <(git clone https://aur.archlinux.org/kodi-screenreader.git)
```

---

## 📊 Zeitplan

| Phase | Aufwand | Gesamt | Status |
|-------|---------|--------|--------|
| 1. Vorbereitung | 10 Min | 10 Min | ⏳ TODO |
| 2. Dateien einfügen | 10 Min | 20 Min | ⏳ TODO |
| 3. Debian testen | 15 Min | 35 Min | ⏳ TODO |
| 4. Arch testen | 15 Min | 50 Min | ⏳ TODO |
| 5. Kodi testen | 5 Min | 55 Min | ⏳ TODO |
| 6. Git Integration | 10 Min | 65 Min | ⏳ TODO |
| 7. Distribution (Optional) | 20 Min | 85 Min | ⏳ OPTIONAL |

**Geschätzter Gesamtaufwand: ~1 Stunde (Kernintegration)**

---

## 🎯 Erfolgs-Kriterien

Nach allen Phasen sollten Sie folgende Punkte erfüllen:

### Repository
- ✅ Dateien `debian/*` vorhanden
- ✅ Datei `PKGBUILD` vorhanden
- ✅ Dokumentation in README referenziert

### Debian Build
- ✅ `dpkg-buildpackage -us -uc` funktioniert
- ✅ Package `kodi-screenreader_1.0.0-1_all.deb` wird erstellt
- ✅ Installation mit `dpkg -i` funktioniert
- ✅ Addon unter `/usr/share/kodi/addons/` sichtbar

### Arch Build
- ✅ `makepkg -si` funktioniert
- ✅ Package `kodi-screenreader-1.0.0-1-any.pkg.tar.zst` wird erstellt
- ✅ Paket ist mit `pacman -Q` sichtbar
- ✅ Addon unter `/usr/share/kodi/addons/` sichtbar

### Funktionalität
- ✅ Kodi startet ohne Fehler
- ✅ Screenreader mit F12 aktivierbar
- ✅ Alle Tastaturkombinationen funktionieren
- ✅ Addon-Einstellungen zugänglich

---

## 🛠️ Tools & Abhängigkeiten

### Debian/Ubuntu Build
```
build-essential     - Compiler und Build-Tools
debhelper           - Debian Packaging Tools
dh-make             - Debhelper Initialization
git                 - Version Control
```

Installation:
```bash
sudo apt-get install build-essential debhelper dh-make git
```

### Arch Linux Build
```
base-devel         - Build Tools (Paketgruppe)
git                - Version Control
```

Installation:
```bash
sudo pacman -S base-devel git
```

### Runtime (beide Systeme)
```
kodi               - Kodi Media Center
python3/python     - Python Runtime
```

---

## 📝 Dokumentation im Repository

Nach Integration sollten Sie folgende Dateien im Repository haben:

```
README.md                   ← Aktualisieren mit Linux-Sektion
├─ Windows Installation     (Existiert: kodi_screenreader.nsi)
├─ Linux Installation       (NEU: QUICK_REFERENCE.md oder BU.md)
└─ Mehr Infos               (NEU: Link zu Dateien)

Für Details:
├─ QUICK_REFERENCE.md       ← Schnelle Anleitung
├─ BUILD_INSTRUCTIONS.md    ← Kurz & prägnant
├─ LINUX_BUILD_FILES.md     ← Vollständig
└─ Weitere                  ← Optional in docs/ ordner
```

---

## 🚀 Automation (Optional)

### GitHub Actions für automatisches Bauen

Datei: `.github/workflows/build-linux.yml`
```yaml
name: Build Linux Packages

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build Debian Package
        run: dpkg-buildpackage -us -uc
      - name: Upload Artifacts
        uses: actions/upload-artifact@v2
        with:
          name: debian-package
          path: ../kodi-screenreader_*.deb
```

---

## ✅ Checkliste für Integration

### Vor Beginn
- [ ] Alle Dateien herunterladen (from /tmp/)
- [ ] README_FIRST.md gelesen
- [ ] Abhängigkeiten installiert

### Phase 2 (Dateien)
- [ ] `debian/` Verzeichnis erstellt
- [ ] Alle 7 debian/ Dateien eingefügt
- [ ] PKGBUILD eingefügt
- [ ] Berechtigungen korrekt (chmod +x)
- [ ] Dateien mit git tracked

### Phase 3 & 4 (Testen)
- [ ] Debian Build erfolgreich
- [ ] Debian Package installierbar
- [ ] Arch Build erfolgreich
- [ ] Arch Package installierbar

### Phase 5 (Kodi)
- [ ] Kodi startet
- [ ] Screenreader funktioniert (F12)
- [ ] Addons sichtbar
- [ ] Tastaturshortcuts funktionieren

### Phase 6 (Git)
- [ ] Alle Dateien gepusht
- [ ] README aktualisiert
- [ ] Dokumentation verlinkt

---

## 📞 Support & Hilfe

| Problem | Lösung |
|---------|--------|
| Fehler beim Bauen | Siehe QUICK_REFERENCE.md → Fehler & Lösungen |
| Abhängigkeiten fehlen | sudo apt-get install -f (Debian) oder makepkg --syncdeps (Arch) |
| Installation fehlgeschlagen | Check /var/log/dpkg.log (Debian) oder pacman.log (Arch) |
| Addon wird nicht erkannt | Kodi neustarten, F12 drücken |

---

## 🎉 Ergebnis nach erfolgreicher Integration

### Linux-Benutzer können jetzt:
1. **Auf Debian/Ubuntu installieren:**
   ```bash
   dpkg-buildpackage -us -uc
   sudo dpkg -i kodi-screenreader_1.0.0-1_all.deb
   ```

2. **Auf Arch installieren:**
   ```bash
   makepkg -si
   ```

3. **Screenreader verwenden:**
   - Kodi starten → F12 → Fertig

### Sie haben erreicht:
- ✅ Windows Installer (existierend)
- ✅ Debian/Ubuntu Package (neu)
- ✅ Arch Linux Package (neu)
- ✅ Umfassende Dokumentation
- ✅ Automatisierte Builds (optional)

---

## 🔄 Zukünftige Erweiterungen

### Möglich nach erfolgreicher Integration:
1. **RPM-Pakete** (Fedora, OpenSUSE) - SPEC-Datei
2. **Snap** - snapcraft.yaml
3. **Flatpak** - org.kodi.screenreader.json
4. **AppImage** - AppImage.AppDir/
5. **PPA/AUR-Veröffentlichung**
6. **CI/CD Pipeline** (GitHub Actions, etc.)

---

**Roadmap erstellt:** 21. Januar 2026  
**Status:** ✅ Bereit zur Implementierung  
**Nächster Schritt:** Phase 1 & 2 durchführen  

→ **Beginnen Sie mit: README_FIRST.md lesen + setup_linux_builds.sh ausführen**
