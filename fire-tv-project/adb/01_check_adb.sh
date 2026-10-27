#!/usr/bin/env bash
# Step 1 - READ ONLY. Checks whether adb is installed on this PC.
# Works in Git Bash (Windows), macOS Terminal, Linux, WSL.
set -u

found=""
if command -v adb >/dev/null 2>&1; then
  found="$(command -v adb)"
else
  for p in \
    "$HOME/platform-tools/adb" \
    "/c/platform-tools/adb.exe" \
    "${LOCALAPPDATA:-}/Android/Sdk/platform-tools/adb.exe" \
    "$HOME/AppData/Local/Android/Sdk/platform-tools/adb.exe" \
    "$HOME/Library/Android/sdk/platform-tools/adb" \
    "$HOME/Android/Sdk/platform-tools/adb"; do
    [ -x "$p" ] && { found="$p"; break; }
  done
fi

if [ -n "$found" ]; then
  echo "adb found: $found"
  "$found" version
  case ":$PATH:" in
    *":$(dirname "$found"):"*) ;;
    *) echo; echo "NOTE: adb is installed but its folder is not on PATH."
       echo "      Either add $(dirname "$found") to PATH or run: export ADB=\"$found\"";;
  esac
  exit 0
fi

cat <<'MSG'
adb is NOT installed.

Install the official Android SDK Platform Tools (Google):
  https://developer.android.com/tools/releases/platform-tools

Windows:
  1. Download "SDK Platform-Tools for Windows" from the link above.
  2. Extract the zip so you have C:\platform-tools\adb.exe
  3. In PowerShell run:
       setx PATH "$env:PATH;C:\platform-tools"
  4. Close and reopen your terminal, then run this script again.

macOS:
  brew install android-platform-tools
  (or unzip to ~/platform-tools and add that folder to PATH)

Linux (Debian/Ubuntu):
  sudo apt install adb
MSG
exit 1
