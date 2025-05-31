#!/usr/bin/env bash

host="$1"
shift
port="${host##*:}"
host="${host%%:*}"

while ! nc -z "$host" "$port"; do
  echo "Waiting for $host:$port..."
  sleep 2
done

exec "$@"