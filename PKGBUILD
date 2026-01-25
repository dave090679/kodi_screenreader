# Maintainer: Dave <dave090679@users.noreply.github.com>
<<<<<<< HEAD
pkgname=kodi_screenreader
pkgver=1.0.r2.gb15d75f
=======
pkgname=kodi-screenreader
pkgver=1.0.0
>>>>>>> 38434a2a81841b2544124396633fa04a01bba2ec
pkgrel=1
pkgdesc="Screenreader addon for Kodi media center with TTS and NVDA support"
arch=('any')
url="https://github.com/dave090679/kodi_screenreader"
license=('GPL2' 'LGPL2.1')
depends=('kodi' 'python')
makedepends=('git')
source=("git+https://github.com/dave090679/kodi_screenreader.git")
md5sums=('SKIP')
<<<<<<< HEAD
install=kodi_screenreader.install
=======

>>>>>>> 38434a2a81841b2544124396633fa04a01bba2ec
pkgver() {
    cd "$pkgname"
    git describe --long --tags 2>/dev/null | sed 's/v//g;s/-/.r/;s/-/./' || echo "1.0.0"
}

prepare() {
    cd "$pkgname"
    # No preparation needed
}

build() {
    # No build required for Python addon
    cd "$pkgname"
}

package() {
<<<<<<< HEAD
    # cd "$pkgname"
=======
    cd "$pkgname"
>>>>>>> 38434a2a81841b2544124396633fa04a01bba2ec
    
    # Install addon directories to system Kodi addons path
    install -dm755 "${pkgdir}/usr/share/kodi/addons"
    
    # Install service.xbmc.tts
<<<<<<< HEAD
      cp -rv service.xbmc.tts "${pkgdir}/usr/share/kodi/addons/"
    # Install keyboard mappings
    install -dm755 "${pkgdir}/etc/kodi/userdata/keymaps"
       install -Dm644 service.xbmc.tts.keyboard.xml \
            "${pkgdir}/etc/kodi/userdata/keymaps/service.xbmc.tts.keyboard.xml"
    # Install addon activation flag
    install -dm755 "${pkgdir}/etc/kodi/userdata/addon_data/service.xbmc.tts"
      install -Dm644 ENABLED \
            "${pkgdir}/etc/kodi/userdata/addon_data/service.xbmc.tts/ENABLED"
=======
    if [ -d "service.xbmc.tts" ]; then
        cp -r service.xbmc.tts "${pkgdir}/usr/share/kodi/addons/"
    fi
    
    # Install repository addon
    if [ -d "ruuk.addon.repository" ]; then
        cp -r ruuk.addon.repository "${pkgdir}/usr/share/kodi/addons/"
    fi
    
    # Install NVDA controller client module
    if [ -d "script.module.nvdacontrollerclient" ]; then
        cp -r script.module.nvdacontrollerclient "${pkgdir}/usr/share/kodi/addons/"
    fi
    
    # Install keyboard mappings
    install -dm755 "${pkgdir}/etc/kodi/userdata/keymaps"
    if [ -f "service.xbmc.tts.keyboard.xml" ]; then
        install -Dm644 service.xbmc.tts.keyboard.xml \
            "${pkgdir}/etc/kodi/userdata/keymaps/service.xbmc.tts.keyboard.xml"
    fi
    
    # Install addon activation flag
    install -dm755 "${pkgdir}/etc/kodi/userdata/addon_data/service.xbmc.tts"
    if [ -f "ENABLED" ]; then
        install -Dm644 ENABLED \
            "${pkgdir}/etc/kodi/userdata/addon_data/service.xbmc.tts/ENABLED"
    fi
    
    # Install license files
    install -Dm644 LICENSE "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
    
    if [ -f "script.module.nvdacontrollerclient/LICENSE.txt" ]; then
        install -Dm644 script.module.nvdacontrollerclient/LICENSE.txt \
            "${pkgdir}/usr/share/licenses/${pkgname}/NVDA-LICENSE"
    fi
>>>>>>> 38434a2a81841b2544124396633fa04a01bba2ec
}
