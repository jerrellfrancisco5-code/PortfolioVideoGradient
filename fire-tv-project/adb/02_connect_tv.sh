#!/usr/bin/env bash
# Step 2 - READ ONLY. Finds the Fire TV on the LAN and opens an adb connection.
# Modifies nothing on the TV. Usage: ./02_connect_tv.sh [TV_IP]
# Fire OS 6 uses classic "ADB debugging" on port 5555 (no pairing code).
set -u
ADB="${ADB:-adb}"
PORT=5555
IP="${1:-}"

"$ADB" start-server >/dev/null 2>&1
echo "== adb devices already known =="
"$ADB" devices -l

# 1. Already connected over the network?
known=$("$ADB" devices | awk 'NR>1 && $1 ~ /:5555$/ {print $1}' | head -1)
if [ -z "$IP" ] && [ -n "$known" ]; then
  IP="${known%:5555}"
  echo "Found existing network device: $IP"
fi

# 2. mDNS discovery (newer adb only; harmless if unsupported)
if [ -z "$IP" ]; then
  echo "== mDNS lookup =="
  out=$("$ADB" mdns services 2>/dev/null || true)
  echo "$out"
  IP=$(echo "$out" | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' | head -1 || true)
fi

# 3. Subnet scan for port 5555
if [ -z "$IP" ]; then
  myip=""
  if command -v hostname >/dev/null && hostname -I >/dev/null 2>&1; then
    myip=$(hostname -I | awk '{print $1}')
  elif command -v ipconfig >/dev/null; then
    myip=$(ipconfig 2>/dev/null | grep -Eo 'IPv4[^:]*: *([0-9.]+)' | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' | grep -E '^(192\.168|10\.|172\.)' | head -1)
    [ -z "$myip" ] && myip=$(ipconfig getifaddr en0 2>/dev/null || true)
  fi
  if [ -n "$myip" ]; then
    prefix="${myip%.*}"
    echo "== Scanning $prefix.1-254 for port $PORT (about a minute) =="
    for i in $(seq 1 254); do
      ( exec 3<>"/dev/tcp/$prefix.$i/$PORT" ) 2>/dev/null && { echo "  open: $prefix.$i"; IP="$prefix.$i"; break; }
    done
  fi
fi

if [ -z "$IP" ]; then
  echo
  echo "Could not find the TV automatically."
  echo "On the TV: Settings > My Fire TV > About > Network shows the IP address."
  read -rp "Enter the TV's IP address: " IP
fi

echo "== Connecting to $IP:$PORT =="
"$ADB" connect "$IP:$PORT"

echo
echo ">>> LOOK AT THE TV NOW. A dialog 'Allow USB debugging?' should appear."
echo ">>> Tick 'Always allow from this computer' and select OK."
echo "Waiting up to 3 minutes for authorization..."
for _ in $(seq 1 90); do
  state=$("$ADB" devices | awk -v d="$IP:$PORT" '$1==d {print $2}')
  case "$state" in
    device)
      echo
      echo "CONNECTED: $IP:$PORT status = device"
      "$ADB" -s "$IP:$PORT" shell getprop ro.product.model
      "$ADB" -s "$IP:$PORT" shell getprop ro.build.version.name 2>/dev/null
      echo "$IP:$PORT" > "$(dirname "$0")/.tv_serial"
      exit 0;;
    unauthorized) printf 'u';;
    offline) printf 'o'; "$ADB" connect "$IP:$PORT" >/dev/null 2>&1;;
    *) printf '.';;
  esac
  sleep 2
done
echo
echo "Timed out. Status was: ${state:-none}. Check that ADB debugging is ON under"
echo "Settings > My Fire TV > Developer Options, and that the PC and TV are on the same Wi-Fi."
exit 1
