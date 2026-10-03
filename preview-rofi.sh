#!/bin/bash
# Screenshot a theme's rofi launcher over its e16 desktop, headless and isolated.
#   ./preview-rofi.sh Umbreon      -> build/.preview/<Theme>-rofi.png
set -eu
cd "$(dirname "$0")"
THEME=$1
DISP=:${PREVIEW_DISPLAY:-77}
WORK=build/.preview/$THEME-rofi
rm -rf "$WORK"; mkdir -p "$WORK/conf/themes" "$WORK/cache"
ln -s "$PWD/build/$THEME" "$WORK/conf/themes/$THEME"

pids=()
cleanup() { kill "${pids[@]}" 2>/dev/null || true; wait 2>/dev/null || true; }
trap cleanup EXIT

Xvfb "$DISP" -screen 0 1280x800x24 -nolisten tcp >/dev/null 2>&1 & pids+=($!)
sleep 1
export DISPLAY=$DISP
export XDG_RUNTIME_DIR=$PWD/$WORK/run   # own rofi lock file, never the real session's
mkdir -p -m 700 "$XDG_RUNTIME_DIR"
e16 -P "$WORK/conf" -Q "$WORK/cache" -t "$THEME" >/dev/null 2>&1 & pids+=($!)
sleep 3
for w in $(eesh wl | awk '$3=="Message" {print $1}'); do eesh wop "$w" close >/dev/null; done

# A fixed list so every screenshot is comparable; the filter shows the counter.
printf '%s\n' Firefox Terminal "Text Editor" "File Manager" Calculator "Image Viewer" \
    "Music Player" Settings "System Monitor" "Screenshot Tool" Mail Calendar |
    rofi -no-config -dmenu -i -p run -filter e -selected-row 1 -theme "$PWD/build/$THEME/rofi/$THEME.rasi" \
    >/dev/null 2>"$WORK/rofi.log" & pids+=($!)
sleep 1.5
xwd -root -silent | ffmpeg -loglevel error -y -f xwd_pipe -i - "build/.preview/$THEME-rofi.png"
echo "build/.preview/$THEME-rofi.png"
