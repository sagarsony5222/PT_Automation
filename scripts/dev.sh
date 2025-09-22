#!/usr/bin/env bash
set -euo pipefail

echo "=== Dev helper: create kind cluster (if missing) and start mongo ==="

# create kind cluster if not exists
if ! kind get clusters | grep -q pt-dev; then
  echo "Creating kind cluster 'pt-dev'..."
  kind create cluster --name pt-dev
else
  echo "kind cluster 'pt-dev' already exists"
fi

# start local mongo if not running
if ! docker ps --format '{{.Names}}' | grep -q '^mongo$'; then
  echo "Starting local MongoDB container..."
  docker run -d --name mongo -p 27017:27017 mongo:6 || true
else
  echo "MongoDB container already running"
fi

echo "Dev environment is ready. kubeconfig context should be 'kind-pt-dev'."
