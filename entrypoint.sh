#!/bin/sh
set -e
echo "JAVA PATH: $(which java)"
java -version
java -jar /tmp/tika-server.jar --host 0.0.0.0 --port ${PORT:-8088} &
# Wait for Tika server to start
sleep 10
exec python3 main.py
