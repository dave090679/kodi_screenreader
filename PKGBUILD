# Maintainer: Dave <dave090679@users.noreply.github.com>
pkgname=kodi-screenreader
pkgver=1.0.0
pkgrel=1
pkgdesc="Screenreader addon for Kodi media center with TTS and NVDA support"
arch=('any')
url="https://github.com/dave090679/kodi_screenreader"
license=('GPL2' 'LGPL2.1')
depends=('kodi' 'python')
makedepends=('git')
source=("git+https://github.com/dave090679/kodi_screenreader.git")
md5sums=('SKIP')

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
    cd "$pkgname"
    
    # Install addon directories to system Kodi addons path
    install -dm755 "${pkgdir}/usr/share/kodi/addons"
    
    # Install service.xbmc.tts
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
}
