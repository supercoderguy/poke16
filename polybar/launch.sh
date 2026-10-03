#!/bin/sh
# (Re)start polybar on the primary monitor.  Called from ~/.e16/Init/autostart.sh.
killall -q polybar
while pgrep -u "$(id -u)" -x polybar >/dev/null; do sleep 0.2; done
MONITOR=$(polybar --list-monitors 2>/dev/null | awk -F: '/primary/ {print $1; exit}')
[ -n "$MONITOR" ] || MONITOR=$(polybar --list-monitors 2>/dev/null | awk -F: 'NR==1 {print $1}')
MONITOR=$MONITOR polybar main >"${XDG_RUNTIME_DIR:-/tmp}/polybar.log" 2>&1 &
