#!/bin/bash
# Screenshot a theme's KDE/Qt colour scheme, headless and isolated: a native KDE
# settings page (with Breeze widget previews) run against a private config dir
# whose kdeglobals is the scheme.  Your real ~/.config/kdeglobals isn't touched.
#   ./preview-qt.sh Umbreon   -> build/.preview/<Theme>-qt.png
set -eu
cd "$(dirname "$0")"
THEME=$1
DISP=:${PREVIEW_DISPLAY:-77}
WORK=$PWD/build/.preview/$THEME-qt
rm -rf "$WORK"; mkdir -p "$WORK/config" "$WORK/data" "$WORK/cache"
cp "build/$THEME/qt/$THEME.colors" "$WORK/config/kdeglobals"

pids=()
cleanup() { kill "${pids[@]}" 2>/dev/null || true; wait 2>/dev/null || true; }
trap cleanup EXIT

Xvfb "$DISP" -screen 0 1280x800x24 -nolisten tcp >/dev/null 2>&1 & pids+=($!)
sleep 1
export DISPLAY=$DISP
QT_QPA_PLATFORMTHEME=kde XDG_CONFIG_HOME=$WORK/config XDG_DATA_HOME=$WORK/data XDG_CACHE_HOME=$WORK/cache \
    kcmshell6 kcm_style >"$WORK/kcm.log" 2>&1 & pids+=($!)
sleep 9
xwd -root -silent | ffmpeg -loglevel error -y -f xwd_pipe -i - -vf "crop=680:420:292:92" "build/.preview/$THEME-qt.png"
echo "build/.preview/$THEME-qt.png"
