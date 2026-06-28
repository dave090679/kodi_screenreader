# -*- coding: utf-8 -*-
import xbmc,binascii

BASE_COMMAND = 'XBMC.NotifyAll(service.xbmc.tts,SAY,"{{\\"text\\":\\"{0}\\",\\"interrupt\\":{1}}}")'

def safeEncode(text):
    return binascii.hexlify(text)

def safeDecode(enc_text):
    return binascii.unhexlify(enc_text)

def sayText(text,interrupt=False):
    assert isinstance(text,str), "Not Unicode"
    command = BASE_COMMAND.format(safeEncode(text),repr(interrupt).lower())
    #print command
    xbmc.executebuiltin(command)

def stop():
    xbmc.executebuiltin('XBMC.NotifyAll(service.xbmc.tts,STOP)')
