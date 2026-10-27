#!/usr/bin/env bash
# Step 3 - READ ONLY audit. Runs only inspection commands (cat, dumpsys, top, ps,
# pm list, settings list, getprop). Writes results to audit/<timestamp>/ and
# generates undo_backup.sh from the TV's real current state. Changes NOTHING on the TV.
set -u
ADB="${ADB:-adb}"
HERE="$(cd "$(dirname "$0")" && pwd)"
SERIAL="${1:-$(cat "$HERE/.tv_serial" 2>/dev/null || true)}"
[ -z "$SERIAL" ] && { echo "Usage: $0 <IP:5555>  (or run 02_connect_tv.sh first)"; exit 1; }
A="$ADB -s $SERIAL"
state=$($ADB devices | awk -v d="$SERIAL" '$1==d {print $2}')
[ "$state" = "device" ] || { echo "Device $SERIAL is '$state', not 'device'. Run 02_connect_tv.sh."; exit 1; }

TS=$(date +%Y%m%d-%H%M%S)
OUT="$HERE/../audit/$TS"
mkdir -p "$OUT"
echo "Writing audit to $OUT"

# ---- 1. RAM and processes -------------------------------------------------
$A shell getprop > "$OUT/getprop.txt"
$A shell cat /proc/meminfo > "$OUT/meminfo.txt"
$A shell dumpsys meminfo > "$OUT/dumpsys_meminfo.txt" 2>/dev/null
( $A shell top -n 1 -m 30 2>/dev/null || $A shell top -n 1 ) > "$OUT/top.txt"
$A shell ps -A > "$OUT/ps.txt" 2>/dev/null || $A shell ps > "$OUT/ps.txt"
$A shell dumpsys activity services 2>/dev/null | grep -E '^\s+\* ServiceRecord' > "$OUT/running_services.txt" || true

# ---- 2. Packages -----------------------------------------------------------
$A shell pm list packages -f  | sed 's/^package://' | sort > "$OUT/packages_all_paths.txt"
$A shell pm list packages     | sed 's/^package://' | sort > "$OUT/packages_all.txt"
$A shell pm list packages -s  | sed 's/^package://' | sort > "$OUT/packages_system.txt"
$A shell pm list packages -3  | sed 's/^package://' | sort > "$OUT/packages_thirdparty.txt"
$A shell pm list packages -d  | sed 's/^package://' | sort > "$OUT/packages_disabled.txt"
$A shell pm list packages -e  | sed 's/^package://' | sort > "$OUT/packages_enabled.txt"
$A shell settings list global > "$OUT/settings_global.txt" 2>/dev/null
$A shell settings list secure > "$OUT/settings_secure.txt" 2>/dev/null
$A shell settings list system > "$OUT/settings_system.txt" 2>/dev/null

# ---- 3. Categorize ---------------------------------------------------------
# First-pass rules. Anything not matched lands in REVIEW so nothing is guessed.
REQUIRED_RE='^(android|com\.android\.|com\.amazon\.tv\.launcher$|com\.amazon\.tv\.settings|com\.amazon\.tv\.devicecontrolsettings|com\.amazon\.device\.settings|com\.amazon\.dcp|com\.amazon\.sync|com\.amazon\.venezia|com\.amazon\.tv\.parentalcontrols|com\.amazon\.tv\.oobe|com\.amazon\.alta\.h2clientservice|com\.amazon\.identity|com\.amazon\.firebat|com\.amazon\.imp|com\.amazon\.tv\.ime|com\.amazon\.tv\.input|com\.amazon\.tv\.livetv|com\.amazon\.tv\.remote|com\.amazon\.bluetoothdialer|com\.amazon\.device\.bluetooth|com\.amazon\.tv\.fw|com\.amazon\.device\.sale|com\.amazon\.tv\.settings\.|com\.amazon\.acos|com\.amazon\.aca$|com\.amazon\.ssm$|com\.amazon\.ssmsys$|com\.amazon\.tv\.nimh|com\.amazon\.device\.messaging|com\.amazon\.providers|com\.amazon\.webview|com\.amazon\.vizzini|com\.amazon\.tv\.ottssocompanionapp|com\.amazon\.ftv\.screensaver|com\.amazon\.tv\.legacyapis|com\.amazon\.platform|com\.amazon\.tv\.releasenotes|com\.svox|com\.insignia|com\.amazon\.cpl|com\.amazon\.ags|com\.amazon\.tv\.alexadevicecontrols|com\.amazon\.alexa|com\.amazon\.tv\.alexa)'
STREAM_RE='^(com\.netflix|com\.google\.android\.youtube|com\.amazon\.firetv\.youtube|com\.amazon\.avod|com\.amazon\.firebat\.|com\.hulu|com\.disney|tv\.pluto|com\.tubitv|com\.roku|com\.plexapp|com\.spotify|com\.hbo|com\.wbd|com\.peacocktv|com\.cbs|com\.paramount|com\.sling|com\.xumo|com\.crackle|org\.pbs|com\.espn|com\.apple\.atve|com\.twitch|com\.amazon\.tv\.livetv|com\.philo|com\.fubo|com\.crunchyroll|com\.amazon\.music|com\.amazon\.bueller\.music|com\.amazon\.cloud9|com\.amazon\.bueller\.photos|com\.iheart|com\.pandora|com\.tidal|com\.plex)'
BLOAT_RE='^(com\.amazon\.tv\.legal\.notices|com\.amazon\.tv\.fw\.metrics|com\.amazon\.device\.metrics|com\.amazon\.client\.metrics|com\.amazon\.hedwig|com\.amazon\.tv\.support|com\.amazon\.tv\.csapp|com\.amazon\.wifilocker|com\.amazon\.advertisingidsettings|com\.amazon\.ssm\.|com\.amazon\.sharingservice|com\.amazon\.kindle|com\.amazon\.shopping|com\.amazon\.tv\.alexanotification|com\.amazon\.tv\.alexaalerts|com\.amazon\.device\.crashmanager|com\.amazon\.device\.logmanager|com\.amazon\.logan|com\.amazon\.tv\.ottssocompanionapp\.metrics|com\.ivona|com\.amazon\.ftv\.collect|com\.amazon\.tv\.promotions|com\.amazon\.tv\.setupcompanion|com\.amazon\.recess|com\.amazon\.tv\.whisperplay|com\.amazon\.whisperlink|com\.amazon\.whisperplay|com\.amazon\.tv\.notification|com\.amazon.ftv\.notifications)'
UPDATER_RE='^(com\.amazon\.tv\.forcedotaupdater|com\.amazon\.device\.software\.ota)'

: > "$OUT/cat_required.txt"; : > "$OUT/cat_streaming.txt"; : > "$OUT/cat_bloat.txt"; : > "$OUT/cat_updater.txt"; : > "$OUT/cat_review.txt"
while read -r pkg; do
  [ -z "$pkg" ] && continue
  tp=""; grep -qx "$pkg" "$OUT/packages_thirdparty.txt" && tp=" (user-installed)"
  if   echo "$pkg" | grep -Eq "$UPDATER_RE";  then echo "$pkg" >> "$OUT/cat_updater.txt"
  elif echo "$pkg" | grep -Eq "$STREAM_RE";   then echo "$pkg$tp" >> "$OUT/cat_streaming.txt"
  elif [ -n "$tp" ];                          then echo "$pkg$tp" >> "$OUT/cat_streaming.txt"
  elif echo "$pkg" | grep -Eq "$BLOAT_RE";    then echo "$pkg" >> "$OUT/cat_bloat.txt"
  elif echo "$pkg" | grep -Eq "$REQUIRED_RE"; then echo "$pkg" >> "$OUT/cat_required.txt"
  else echo "$pkg" >> "$OUT/cat_review.txt"; fi
done < "$OUT/packages_all.txt"

# ---- 4. undo_backup.sh from real state ------------------------------------
UNDO="$HERE/../undo_backup.sh"
{
  echo "#!/usr/bin/env bash"
  echo "# Generated $TS from $SERIAL. Restores every package to the enabled/disabled"
  echo "# state it had at audit time. Run: ./undo_backup.sh [IP:5555]"
  echo "set -u"
  echo "ADB=\"\${ADB:-adb}\"; SERIAL=\"\${1:-$SERIAL}\"; A=\"\$ADB -s \$SERIAL\""
  echo "echo 'Restoring package states...'"
  while read -r pkg; do
    [ -z "$pkg" ] && continue
    if grep -qx "$pkg" "$OUT/packages_disabled.txt"; then
      echo "\$A shell pm disable-user --user 0 $pkg >/dev/null 2>&1 || true   # was disabled"
    else
      echo "\$A shell pm enable $pkg >/dev/null 2>&1 || true"
    fi
  done < "$OUT/packages_all.txt"
  echo "echo 'Done. Reboot the TV: \$A reboot'"
} > "$UNDO"
chmod +x "$UNDO"
cp "$UNDO" "$OUT/undo_backup.sh"

# ---- 5. Summary ------------------------------------------------------------
echo
echo "===== RAM ====="
grep -E 'MemTotal|MemFree|MemAvailable' "$OUT/meminfo.txt"
echo
echo "===== Top processes ====="
head -25 "$OUT/top.txt"
echo
for c in required streaming bloat updater review; do
  echo "===== $(echo "$c" | tr a-z A-Z) ($(wc -l < "$OUT/cat_$c.txt")) ====="
  cat "$OUT/cat_$c.txt"; echo
done
echo "Full output: $OUT"
echo "Undo script: $UNDO   (nothing has been changed on the TV)"
