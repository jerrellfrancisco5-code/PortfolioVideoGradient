# Bedroom Fire TV: what the photo says and how to fix it

Model: Insignia NS-32F202NA22 (F20 series, 32", 720p, Fire TV Edition, 2022 model year)
Software: Fire OS 6.7.1.1 (Android 7.1 based)
Storage: 3.59 GB free (likely of 8 GB) - storage is NOT the problem
Clock: correct, so network and time sync are working

Honest baseline: this is a budget TV with a weak processor and about 1 GB of RAM.
Fire OS 6 is the old branch; this TV will never get Fire OS 8. Software tweaks
below help a lot, but the hardware is the ceiling.

## 1. Debug the lag (do these in order, test after each)

1. Hard restart: Settings > My Fire TV > Restart. Or hold Select + Play/Pause for 5 s.
   Or unplug the TV for 60 seconds. Do this first; it fixes most "buggy" days.
2. Check for updates: Settings > My Fire TV > About > Check for Updates.
   If it offers anything newer than 6.7.1.1, install it.
3. Clear app caches: Settings > Applications > Manage Installed Applications >
   pick each app you use > Clear Cache (not Clear Data unless it still misbehaves).
   Do Prime Video, Netflix, YouTube and anything else heavy.
4. Uninstall apps you never open. Same menu > Uninstall.
5. Stop the home screen from autoplaying ads:
   Settings > Preferences > Featured Content > Allow Video Autoplay OFF,
   Allow Audio Autoplay OFF. This is the single biggest "feels faster" change.
6. Turn off tracking and background data:
   Settings > Preferences > Privacy Settings > Device Usage Data OFF,
   Collect App Usage Data OFF, Interest-based Ads OFF.
   Settings > Preferences > Data Monitoring OFF.
7. Notifications: Settings > Preferences > Notification Settings > turn off app notifications.
8. Wi-Fi: Settings > Network, look at signal strength. Use the 5 GHz band if your router has one.
   If it says Fair or Weak, move the router or add an extender.
9. Remote: fresh batteries. A dying remote sends phantom presses that look like UI bugs.
   Re-pair: hold Home for 10 s.
10. Last resort: Settings > My Fire TV > Reset to Factory Defaults. Then sign in and
    install only the apps you use. Old Fire TVs often run much better after this.

## 2. Free channels (all legal, no account cost)

- Keep: Amazon Photos and the screen saver are protected; do not uninstall or clear data on them.
- Antenna: this TV has a built-in tuner. A cheap flat indoor antenna on the coax
  input gives local broadcast channels (ABC, CBS, NBC, FOX, PBS) free in HD.
  Settings > Live TV > Channel Scan. They show up in the Fire TV Live tab guide.
- Fire TV Channels: already built in, under the Live tab. Hundreds of free ad-supported channels.
- Apps to install from the Appstore:
  - Pluto TV (live channel grid, like cable)
  - Tubi (biggest free movie and show library)
  - The Roku Channel (works on Fire TV)
  - Sling Freestream (free live channels, no Sling subscription needed)
  - Xumo Play, Plex (free live TV plus your own media), Crackle
  - PBS, YouTube
  - Kanopy and Hoopla with a library card
  - Prime Video "Watch for Free" section (Freevee was folded into it; free with ads)

## 3. Make the interface better

Inside the stock UI:
- Autoplay off (step 5 above) makes the home screen calm and fast.
- Reorder apps: highlight an app in Your Apps & Channels, press Menu (three lines) > Move.
  Put the 6 you actually use in the front row.
- Settings > Preferences > Featured Content and Settings > Preferences > Content
  Preferences let you hide stuff you don't want.
- Settings > Display & Sounds > Display > turn off any "Dynamic" picture mode and use
  Movie or Natural; it looks better and the TV works less.

Bigger change (needs your PC on the same Wi-Fi):
- You can install a custom launcher such as Projectivy Launcher using ADB and the
  Launcher Manager tool. It removes the ads and gives a clean, fast home screen.
  Trade-offs: Amazon updates sometimes break it, it takes 20 minutes of setup,
  and it is reversible. If you want this, connect your PC with Remote Control
  and I can walk the ADB steps with you.

## 4. The real upgrade

The panel is fine; the computer inside is slow. A Fire TV Stick 4K (or any modern
streaming stick) plugged into HDMI 1 bypasses the TV's brain entirely, runs the
current Fire OS, and makes this TV feel new for far less than a replacement.
Set the TV's input to that HDMI and it will auto-wake with the stick's remote.
