#!/bin/sh
# Polybar now-playing: "Artist – Title", with only the first artist.
# Cuts at the first ", " ";" " x " " with " or "feat."/"ft." -- not at "&", since duo names use it
# (YouTube Music packs collaborators into one artist string), and take only the
# first entry when the player reports several artists.
[ "$(playerctl status 2>/dev/null)" = Playing ] || exit 0
artist=$(playerctl metadata artist 2>/dev/null | head -n1 |
         sed -E 's/ *(,|;| [Ff](ea)?t\.? | [Xx] | with ).*//')
title=$(playerctl metadata title 2>/dev/null)
[ -n "$title" ] || exit 0
if [ -n "$artist" ]; then
    printf '%s – %s\n' "$artist" "$title"
else
    printf '%s\n' "$title"
fi | cut -c1-45
