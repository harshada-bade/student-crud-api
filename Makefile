.PHONY: install run migrate test docker-build docker-run docker-stop

VERSION=1.0.0
IMAGE_NAME=student-api

install:
	pip install -r requirements.txt

run:
	python run.py

migrate:
	flask db migrate -m "migration"

upgrade:
	flask db upgrade

test:
	pytest tests/ -v

# ── Docker targets ──────────────────────────────────

docker-build:
	docker build -t $(IMAGE_NAME):$(VERSION) .

docker-run:
	docker run -d \
		--name student-api \
		-p 5000:5000 \
		-e DATABASE_URL=sqlite:///students.db \
		-e LOG_LEVEL=INFO \
		$(IMAGE_NAME):$(VERSION)

docker-stop:
	docker stop student-api
	docker rm student-api

# ── Docker Compose targets ──────────────────────────────────

db-start:
	@echo "Starting database container..."
	docker compose up -d db
	@echo "Waiting for database to be healthy..."
	@until docker inspect --format='{{.State.Health.Status}}' student-db 2>/dev/null | grep -q healthy; do \
		sleep 1; \
	done
	@echo "Database is healthy and ready ✅"

db-migrate: db-start
	@echo "Running database migrations..."
	docker compose run --rm api flask db upgrade
	@echo "Migrations applied ✅"

compose-build:
	docker compose build

compose-up: db-migrate compose-build
	@echo "Starting API container..."
	docker compose up -d api
	@echo "API is up at http://127.0.0.1:5000 ✅"

compose-down:
	docker compose down

compose-logs:
	docker compose logs -f

api-start: compose-up