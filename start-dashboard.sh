#!/bin/bash
# Dashboard Server Startup Script
cd /data/.openclaw/workspace/dashboard/public
python3 -m http.server 8080 > /tmp/dashboard.log 2>&1 &
echo $! > /tmp/dashboard.pid
echo "Dashboard started on http://localhost:8080"