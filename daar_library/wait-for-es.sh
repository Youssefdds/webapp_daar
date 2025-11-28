#!/bin/sh
set -e

host="$1"
shift

echo "Waiting for Elasticsearch at $host..."

until curl -s "$host" > /dev/null; do
  echo "Elasticsearch not ready yet..."
  sleep 2
done

echo "Elasticsearch is up!"
exec "$@"
