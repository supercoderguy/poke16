#!/bin/bash
# Screenshot a theme's polybar on its e16 desktop, headless and isolated
# (uses a copy of polybar/config.ini pointed at the theme; ~/.config untouched).
#   ./preview-polybar.sh Umbreon   -> build/.preview/<Theme>-polybar.png
set -eu
cd "$(dirname "$0")"
THEME=$1
DISP=:${PREVIEW_DISPLAY:-77}
WORK=$PWD/build/.preview/$THEME-polybar
rm -rf "$WORK"; mkdir -p "$WORK/conf/themes" "$WORK/cache"
ln -s "$PWD/build/$THEME" "$WORK/conf/themes/$THEME"
# polybar rules first: the first matching border rule wins
{ cat polybar/e16-matches.cfg; echo; cat /usr/share/e16/config/matches.cfg; } > "$WORK/conf/matches.cfg"
sed "s|^include-file = .*|include-file = $PWD/build/$THEME/polybar/$THEME.ini|" polybar/config.ini > "$WORK/config.ini"

pids=()
cleanup() { kill "${pids[@]}" 2>/dev/null || true; wait 2>/dev/null || true; }
trap cleanup EXIT

Xvfb "$DISP" -screen 0 1280x800x24 -nolisten tcp -fp /usr/share/fonts/75dpi,/usr/share/fonts/100dpi >/dev/null 2>&1 & pids+=($!)
sleep 1
export DISPLAY=$DISP
e16 -P "$WORK/conf" -Q "$WORK/cache" -t "$THEME" >/dev/null 2>&1 & pids+=($!)
sleep 3
for w in $(eesh wl | awk '$3=="Message" {print $1}'); do eesh wop "$w" close >/dev/null; done
xcalc -geometry 300x200+60+80 -title "A focused window" 2>/dev/null & pids+=($!)
sleep 1
polybar -c "$WORK/config.ini" -q main >"$WORK/polybar.log" 2>&1 & pids+=($!)
sleep 2
eesh warp abs 200 150 >/dev/null; eesh wop "$(eesh wl | awk '/A focused window/ {print $1; exit}')" focus >/dev/null
sleep 1.5
xwd -root -silent | ffmpeg -loglevel error -y -f xwd_pipe -i - "build/.preview/$THEME-polybar.png"
echo "build/.preview/$THEME-polybar.png"
grep -iE 'error|warn' "$WORK/polybar.log" | sort -u | head || true
