# kodi_screenreader
 nsis installer for kodi screenreader for windows based on the kodi sfreenreader from @pvagner

## macOS

The macOS installer (`kodi_screenreader_macos_<version>.pkg`) installs the addon, the keymap
and the enable marker into the Kodi profile of every user who uses Kodi
(`~/Library/Application Support/Kodi`) and enables the addon in Kodi's addon database,
so it speaks on the next Kodi start. Kodi must be installed and not running.

Speech uses the macOS `say` voices (voice, speed and volume can be set in the addon settings).
If VoiceOver is running and "Allow VoiceOver to be controlled with AppleScript" is enabled
in VoiceOver Utility, VoiceOver can be selected as the speech engine instead.

The package is not signed. On first open, macOS may block it: open it with
Control-click > Open, or allow it under System Settings > Privacy & Security.

Build the package on a Mac (Xcode command line tools are not required):

```
packaging/macos/build_pkg.sh
```

Set `SIGN_IDENTITY="Developer ID Installer: ..."` to sign it.

Uninstall:

```
sudo "/Library/Application Support/Kodi Screenreader/uninstall.sh"
```
