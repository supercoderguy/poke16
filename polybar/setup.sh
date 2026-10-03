#!/bin/bash
# One-off polybar setup for the e16 session (safe to re-run).
#   - links ~/.config/polybar/{config.ini,launch.sh,nowplaying.sh} to this project
#   - points ~/.config/polybar/theme.ini at the current e16 theme
#   - writes ~/.e16/matches.cfg: the polybar rules, then e16's defaults
#     (first matching border rule wins, so ours must come first)
#   - adds the launcher to ~/.e16/Init/autostart.sh
set -eu
here=$(cd "$(dirname "$0")" && pwd)
root=$(dirname "$here")
cfg=$HOME/.config/polybar
mkdir -p "$cfg"

for f in config.ini launch.sh nowplaying.sh; do
    if [ -e "$cfg/$f" ] && [ ! -L "$cfg/$f" ]; then
        echo "refusing to replace $cfg/$f (not a symlink)" >&2; exit 1
    fi
    ln -sfn "$here/$f" "$cfg/$f"
done

theme=$(eesh theme 2>/dev/null | awk '/^Name:/ {print $2}')
theme=${theme:-Umbreon}
ln -sfn "$root/build/$theme/polybar/$theme.ini" "$cfg/theme.ini"
echo "polybar theme: $theme"

m=$HOME/.e16/matches.cfg
if [ -e "$m" ] && ! grep -q 'Class.*Polybar' "$m"; then
    echo "$m exists without polybar rules; add $here/e16-matches.cfg at its top by hand" >&2
else
    { echo "# written by $here/setup.sh"; cat "$here/e16-matches.cfg"; echo; cat /usr/share/e16/config/matches.cfg; } > "$m"
    echo "wrote $m"
fi

a=$HOME/.e16/Init/autostart.sh
if ! grep -q 'polybar/launch.sh' "$a"; then
    printf '\n# polybar (see %s)\n~/.config/polybar/launch.sh\n' "$here" >> "$a"
    echo "added polybar to $a"
fi
