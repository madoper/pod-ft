#!/bin/bash
# pod-ft local development environment
# Starts all infrastructure services and development servers

set -euo pipefail

echo "=== Starting infrastructure ==="
docker compose up -d postgres qdrant minio redis

echo "=== Waiting for services ==="
sleep 5

echo "=== Initializing MinIO buckets ==="
bash infra/minio/create-buckets.sh

echo "=== Running migrations ==="
uv run alembic upgrade head

echo "=== Starting gateway dev server ==="
uv run --directory backend/apps/gateway uvicorn app.main:app --reload --port 8000
