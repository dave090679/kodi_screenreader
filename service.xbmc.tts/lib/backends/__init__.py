# -*- coding: utf-8 -*-
import importlib
import os
import sys

sys.path.insert(0,os.path.dirname(__file__))

from lib import util


def _load_backend(module_name, *class_names):
    try:
        module = importlib.import_module(module_name)
    except Exception as exc:
        util.LOG('Skipping backend module {0}: {1}: {2}'.format(module_name, exc.__class__.__name__, exc))
        for class_name in class_names:
            globals()[class_name] = None
        return

    for class_name in class_names:
        globals()[class_name] = getattr(module, class_name, None)


audio = importlib.import_module('audio')

_load_backend('base', 'LogOnlyTTSBackend')
_load_backend('nvda', 'NVDATTSBackend')
_load_backend('festival', 'FestivalTTSBackend')
_load_backend('pico2wave', 'Pico2WaveTTSBackend')
_load_backend('flite', 'FliteTTSBackend')
_load_backend('osxsay', 'OSXSayTTSBackend')
_load_backend('sapi', 'SAPITTSBackend')
_load_backend('espeak', 'ESpeakTTSBackend', 'ESpeakCtypesTTSBackend')
_load_backend('speechdispatcher', 'SpeechDispatcherTTSBackend')
_load_backend('jaws', 'JAWSTTSBackend')
_load_backend('speech_server', 'SpeechServerBackend')
_load_backend('cepstral', 'CepstralTTSBackend')
_load_backend('recite', 'ReciteTTSBackend')
_load_backend('termux', 'TermuxTTSBackend')


def _defined(*backend_classes):
    return [backend_class for backend_class in backend_classes if backend_class]


backendsByPriority = _defined(
    SAPITTSBackend,
    OSXSayTTSBackend,
    TermuxTTSBackend,
    SpeechDispatcherTTSBackend,
    ESpeakTTSBackend,
    JAWSTTSBackend,
    NVDATTSBackend,
    FliteTTSBackend,
    Pico2WaveTTSBackend,
    FestivalTTSBackend,
    CepstralTTSBackend,
    SpeechServerBackend,
    ReciteTTSBackend,
    ESpeakCtypesTTSBackend,
    LogOnlyTTSBackend,
)

def removeBackendsByProvider(to_remove):
    rem = []
    for b in backendsByPriority:
        if b.provider in to_remove:
            rem.append(b)
    for r in rem: backendsByPriority.remove(r)

def getAvailableBackends(can_stream_wav=False):
    available = []
    for b in backendsByPriority:
        if not b._available(): continue
        if can_stream_wav and not b.canStreamWav: continue
        available.append(b)
    return available

def getBackendFallback():
    if util.isATV2() and FliteTTSBackend:
        return FliteTTSBackend
    elif util.isWindows() and SAPITTSBackend:
        return SAPITTSBackend
    elif util.isOSX() and OSXSayTTSBackend:
        return OSXSayTTSBackend
    elif util.isOpenElec() and ESpeakTTSBackend:
        return ESpeakTTSBackend
    for b in backendsByPriority:
        if b._available(): return b
    return None

def getVoices(provider):
    voices = None
    bClass = getBackendByProvider(provider)
    if bClass:
        voices = bClass.voices()
    return voices

def getLanguages(provider):
    languages = None
    bClass = getBackendByProvider(provider)
    if bClass:
        with bClass() as b: languages = b.languages()
    return languages

def getSettingsList(provider,setting,*args):
    settings = None
    bClass = getBackendByProvider(provider)
    if bClass:
        settings = bClass.settingList(setting,*args)
    return settings

def getPlayers(provider):
    players = None
    bClass = getBackendByProvider(provider)
    if bClass and hasattr(bClass,'players'):
        players = bClass.players()
    return players

def getBackend(provider='auto'):
    provider = util.getSetting('backend') or provider
    b = getBackendByProvider(provider)
    if not b or not b._available():
         for b in backendsByPriority:
            if b._available(): break
    return b

def getWavStreamBackend(provider='auto'):
    b = getBackendByProvider(provider)
    if not b or not b._available() or not b.canStreamWav:
         for b in backendsByPriority:
            if b._available() and b.canStreamWav: break
    return b

def getBackendByProvider(name):
    if name == 'auto': return None
    for b in backendsByPriority:
        if b.provider == name and b._available():
            return b
    return None
