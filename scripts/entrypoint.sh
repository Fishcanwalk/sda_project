#!/usr/bin/env bash
set -euo pipefail

# Entry script: wait for MongoDB, run admin init (idempotent), then exec the main command.

MAX_RETRIES=${MAX_RETRIES:-30}
RETRY_DELAY=${RETRY_DELAY:-2}
MONGO_HOST=${MONGODB_HOST:-mongodb}
MONGO_PORT=${MONGODB_PORT:-27017}

wait_for_mongo() {
  echo "Waiting for MongoDB at ${MONGO_HOST}:${MONGO_PORT}..."
  local i=0
  while ! bash -c "</dev/tcp/${MONGO_HOST}/${MONGO_PORT}" >/dev/null 2>&1; do
    i=$((i+1))
    if [ "$i" -ge "$MAX_RETRIES" ]; then
      echo "Timed out waiting for MongoDB after $i attempts" >&2
      return 1
    fi
    sleep "$RETRY_DELAY"
  done
  echo "MongoDB is reachable"
}

run_init() {
  # Use explicit venv python if available
  PYTHON=${PYTHON:-/venv/bin/python3}
  if [ ! -x "$PYTHON" ]; then
    PYTHON=$(which python3 || which python || true)
  fi
  if [ -z "$PYTHON" ]; then
    echo "No python interpreter found to run init-admin" >&2
    return 1
  fi

  echo "Running admin init with $PYTHON /app/scripts/init-admin"
  "$PYTHON" /app/scripts/init-admin || return $?
}

main() {
  # Wait for DB then run init; if waiting fails, continue so container still starts
  if wait_for_mongo; then
    if ! run_init; then
      echo "init-admin failed; continuing to start the service" >&2
    fi
  else
    echo "Skipping init-admin because MongoDB is not reachable" >&2
  fi

  echo "Executing main process: $@"
  exec "$@"
}

main "$@"
