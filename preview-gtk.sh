#!/bin/bash
# Screenshot a theme's GTK3 widgets over its e16 desktop, headless and isolated
# (own XDG config/data dirs: your GTK settings and KDE overrides aren't used).
#   ./preview-gtk.sh Umbreon   -> build/.preview/<Theme>-gtk.png
#
# Headless Xvfb doesn't show GTK popups in a root-window grab, so the tooltip
# is captured from its own window and pasted in at its position.
set -eu
cd "$(dirname "$0")"
THEME=$1
DISP=:${PREVIEW_DISPLAY:-77}
WORK=build/.preview/$THEME-gtk
OUT=build/.preview/$THEME-gtk.png
rm -rf "$WORK"; mkdir -p "$WORK/conf/themes" "$WORK/cache" "$WORK/data/themes" "$WORK/config/gtk-3.0"
ln -s "$PWD/build/$THEME" "$WORK/conf/themes/$THEME"
ln -s "$PWD/build/$THEME" "$WORK/data/themes/$THEME"
printf '[Settings]\ngtk-icon-theme-name=breeze\ngtk-font-name=Noto Sans 10\n' > "$WORK/config/gtk-3.0/settings.ini"

pids=()
cleanup() { kill "${pids[@]}" 2>/dev/null || true; wait 2>/dev/null || true; }
trap cleanup EXIT

Xvfb "$DISP" -screen 0 1280x800x24 -nolisten tcp >/dev/null 2>&1 & pids+=($!)
sleep 1
export DISPLAY=$DISP
e16 -P "$WORK/conf" -Q "$WORK/cache" -t "$THEME" >/dev/null 2>&1 & pids+=($!)
sleep 3
for w in $(eesh wl | awk '$3=="Message" {print $1}'); do eesh wop "$w" close >/dev/null; done

XDG_CONFIG_HOME=$PWD/$WORK/config XDG_DATA_HOME=$PWD/$WORK/data GTK_THEME=$THEME \
    python3 gtk-gallery.py --backdrop 2>"$WORK/gtk.log" & pids+=($!)
sleep 2
# rest the pointer on the "Hover me" button so its tooltip appears
eesh warp abs 515 160 >/dev/null; sleep 0.3; eesh warp abs 520 168 >/dev/null
sleep 2

xwd -root -silent | ffmpeg -loglevel error -y -f xwd_pipe -i - "$WORK/root.png"
tip=$(xwininfo -root -tree | awk '/"gtk-gallery.py": \("gtk-gallery.py" "Gtk-gallery.py"\)/ && $NF != "+0+0" {print $1, $NF; exit}')
if [ -n "$tip" ]; then
    set -- $tip; pos=${2#+}; x=${pos%%+*}; y=${pos#*+}
    xwd -id "$1" -silent | ffmpeg -loglevel error -y -f xwd_pipe -i - "$WORK/tip.png"
    ffmpeg -loglevel error -y -i "$WORK/root.png" -i "$WORK/tip.png" -filter_complex "[1]format=rgb24[t];[0][t]overlay=$x:$y" "$OUT"
else
    cp "$WORK/root.png" "$OUT"
fi
echo "$OUT"
grep -i -E 'theme parsing|error' "$WORK/gtk.log" | sort -u | head -20 || true
