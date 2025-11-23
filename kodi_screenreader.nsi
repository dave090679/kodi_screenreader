############################################################################################
#      NSIS Installation Script created by NSIS Quick Setup Script Generator v1.09.18
#               Entirely Edited with NullSoft Scriptable Installation System                
#              by Vlasis K. Barkas aka Red Wine red_wine@freemail.gr Sep 2006               
############################################################################################
!include x64.nsh
!define APP_NAME "kodi screenreader"
!define WEB_SITE "https://kodi.tv/"
!define VERSION "01.10.00.00"
!define INSTALLER_NAME "kodi_screenreader_1.1.exe"
!define INSTALL_TYPE "SetShellVarContext current"
######################################################################
AutoCloseWindow true
VIProductVersion  "${VERSION}"
VIAddVersionKey "ProductName"  "${APP_NAME}"
VIAddVersionKey "CompanyName"  "${COMP_NAME}"
VIAddVersionKey "LegalCopyright"  "${COPYRIGHT}"
VIAddVersionKey "FileDescription"  "${DESCRIPTION}"
VIAddVersionKey "FileVersion"  "${VERSION}"

######################################################################

SetCompressor ZLIB
Name "${APP_NAME}"
Caption "${APP_NAME}"
OutFile "${INSTALLER_NAME}"
BrandingText "${APP_NAME}"
XPStyle on
InstType "Minimal" IT_MIN
######################################################################

page instfiles
LoadLanguageFile "${NSISDIR}\Contrib\Language files\German.nlf"

######################################################################

######################################################################
; Define the main components section

sectiongroup "Basiskomponenten" 

  section "kodi screenreader" 
    sectioninsttype ${IT_MIN}
    setoutpath "$APPDATA\Kodi\addons\service.xbmc.tts"
    file /r "service.xbmc.tts\*.*"
    setoutpath "$APPDATA\Kodi\userdata\addon_data\service.xbmc.tts"
    file "ENABLED"
    setoutpath "$APPDATA\Kodi\userdata\keymaps"
    file "service.xbmc.tts.keyboard.xml"
  sectionend
sectiongroupend
Function .onInit
  ReadRegStr $0 HKCU "Software\Kodi" "Start Menu Folder"
  ${If} $0 == ""
    messagebox MB_OK "Kodi ist nicht installiert"
    quit
  ${EndIf}
  FindWindow $0 "" "Kodi"
  ${If} $0 != 0
    messagebox MB_OK "Kodi läuft noch. Beenden Sie es, bevor Sie den Screenreader installieren. Holen Sie das Fenster mit alttab in den Vordergrund und drücken Sie dann alt+F4, um Kodi zu schliießen."
    quit
  ${EndIf}
FunctionEnd

Function .onInstSuccess
  MessageBox MB_OK "Der Screenreader wurde erfolgreich installiert. Drücken Sie nach dem Start von Kodi F12, um ihn zu aktivieren."
FunctionEnd