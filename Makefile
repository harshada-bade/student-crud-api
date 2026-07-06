.PHONY: install run migrate upgrade test lint clean help docker-build docker-run docker-stop db-start db-migrate compose-build compose-up compose-down compose-logs api-start info prometheus-pf alertmanager-pf

VERSION=1.0.0
IMAGE_NAME=student-api

install:
	uv sync

run:
	uv run python run.py

migrate:
	uv run flask db migrate -m "migration"

upgrade:
	uv run flask db upgrade

test:
	uv run pytest tests/ -v

# ── Docker targets ──────────────────────────────────

docker-build:
	docker build -t $(IMAGE_NAME):$(VERSION) -t $(IMAGE_NAME):latest .

docker-run:
	docker run -d \
		--name student-api \
		-p 5000:5000 \
		-e DATABASE_URL=sqlite:///students.db \
		-e LOG_LEVEL=INFO \
		$(IMAGE_NAME):$(VERSION)

docker-stop:
	docker stop student-api || true
	docker rm student-api || true

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

# ── Linter targets ──────────────────────────────────

lint:
	uv run flake8 app/ tests/

# ── Service Info ──────────────────────────────────

info:
	@MINIKUBE_IP=$$(minikube ip) && \
	echo "" && \
	echo "=== Grafana ===" && \
	echo "  URL:      http://$$MINIKUBE_IP:30119" && \
	echo "  Username: admin" && \
	echo "  Password: $$(kubectl get secret kube-prometheus-stack-grafana -n observability -o jsonpath='{.data.admin-password}' | base64 -d)" && \
	echo "" && \
	echo "=== ArgoCD ===" && \
	echo "  URL:      http://$$MINIKUBE_IP:30080" && \
	echo "  Username: admin" && \
	echo "  Password: $$(kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath='{.data.password}' | base64 -d)" && \
	echo "" && \
	echo "=== Prometheus (no auth) ===" && \
	echo "  Run: make prometheus-pf  -> http://localhost:9090" && \
	echo "" && \
	echo "=== Alertmanager (no auth) ===" && \
	echo "  Run: make alertmanager-pf  -> http://localhost:9093" && \
	echo ""

prometheus-pf:
	kubectl port-forward svc/prometheus-kube-prometheus-stack-prometheus -n observability 9090:9090

alertmanager-pf:
	kubectl port-forward svc/kube-prometheus-stack-alertmanager -n observability 9093:9093

# ── Cleanup ──────────────────────────────────

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete
	rm -rf .venv

# ── Help ──────────────────────────────────

help:
	@echo "Available targets:"
	@echo "  install        Install dependencies via uv"
	@echo "  run            Run the Flask development server"
	@echo "  migrate        Generate a new database migration"
	@echo "  upgrade        Apply pending database migrations"
	@echo "  test           Run the test suite"
	@echo "  lint           Run flake8 linter"
	@echo "  clean          Remove __pycache__, .pyc files, and .venv"
	@echo "  docker-build   Build Docker image ($(IMAGE_NAME):$(VERSION) and :latest)"
	@echo "  docker-run     Run the Docker image locally"
	@echo "  docker-stop    Stop and remove the Docker container"
	@echo "  db-start       Start the database container via Docker Compose"
	@echo "  db-migrate     Run migrations via Docker Compose"
	@echo "  compose-build  Build all Docker Compose services"
	@echo "  compose-up     Start the full stack via Docker Compose"
	@echo "  compose-down   Stop all Docker Compose services"
	@echo "  compose-logs   Tail Docker Compose logs"
	@echo "  info           Print URLs and credentials for all service UIs"
	@echo "  prometheus-pf  Port-forward Prometheus to http://localhost:9090"
	@echo "  alertmanager-pf Port-forward Alertmanager to http://localhost:9093"
