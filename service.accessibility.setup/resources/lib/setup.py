# -*- coding: utf-8 -*-
"""Sets up Kodi for screen reader users.

Every step is versioned in state.json and runs only once (or again after its
version is raised), so changes the user makes afterwards are kept. The only
step that runs on every start is keeping the accessible skin copy in sync with
Kodi's bundled Estuary.
"""
import json
import os
import re
import shutil
import urllib.request

import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

ADDON = xbmcaddon.Addon('service.accessibility.setup')
ADDON_ID = ADDON.getAddonInfo('id')
PROFILE = xbmcvfs.translatePath(ADDON.getAddonInfo('profile'))
STATE_FILE = os.path.join(PROFILE, 'state.json')

SKIN_ID = 'skin.estuary.barrierefrei'
SKIN_NAME = 'Estuary barrierefrei'
SOURCE_SKIN = xbmcvfs.translatePath('special://xbmc/addons/skin.estuary')
TARGET_SKIN = xbmcvfs.translatePath('special://home/addons/' + SKIN_ID)
SKIN_MARKER = os.path.join(TARGET_SKIN, '.barrierefrei')
# Raise when the patches applied to the skin copy change
SKIN_PATCH_VERSION = 1

CHANNEL_INSTANCE_NAME = 'Öffentlich-rechtliche Sender (Barrierefreie Einrichtung)'
BUNDLED_CHANNELS = os.path.join(xbmcvfs.translatePath(ADDON.getAddonInfo('path')),
                                'resources', 'channels', 'oeffentlich-rechtlich.m3u')

# Step name -> version. Raise a version to run that step once more after an update.
STEPS = {
    'gui_settings': 1,
    'skin_settings': 1,
    'channels': 1,
    'favourites': 1,
}

# Streaming add-ons that get a favourite when installed: (add-on id, window, title)
FAVOURITE_ADDONS = [
    ('plugin.video.mediathekview', 'videos', 'MediathekView'),
    ('plugin.video.ardmediathek_de', 'videos', 'ARD Mediathek'),
    ('plugin.video.zdf_de_lite', 'videos', 'ZDF Mediathek'),
    ('plugin.video.joyn', 'videos', 'Joyn (ProSieben, Sat.1)'),
    ('plugin.video.youtube', 'videos', 'YouTube'),
    ('plugin.video.netflix', 'videos', 'Netflix'),
    ('plugin.video.amazon-test', 'videos', 'Amazon Prime Video'),
    ('plugin.audio.radio_de', 'music', 'Radio'),
    ('plugin.audio.podcasts', 'music', 'Podcasts'),
    ('plugin.audio.deutschlandfunk', 'music', 'Deutschlandfunk'),
    ('plugin.audio.wdraudiothek', 'music', 'WDR Audiothek'),
]


def log(msg, level=xbmc.LOGINFO):
    xbmc.log('[{0}] {1}'.format(ADDON_ID, msg), level)


def T(string_id):
    return ADDON.getLocalizedString(string_id)


def rpc(method, **params):
    request = {'jsonrpc': '2.0', 'id': 1, 'method': method}
    if params:
        request['params'] = params
    response = json.loads(xbmc.executeJSONRPC(json.dumps(request)))
    if 'error' in response:
        log('{0} failed: {1}'.format(method, response['error']), xbmc.LOGWARNING)
        return None
    return response.get('result')


def wait_for(condition, timeout=10.0):
    monitor = xbmc.Monitor()
    waited = 0.0
    while not condition():
        if waited >= timeout or monitor.waitForAbort(0.25):
            return False
        waited += 0.25
    return True


def setting_enabled(setting_id):
    return ADDON.getSettingBool(setting_id)


# --- state -------------------------------------------------------------------

def load_state():
    try:
        with open(STATE_FILE, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def save_state(state):
    os.makedirs(PROFILE, exist_ok=True)
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2)


# --- add-on helpers ----------------------------------------------------------

def addon_installed(addon_id):
    return rpc('Addons.GetAddonDetails', addonid=addon_id, properties=['enabled']) is not None


def addon_enabled(addon_id):
    result = rpc('Addons.GetAddonDetails', addonid=addon_id, properties=['enabled'])
    return bool(result and result['addon'].get('enabled'))


def get_setting(setting_id):
    result = rpc('Settings.GetSettingValue', setting=setting_id)
    return result['value'] if result else None


def set_setting(setting_id, value):
    if get_setting(setting_id) == value:
        return
    rpc('Settings.SetSettingValue', setting=setting_id, value=value)
    log('setting {0} = {1}'.format(setting_id, value))


# --- skin --------------------------------------------------------------------

def _addon_version(addon_dir):
    with open(os.path.join(addon_dir, 'addon.xml'), encoding='utf-8') as f:
        match = re.search(r'<addon[^>]*\sversion="([^"]+)"', f.read())
    return match.group(1) if match else ''


def _skin_marker():
    return '{0}/{1}'.format(_addon_version(SOURCE_SKIN), SKIN_PATCH_VERSION)


def _patch_skin(skin_dir):
    """Applies the accessibility patches. Returns False if the skin changed too much."""
    addon_xml = os.path.join(skin_dir, 'addon.xml')
    with open(addon_xml, encoding='utf-8') as f:
        text = f.read()
    text, n = re.subn(r'<addon id="skin\.estuary"', '<addon id="{0}"'.format(SKIN_ID), text, count=1)
    text = re.sub(r'(<addon id="{0}"[^>]*\sname=")[^"]*'.format(re.escape(SKIN_ID)), r'\g<1>' + SKIN_NAME, text, count=1)
    if n != 1:
        return False
    with open(addon_xml, 'w', encoding='utf-8') as f:
        f.write(text)

    # Home menu: Right arrow jumps from the main menu into the widget row next to it.
    # Screen reader users get lost there, so the menu is only left with Enter.
    home_xml = os.path.join(skin_dir, 'xml', 'Home.xml')
    with open(home_xml, encoding='utf-8') as f:
        text = f.read()
    text, n = re.subn(r'\s*<onright>SetFocus\(\$INFO\[Container\(9000\)\.ListItem\.Property\(menu_id\)\]\)</onright>',
                      '', text)
    if n != 1:
        return False
    with open(home_xml, 'w', encoding='utf-8') as f:
        f.write(text)
    return True


def ensure_skin_copy():
    """Creates or refreshes the patched copy of Estuary. Returns True if files changed."""
    marker = _skin_marker()
    try:
        with open(SKIN_MARKER, encoding='utf-8') as f:
            if f.read().strip() == marker:
                return False
    except OSError:
        pass

    staging = TARGET_SKIN + '.new'
    shutil.rmtree(staging, ignore_errors=True)
    shutil.copytree(SOURCE_SKIN, staging)
    if not _patch_skin(staging):
        shutil.rmtree(staging, ignore_errors=True)
        log('Estuary has changed, the skin patches no longer apply. Keeping the existing copy.', xbmc.LOGWARNING)
        return False
    with open(os.path.join(staging, '.barrierefrei'), 'w', encoding='utf-8') as f:
        f.write(marker)
    shutil.rmtree(TARGET_SKIN, ignore_errors=True)
    os.rename(staging, TARGET_SKIN)
    log('skin copy created from Estuary ' + marker)
    return True


def activate_skin(files_changed):
    xbmc.executebuiltin('UpdateLocalAddons', True)
    if not wait_for(lambda: addon_installed(SKIN_ID)):
        log('skin copy was not registered by Kodi', xbmc.LOGWARNING)
        return False
    if not addon_enabled(SKIN_ID):
        rpc('Addons.SetAddonEnabled', addonid=SKIN_ID, enabled=True)

    if xbmc.getSkinDir() == SKIN_ID:
        if files_changed:
            xbmc.executebuiltin('ReloadSkin()')
        return True

    rpc('Settings.SetSettingValue', setting='lookandfeel.skin', value=SKIN_ID)
    # Kodi asks whether to keep the new skin and reverts after a timeout; confirm it.
    if wait_for(lambda: xbmc.getCondVisibility('Window.IsActive(yesnodialog)'), 15):
        xbmc.executebuiltin('SendClick(yesnodialog,11)')
    return wait_for(lambda: xbmc.getSkinDir() == SKIN_ID, 15)


def _library_count(method):
    result = rpc(method, limits={'start': 0, 'end': 1})
    return (result or {}).get('limits', {}).get('total', 0)


def _has_sources(media):
    result = rpc('Files.GetSources', media=media)
    return bool(result and result.get('sources'))


def _pvr_enabled():
    result = rpc('Addons.GetAddons', type='kodi.pvrclient', enabled=True)
    return bool(result and result.get('addons'))


def apply_skin_settings():
    """Hides home menu entries that would only lead to empty pages."""
    hide = {
        'HomeMenuNoMovieButton': _library_count('VideoLibrary.GetMovies') == 0,
        'HomeMenuNoTVShowButton': _library_count('VideoLibrary.GetTVShows') == 0,
        'HomeMenuNoMusicVideoButton': _library_count('VideoLibrary.GetMusicVideos') == 0,
        'HomeMenuNoPicturesButton': not _has_sources('pictures'),
        'HomeMenuNoGamesButton': True,
        'HomeMenuNoWeatherButton': not get_setting('weather.addon'),
        'HomeMenuNoTVButton': not _pvr_enabled(),
        'HomeMenuNoRadioButton': not _pvr_enabled(),
        'no_slide_animations': True,
        'home_no_categories_widget': True,
    }
    for name, value in hide.items():
        xbmc.executebuiltin('Skin.SetBool({0})'.format(name) if value else 'Skin.Reset({0})'.format(name))
    log('home menu: ' + ', '.join(n for n, v in hide.items() if v))


# --- Kodi settings -----------------------------------------------------------

def apply_gui_settings():
    set_setting('accessibility.audiovisual', True)   # prefer audio description
    set_setting('input.enablemouse', False)          # touchpad touches no longer move the focus
    set_setting('filelists.showparentdiritems', False)  # no ".." entry at the top of every list
    set_setting('locale.audiolanguage', 'default')   # audio track in the interface language
    if get_setting('locale.language') == 'resource.language.de_de':
        set_setting('locale.keyboardlayouts', ['German QWERTZ', 'English QWERTY'])
        set_setting('locale.activekeyboardlayout', 'German QWERTZ')


# --- live TV and radio -------------------------------------------------------

def _url_reachable(url):
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'Kodi'})
        with urllib.request.urlopen(request, timeout=15) as response:
            return response.read(7) == b'#EXTM3U'
    except Exception:
        return False


def _xml_escape(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def setup_channels():
    """Adds an IPTV Simple instance with the public broadcasters' free live streams."""
    if not addon_installed('pvr.iptvsimple'):
        xbmc.executebuiltin('InstallAddon(pvr.iptvsimple)', True)
        if not wait_for(lambda: addon_installed('pvr.iptvsimple'), 120):
            log('pvr.iptvsimple not installed, skipping channels', xbmc.LOGWARNING)
            return False

    data_dir = xbmcvfs.translatePath('special://profile/addon_data/pvr.iptvsimple')
    os.makedirs(data_dir, exist_ok=True)
    instances = [f for f in os.listdir(data_dir) if re.match(r'instance-settings-\d+\.xml$', f)]
    unconfigured = None
    for name in instances:
        with open(os.path.join(data_dir, name), encoding='utf-8') as f:
            content = f.read()
        if CHANNEL_INSTANCE_NAME in content:
            log('channel instance already present: ' + name)
            return True
        # Kodi creates an empty default instance ("Migrated Add-on Config"); reuse it
        if not re.search(r'<setting id="(m3uPath|m3uUrl)"[^>]*>[^<]+</setting>', content):
            unconfigured = name

    url = ADDON.getSetting('channel_list_url')
    if url and _url_reachable(url):
        source = '    <setting id="m3uPathType">1</setting>\n' \
                 '    <setting id="m3uUrl">{0}</setting>\n' \
                 '    <setting id="m3uRefreshMode">2</setting>\n'.format(_xml_escape(url))
    else:
        log('channel list URL not reachable, using the bundled list')
        source = '    <setting id="m3uPathType">0</setting>\n' \
                 '    <setting id="m3uPath">{0}</setting>\n'.format(_xml_escape(BUNDLED_CHANNELS))

    if unconfigured:
        instance_file = os.path.join(data_dir, unconfigured)
    else:
        numbers = [int(re.search(r'\d+', n).group()) for n in instances]
        instance_file = os.path.join(data_dir, 'instance-settings-{0}.xml'.format(max(numbers + [0]) + 1))
    with open(instance_file, 'w', encoding='utf-8') as f:
        f.write('<settings version="2">\n'
                '    <setting id="kodi_addon_instance_name">{0}</setting>\n'
                '    <setting id="kodi_addon_instance_enabled">true</setting>\n'
                '{1}'
                '</settings>\n'.format(_xml_escape(CHANNEL_INSTANCE_NAME), source))
    log('channel instance written: ' + instance_file)

    # Restart the add-on so it picks up the new instance
    rpc('Addons.SetAddonEnabled', addonid='pvr.iptvsimple', enabled=False)
    xbmc.sleep(1000)
    rpc('Addons.SetAddonEnabled', addonid='pvr.iptvsimple', enabled=True)
    return True


# --- favourites --------------------------------------------------------------

def add_favourites():
    """Adds favourites for installed streaming add-ons. Existing favourites are kept."""
    result = rpc('Favourites.GetFavourites', properties=['windowparameter'])
    existing = {f.get('windowparameter') for f in (result or {}).get('favourites') or []}
    added = []
    for addon_id, window, title in FAVOURITE_ADDONS:
        path = 'plugin://{0}/'.format(addon_id)
        if path in existing or not addon_installed(addon_id):
            continue
        # AddFavourite toggles, so it must only be called for missing entries
        rpc('Favourites.AddFavourite', title=title, type='window', window=window, windowparameter=path,
            thumbnail='special://home/addons/{0}/icon.png'.format(addon_id))
        added.append(title)
    log('favourites added: ' + ', '.join(added))
    return added


# --- main --------------------------------------------------------------------

def run(force=False):
    state = {} if force else load_state()
    done = []

    if setting_enabled('manage_skin'):
        try:
            changed = ensure_skin_copy()
            if activate_skin(changed):
                if state.get('skin_settings', 0) < STEPS['skin_settings']:
                    apply_skin_settings()
                    state['skin_settings'] = STEPS['skin_settings']
                    done.append(T(30100))
        except Exception as e:
            log('skin step failed: {0}'.format(e), xbmc.LOGERROR)

    steps = [
        ('gui_settings', 'apply_settings', apply_gui_settings, 30101),
        ('channels', 'setup_channels', setup_channels, 30102),
        ('favourites', 'add_favourites', add_favourites, 30103),
    ]
    for step, setting_id, func, label in steps:
        if not setting_enabled(setting_id) or state.get(step, 0) >= STEPS[step]:
            continue
        try:
            if func() is not False:
                state[step] = STEPS[step]
                done.append(T(label))
        except Exception as e:
            log('{0} failed: {1}'.format(step, e), xbmc.LOGERROR)

    save_state(state)
    if done:
        xbmcgui.Dialog().ok(T(30000), T(30104) + '\n' + '\n'.join(done))
    return done
