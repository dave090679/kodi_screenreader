# Maintainer: Dave <dave090679@users.noreply.github.com>
pkgname=kodi_screenreader
pkgver=1.0.r2.gb15d75f
pkgrel=1
pkgdesc="Screenreader addon for Kodi media center with TTS and NVDA support"
arch=('any')
url="https://github.com/dave090679/kodi_screenreader"
license=('GPL2' 'LGPL2.1')
depends=('kodi' 'python')
makedepends=('git')
source=("git+https://github.com/dave090679/kodi_screenreader.git")
md5sums=('SKIP')
install=kodi_screenreader.install
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
    # cd "$pkgname"
    
    # Install addon directories to system Kodi addons path
    install -dm755 "${pkgdir}/usr/share/kodi/addons"
    
    # Install service.xbmc.tts
      cp -rv service.xbmc.tts "${pkgdir}/usr/share/kodi/addons/"
    # Install keyboard mappings
    install -dm755 "${pkgdir}/etc/kodi/userdata/keymaps"
       install -Dm644 service.xbmc.tts.keyboard.xml \
            "${pkgdir}/etc/kodi/userdata/keymaps/service.xbmc.tts.keyboard.xml"
    # Install addon activation flag
    install -dm755 "${pkgdir}/etc/kodi/userdata/addon_data/service.xbmc.tts"
      install -Dm644 ENABLED \
            "${pkgdir}/etc/kodi/userdata/addon_data/service.xbmc.tts/ENABLED"
}
