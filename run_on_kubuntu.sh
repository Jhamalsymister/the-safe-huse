#!/bin/bash
# Kubuntu launcher for the Jhamal Symister news tracker
# Works on Kubuntu / Ubuntu 24.04: Konsole -> ./run_on_kubuntu.sh
set -e
cd "$(dirname "$0")"
command -v python3 >/dev/null || { echo "Python 3 not found. Install it: sudo apt install python3"; exit 1; }
python3 news_tracker.py --all "$@"
# Open today's post in the default Kubuntu editor/viewer, if a desktop is running
POST="posts/all_news_$(date +%F).md"
[ -f "$POST" ] && [ -n "$DISPLAY" ] && xdg-open "$POST" >/dev/null 2>&1 || true
