# ADB workflow for the bedroom Fire TV

These must run on a computer that is on the same Wi-Fi as the TV. A cloud
Claude session cannot reach your LAN. Open a session on your PC first:

- Claude Desktop app, open the `fire-tv-project` folder, or
- in a terminal inside `fire-tv-project`, run `claude remote-control`

Then run the steps in order. Steps 1 to 3 are read-only; they change nothing on the TV.

| Step | Script | What it does |
|---|---|---|
| 1 | `adb/01_check_adb.sh` | Finds adb or prints the official install steps |
| 2 | `adb/02_connect_tv.sh [IP]` | Scans the LAN, connects, waits for you to press Allow on the TV, reports "connected" |
| 3 | `adb/03_audit_tv.sh` | RAM, processes, all packages, categorized; writes `audit/<time>/` and `undo_backup.sh` |
| 4 | (pending your approval) | Any `pm disable-user` changes, each reversible with `undo_backup.sh` |

On the TV, ADB debugging lives under Settings > My Fire TV > Developer Options.
The IP address is under Settings > My Fire TV > About > Network.

Package categories are a first pass from known Fire OS package names. Anything
the script is not sure about goes in REVIEW, not in bloat. Nothing is disabled
until you say so, and nothing is ever uninstalled.
