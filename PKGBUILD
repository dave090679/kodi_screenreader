# Maintainer: Dave <dave090679@users.noreply.github.com>
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

pkgname=kodi_screenreader
pkgver="$(python3 "$repo_root/packaging/addon_version.py")"
pkgrel=1
pkgdesc="Screenreader addon for Kodi media center with TTS and NVDA support"
arch=('any')
url="https://github.com/dave090679/kodi_screenreader"
license=('GPL2' 'LGPL2.1')
depends=('kodi' 'python3' 'speech-dispatcher' 'espeak-ng')
source=()
sha256sums=()

prepare() {
    # No preparation needed
}

build() {
    # No build required for Python addon
}

package() {
    bash "$repo_root/packaging/install-addon-tree.sh" "${pkgdir}"

    # Install license files
    install -Dm644 "$repo_root/LICENSE" "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
}
