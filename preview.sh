#!/bin/bash
# Screenshot a built theme in a headless, isolated e16 (does not touch ~/.e16).
#   ./preview.sh Umbreon [WxH]
# Writes build/.preview/<Theme>-{desk,dialog,menu}.png
set -eu
cd "$(dirname "$0")"
THEME=$1
GEOM=${2:-1280x800}
DISP=:${PREVIEW_DISPLAY:-77}
WORK=build/.preview/$THEME
rm -rf "$WORK"; mkdir -p "$WORK/conf/themes" "$WORK/cache"
ln -s "$PWD/build/$THEME" "$WORK/conf/themes/$THEME"

pids=()
cleanup() { kill "${pids[@]}" 2>/dev/null || true; wait 2>/dev/null || true; }
trap cleanup EXIT

Xvfb "$DISP" -screen 0 "${GEOM}x24" -nolisten tcp -fp /usr/share/fonts/75dpi,/usr/share/fonts/100dpi >/dev/null 2>&1 & pids+=($!)
sleep 1
export DISPLAY=$DISP
e16 -P "$WORK/conf" -Q "$WORK/cache" -t "$THEME" >"$WORK/e16.log" 2>&1 & pids+=($!)
sleep 3
e() { eesh "$@" >/dev/null 2>&1 || true; }
shot() { xwd -root -silent | ffmpeg -loglevel error -y -f xwd_pipe -i - "build/.preview/$THEME-$1.png"; echo "build/.preview/$THEME-$1.png"; }
winid() { eesh wl | awk -v t="$1" '$3==t {print $1; exit}'; }
focus() { e warp abs "$2" "$3"; e wop "$(winid "$1")" focus; sleep 0.5; }

# Close the "menu generation complete" notice
for w in $(eesh wl | awk '$3=="Message" {print $1}'); do e wop "$w" close; done

# 1. Plain desktop: one inactive and one focused window
xclock -geometry 380x300+70+80 -update 1 -title inactive 2>/dev/null & pids+=($!)
xcalc -geometry 260x300+560+90 -title active 2>/dev/null & pids+=($!)   # xclock refuses focus
sleep 1.5
focus active 690 240
shot desk

# 2. A settings dialog full of widgets, plus a message box
e configure Focus
sleep 1
focus Focus 640 400
e dok "The quick brown Pokemon jumps over the lazy moon."
sleep 1
shot dialog

# 3. Root menu (menus take the focus, so do this last)
for w in $(eesh wl | awk '$3=="Message" || $3=="Focus" {print $1}'); do e wop "$w" close; done
e warp abs 900 300
e menus show ROOT_2
sleep 1
shot menu
