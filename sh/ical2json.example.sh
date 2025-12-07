# -----------------------------------------------------------------
# Copyright (C) 2025 Erwann Rogard
# Source repository: https://github.com/rogard/helpers.py
#
# Python code:
# Released under the GNU General Public License v3.0 or later
# See https://www.gnu.org/licenses/gpl-3.0.html
# -----------------------------------------------------------------

# Troubleshooting:
# - Address already in use Port 5000 is in use by another program
# `fuser -k 5000/tcp || true`

set -e

cd "$(dirname "$0")/.."

# This is a dummy calendar
url_ics='https://calendar.google.com/calendar/ical/abe44317faa2cfe48c0ca99b5ede79bca5e401facae66c109e2cc870e0ad8338%40group.calendar.google.com/public/basic.ics'

cal_json='json/calendar.json'

#!/bin/bash
set -e
cd "$(dirname "$0")/.."

port=5000
url_local="http://127.0.0.1:${port}"
url_proxy="${url_local}/${url_ics}"

# Start Flask
pipenv run python py/ical2json.py &
flask_pid=$!
trap "kill $flask_pid 2>/dev/null || true" EXIT

# Wait for server
for i in {1..30}; do
    curl -s -o /dev/null "${url_local}/" 2>/dev/null && break
    sleep 0.5
done

# Fetch JSON and save
curl -s "${url_proxy}" > "$cal_json"
echo "Saved to $cal_json"
