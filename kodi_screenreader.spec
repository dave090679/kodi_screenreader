%global repo_root %(pwd)
%global _sourcedir %{repo_root}

Name:           kodi_screenreader
Version:        1.0.8
Release:        1%{?dist}
Summary:        Screenreader addon for Kodi media center with TTS and NVDA support

License:        GPL-2.0-only AND LGPL-2.1-only
URL:            https://github.com/dave090679/kodi_screenreader
BuildArch:      noarch

Requires:       kodi python3

%description
Screenreader addon for the Kodi media center providing text-to-speech
functionality and NVDA controller client integration.

%prep
%setup -q -c -T
cp -a %{_sourcedir}/LICENSE .

%build
# No build required (Kodi addon is interpreted Python + assets)

%install
install -dm755 %{buildroot}%{_datadir}/kodi/addons/service.xbmc.tts
cp -a %{_sourcedir}/service.xbmc.tts/. %{buildroot}%{_datadir}/kodi/addons/service.xbmc.tts/

install -Dm644 %{_sourcedir}/service.xbmc.tts.keyboard.xml \
    %{buildroot}%{_sysconfdir}/kodi/userdata/keymaps/service.xbmc.tts.keyboard.xml

install -Dm644 %{_sourcedir}/ENABLED \
    %{buildroot}%{_sysconfdir}/kodi/userdata/addon_data/service.xbmc.tts/ENABLED

%post
get_logged_in_users() {
    USERS=$(loginctl list-users --no-legend 2>/dev/null | awk '{print $1}')
    [ -z "$USERS" ] && USERS=$(who | awk '{print $1}')
    echo "$USERS"
}

for USER in $(get_logged_in_users); do
    [ "$USER" = "root" ] && continue

    USER_HOME=$(getent passwd "$USER" | cut -d: -f6)
    [ -z "$USER_HOME" ] && continue

    KODI_DIR="$USER_HOME/.kodi"

    mkdir -p "$KODI_DIR/addons"
    mkdir -p "$KODI_DIR/userdata/keymaps"
    mkdir -p "$KODI_DIR/userdata/addon_data/service.xbmc.tts"

    cp -r "/usr/share/kodi/addons/service.xbmc.tts" "$KODI_DIR/addons/" 2>/dev/null || true
    cp -f "/etc/kodi/userdata/keymaps/service.xbmc.tts.keyboard.xml" \
          "$KODI_DIR/userdata/keymaps/" 2>/dev/null || true
    cp -f "/etc/kodi/userdata/addon_data/service.xbmc.tts/ENABLED" \
          "$KODI_DIR/userdata/addon_data/service.xbmc.tts/" 2>/dev/null || true

    chown -R "$USER:$USER" "$KODI_DIR" 2>/dev/null || true
done

exit 0

%triggerin -- %{name}
get_logged_in_users() {
    USERS=$(loginctl list-users --no-legend 2>/dev/null | awk '{print $1}')
    [ -z "$USERS" ] && USERS=$(who | awk '{print $1}')
    echo "$USERS"
}

for USER in $(get_logged_in_users); do
    [ "$USER" = "root" ] && continue

    USER_HOME=$(getent passwd "$USER" | cut -d: -f6)
    [ -z "$USER_HOME" ] && continue

    KODI_DIR="$USER_HOME/.kodi"

    mkdir -p "$KODI_DIR/addons"
    mkdir -p "$KODI_DIR/userdata/keymaps"
    mkdir -p "$KODI_DIR/userdata/addon_data/service.xbmc.tts"

    cp -r "/usr/share/kodi/addons/service.xbmc.tts" "$KODI_DIR/addons/" 2>/dev/null || true
    cp -f "/etc/kodi/userdata/keymaps/service.xbmc.tts.keyboard.xml" \
          "$KODI_DIR/userdata/keymaps/" 2>/dev/null || true
    cp -f "/etc/kodi/userdata/addon_data/service.xbmc.tts/ENABLED" \
          "$KODI_DIR/userdata/addon_data/service.xbmc.tts/" 2>/dev/null || true

    chown -R "$USER:$USER" "$KODI_DIR" 2>/dev/null || true
done

exit 0

%postun
if [ $1 -eq 0 ]; then
    get_logged_in_users() {
        USERS=$(loginctl list-users --no-legend 2>/dev/null | awk '{print $1}')
        [ -z "$USERS" ] && USERS=$(who | awk '{print $1}')
        echo "$USERS"
    }

    for USER in $(get_logged_in_users); do
        [ "$USER" = "root" ] && continue

        USER_HOME=$(getent passwd "$USER" | cut -d: -f6)
        [ -z "$USER_HOME" ] && continue

        KODI_DIR="$USER_HOME/.kodi"

        rm -rf "$KODI_DIR/addons/service.xbmc.tts" 2>/dev/null || true
        rm -f "$KODI_DIR/userdata/keymaps/service.xbmc.tts.keyboard.xml" 2>/dev/null || true
        rm -rf "$KODI_DIR/userdata/addon_data/service.xbmc.tts" 2>/dev/null || true
    done
fi

exit 0

%triggerun -- %{name}
get_logged_in_users() {
    USERS=$(loginctl list-users --no-legend 2>/dev/null | awk '{print $1}')
    [ -z "$USERS" ] && USERS=$(who | awk '{print $1}')
    echo "$USERS"
}

for USER in $(get_logged_in_users); do
    [ "$USER" = "root" ] && continue

    USER_HOME=$(getent passwd "$USER" | cut -d: -f6)
    [ -z "$USER_HOME" ] && continue

    KODI_DIR="$USER_HOME/.kodi"

    rm -rf "$KODI_DIR/addons/service.xbmc.tts" 2>/dev/null || true
    rm -f "$KODI_DIR/userdata/keymaps/service.xbmc.tts.keyboard.xml" 2>/dev/null || true
    rm -rf "$KODI_DIR/userdata/addon_data/service.xbmc.tts" 2>/dev/null || true
done

exit 0

%files
%license LICENSE
%{_datadir}/kodi/addons/service.xbmc.tts
%{_sysconfdir}/kodi/userdata/keymaps/service.xbmc.tts.keyboard.xml
%{_sysconfdir}/kodi/userdata/addon_data/service.xbmc.tts/ENABLED

%changelog
* Sun Jun 28 2026 Dave <dave090679@users.noreply.github.com> - 1.0.8-1
- Build RPMs directly from the repository checkout
