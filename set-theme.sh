#!/bin/bash
# Switch e16, rofi, GTK3 and Qt/KDE to one of the themes together.
#   ./set-theme.sh Umbreon               everything
#   ./set-theme.sh Umbreon gtk qt        just the parts named (e16 rofi gtk qt ytm polybar)
#
# GTK: the running xsettingsd overrides settings.ini, so both are updated and
# xsettingsd is told to reload; running GTK apps restyle immediately.
# (KDE's System Settings rewrites these files if you change GTK settings there.)
# Qt: applies the KDE colour scheme to ~/.config/kdeglobals; KDE apps (incl.
# Flatpaks) pick it up live.  Other Qt apps also need QT_QPA_PLATFORMTHEME=kde
# in the session environment.
# ytm: points Pear Desktop (YouTube Music) at the theme's CSS; restart Pear to
# apply.  Done while Pear is closed, since it rewrites its config on exit.
# polybar: relinks ~/.config/polybar/theme.ini and restarts the running bar.
set -eu
NAME=${1:?usage: $0 <Theme> [e16] [rofi] [gtk] [qt] [ytm] [polybar]}
shift
PARTS=${*:-e16 rofi gtk qt ytm polybar}

[ -d "$HOME/.e16/themes/$NAME" ] || { echo "no such theme: $NAME" >&2; exit 1; }

for part in $PARTS; do
    case $part in
    e16)
        eesh theme use "$NAME" && echo "e16:  $NAME" ;;
    rofi)
        cfg=$HOME/.config/rofi/config.rasi
        if [ -f "$cfg" ] && grep -q '^@theme ' "$cfg"; then
            sed -i "s|^@theme .*|@theme \"$NAME\"|" "$cfg"
        else
            mkdir -p "$(dirname "$cfg")"; echo "@theme \"$NAME\"" >> "$cfg"
        fi
        echo "rofi: $NAME" ;;
    gtk)
        xs=$HOME/.config/xsettingsd/xsettingsd.conf
        if [ -f "$xs" ]; then
            if grep -q '^Net/ThemeName ' "$xs"; then
                sed -i "s|^Net/ThemeName .*|Net/ThemeName \"$NAME\"|" "$xs"
            else
                echo "Net/ThemeName \"$NAME\"" >> "$xs"
            fi
            pkill -HUP -x xsettingsd || true
        fi
        ini=$HOME/.config/gtk-3.0/settings.ini
        if [ -f "$ini" ] && grep -q '^gtk-theme-name=' "$ini"; then
            sed -i "s|^gtk-theme-name=.*|gtk-theme-name=$NAME|" "$ini"
        fi
        echo "gtk:  $NAME" ;;
    qt)
        plasma-apply-colorscheme "$NAME" >/dev/null && echo "qt:   $NAME" ;;
    ytm)
        pear="$HOME/.var/app/com.github.th_ch.youtube_music/config/YouTube Music"
        css="$pear/themes/$NAME.css"
        if [ ! -f "$css" ]; then
            echo "ytm:  skipped ($css missing; run ./build.py --install)"
        elif pgrep -f com.github.th_ch.youtube_music >/dev/null; then
            echo "ytm:  skipped (close YouTube Music first; it rewrites its config on exit)"
        else
            python3 - "$pear/config.json" "$css" <<'PY'
import json, sys
path, css = sys.argv[1:]
c = json.load(open(path))
c.setdefault("options", {})["themes"] = [css]
json.dump(c, open(path, "w"), indent=2)
PY
            echo "ytm:  $NAME"
        fi ;;
    polybar)
        ini=$HOME/.e16/themes/$NAME/polybar/$NAME.ini
        if [ -f "$ini" ] && [ -d "$HOME/.config/polybar" ]; then
            ln -sfn "$(readlink -f "$ini")" "$HOME/.config/polybar/theme.ini"
            pgrep -x polybar >/dev/null && polybar-msg cmd restart >/dev/null 2>&1 || true
            echo "polybar: $NAME"
        else
            echo "polybar: skipped (run polybar/setup.sh first)"
        fi ;;
    *)
        echo "unknown part: $part (use e16, rofi, gtk, qt, ytm, polybar)" >&2; exit 1 ;;
    esac
done
