# Handoff: bedroom Fire TV cleanup (read this first)

You are a Claude Code session running ON THE USER'S WINDOWS PC, which is on the
same Wi-Fi as the TV. The previous session was in the cloud and could not reach
the LAN. Everything below is already decided; do not re-ask.

## The TV
- Insignia NS-32F202NA22, 32" 720p Fire TV Edition (2022), Fire OS 6.7.1.1
- Amazon account on it: Jennifer Haag. Device name "Jennifer's TV".
- ADB debugging is ON. Port 5555, classic adb connect (no pairing code).
- IP address: 192.168.1.227 (Wi-Fi "GoodMorningSummit", gateway 192.168.1.1). Connect with: adb connect 192.168.1.227:5555

- Symptoms: laggy, "buggy". Goals: debug, free channels, cleaner UI, up to date.

## Hard rules from the user
1. PRESERVE family photos and the screen saver. Amazon Photos, the Fire TV
   screensaver, cloud drive/sync and account services are PROTECTED. Never
   disable, uninstall or clear data on them. adb/03_audit_tv.sh enforces this.
2. No modification commands until the user gives explicit confirmation of the
   categorized list. Steps 1-3 are read-only.
3. Disable with `pm disable-user --user 0 <pkg>` only. Never uninstall.
   Every change must be reversible by undo_backup.sh.

## State so far
- adb: user says they installed Android Platform Tools via
  adb/install_adb_windows.ps1 (expected at C:\platform-tools). Not yet verified.
- No connection to the TV has been made yet. No audit has run.

## Do this, in order
1. Verify adb: `adb version` (fall back to C:\platform-tools\adb.exe).
2. Connect: `bash adb/02_connect_tv.sh` (Git Bash) or manually
   `adb connect <IP>:5555`, then tell the user to press Allow on the TV screen,
   tick "Always allow", and wait until `adb devices` shows `device`.
   Confirm "connected" to the user before anything else.
3. Audit (read-only): `bash adb/03_audit_tv.sh` or the equivalent adb shell
   commands: /proc/meminfo, top -n 1, ps, pm list packages -s / -3 / -d / -e.
   It writes audit/<timestamp>/ and generates undo_backup.sh.
4. Present to the user: RAM free/total, top processes, and packages in three
   groups: [Required System Apps], [My Actively Used Streaming Apps],
   [Safe-to-Disable Bloatware/Telemetry]. Put anything uncertain in Required or
   a "Review" note, never in bloat. Mark protected photo/screensaver packages.
5. STOP and wait for explicit confirmation before running any pm disable-user.
6. After approval: disable only the approved list, reboot (`adb reboot`), and
   confirm photos + screen saver still work.

## Known safe-to-disable candidates on Fire OS 6 (verify each exists first)
com.amazon.tv.legal.notices, com.amazon.tv.fw.metrics, com.amazon.device.metrics,
com.amazon.client.metrics (and .api), com.amazon.hedwig (Help), com.amazon.tv.support,
com.amazon.tv.csapp, com.amazon.wifilocker, com.amazon.advertisingidsettings,
com.amazon.device.crashmanager, com.amazon.device.logmanager, com.amazon.logan,
com.amazon.tv.alexanotification, com.amazon.tv.alexaalerts, com.ivona.* (TTS),
com.amazon.kindle, com.amazon.shopping, com.amazon.tv.promotions.
Do NOT disable: com.amazon.tv.launcher, com.amazon.venezia (Appstore),
com.amazon.dcp*, com.amazon.sync.service, com.amazon.identity*, com.amazon.bueller.photos,
com.amazon.ftv.screensaver, com.amazon.tv.settings*, anything com.android.*.
Updaters (com.amazon.tv.forcedotaupdater.v2, com.amazon.device.software.ota*)
are optional and block OS updates; leave on unless the user asks.

## Other improvements already written up (FIX-GUIDE.md)
Autoplay off under Settings > Preferences > Featured Content; privacy toggles off;
free apps: Pluto TV, Tubi, Roku Channel, Sling Freestream, Plex, antenna via coax.
Custom launcher (Projectivy) via ADB is optional and only if the user asks.

## Files in this folder
- adb/01_check_adb.sh, adb/02_connect_tv.sh, adb/03_audit_tv.sh (read-only)
- adb/install_adb_windows.ps1
- FIX-GUIDE.md, README.md, fire-tv-about-screen.jpg
