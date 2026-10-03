#!/bin/bash
# Screenshot music.youtube.com with a theme's Pear Desktop CSS applied, in a
# headless Firefox with a throwaway profile (your browser and Pear untouched).
#   ./preview-ytmusic.sh Umbreon [url]   -> build/.preview/<Theme>-ytmusic.png
set -eu
cd "$(dirname "$0")"
THEME=$1
URL=${2:-https://music.youtube.com/}
DISP=:${PREVIEW_DISPLAY:-77}
WORK=$PWD/build/.preview/$THEME-ytmusic
rm -rf "$WORK"; mkdir -p "$WORK/profile/chrome"

cat > "$WORK/profile/user.js" <<'EOF'
user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);
user_pref("browser.shell.checkDefaultBrowser", false);
user_pref("browser.aboutwelcome.enabled", false);
user_pref("browser.startup.homepage_override.mstone", "ignore");
user_pref("datareporting.policy.dataSubmissionPolicyBypassNotification", true);
user_pref("toolkit.telemetry.reportingpolicy.firstRun", false);
user_pref("browser.tabs.warnOnClose", false);
user_pref("media.autoplay.default", 5);
EOF
{ echo '@-moz-document domain("music.youtube.com") {'; cat "build/$THEME/ytmusic/$THEME.css"; echo '}'; } \
    > "$WORK/profile/chrome/userContent.css"

pids=()
cleanup() { kill "${pids[@]}" 2>/dev/null || true; wait 2>/dev/null || true; }
trap cleanup EXIT

Xvfb "$DISP" -screen 0 1440x900x24 -nolisten tcp >/dev/null 2>&1 & pids+=($!)
sleep 1
DISPLAY=$DISP firefox --no-remote --new-instance --profile "$WORK/profile" --kiosk "$URL" \
    >"$WORK/firefox.log" 2>&1 & pids+=($!)
sleep "${PREVIEW_WAIT:-18}"
DISPLAY=$DISP xwd -root -silent | ffmpeg -loglevel error -y -f xwd_pipe -i - "build/.preview/$THEME-ytmusic.png"
echo "build/.preview/$THEME-ytmusic.png"
