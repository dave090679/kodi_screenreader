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

## Accessibility setup (`service.accessibility.setup`)

Companion add-on to the screen reader. On the first Kodi start it:

- creates the skin **Estuary barrierefrei**, a copy of Kodi's Estuary where the home menu
  is only left with Enter (Right no longer jumps into the widget row), and switches to it.
  After a Kodi update with a new Estuary, the copy is rebuilt automatically.
- hides home menu entries that would only open empty pages (movies, TV shows, music videos
  without a library, TV and radio without a PVR add-on, games, weather without a provider).
- turns on "prefer audio description", turns off the mouse and the ".." list entry,
  and uses the German keyboard layout when Kodi runs in German.
- adds the free live streams of the German public broadcasters (19 TV, 15 radio stations)
  through IPTV Simple. The list is loaded daily from
  `service.accessibility.setup/resources/channels/oeffentlich-rechtlich.m3u` in this repository,
  so fixing a stream there updates every installation. Check the streams with
  `python3 tools/check_streams.py` (from a German connection, most streams are geo-blocked).
- adds favourites for installed streaming add-ons (MediathekView, ARD, ZDF, Joyn, YouTube,
  Netflix, Amazon, radio.de, podcasts, Deutschlandfunk, WDR Audiothek).

Every step runs once; changes made by the user afterwards are kept. Steps can be turned off
in the add-on settings, and the whole setup can be run again from Add-ons > Program add-ons.
