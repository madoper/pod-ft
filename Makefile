# pod-ft development tasks

.PHONY: dev infra migrate lint typecheck test clean

dev: infra migrate
	uv run uvicorn backend.apps.gateway.app.main:app --reload --host 0.0.0.0 --port 8000

infra:
	docker compose up -d postgres qdrant minio redis neo4j
	$(MAKE) infra-buckets

infra-vps:
	docker compose up -d postgres qdrant minio redis
	$(MAKE) infra-buckets

infra-buckets:
	powershell -Command "
		Get-Content infra/minio/create-buckets.sh | Select-String 'mc' | ForEach-Object {
			if ($$_ -match 'mc mb (.+)') { Write-Host 'Bucket:' $$Matches[1] }
		}
	" 2>nul || true

migrate:
	uv run alembic upgrade head

gateway:
	uv run uvicorn backend.apps.gateway.app.main:app --reload --host 0.0.0.0 --port 8000

lint:
	ruff check .

typecheck:
	mypy backend/

test:
	uv run python -m pytest

test-unit:
	uv run python -m pytest backend/tests/unit/

test-e2e:
	uv run python -m pytest backend/tests/e2e/ --base-url=$(or $(BASE_URL),http://localhost:8000)

clean:
	powershell -Command "Get-ChildItem -Recurse -Directory -Filter '__pycache__' | Remove-Item -Recurse -Force 2>nul; Get-ChildItem -Recurse -Filter '*.pyc' | Remove-Item -Force 2>nul"
