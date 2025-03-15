#!/bin/sh
set -e
echo "JAVA PATH: $(which java)"
java -version
echo "Starting Tika server..."
java -jar /tmp/tika-server.jar --host 0.0.0.0 --port ${PORT:-8088} &
echo "Waiting for Tika server to become available..."
# Poll the Tika endpoint until it responds
until curl -s "http://localhost:${PORT:-8088}" > /dev/null; do
    echo "Waiting for Tika server..."
    sleep 1
done
echo "Tika server is up, starting main application..."
exec python3 main.py
