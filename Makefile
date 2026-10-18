# VIF SmartShelf — Makefile

.DEFAULT_GOAL := help
.PHONY: help dev web-dev api-dev db-start db-migrate db-reset lint-api lint-web test-api test-web docker-build clean

# ================================================================
# Variables
# ================================================================

API_DIR := apps/services/inference-api
WEB_DIR := apps/web
DOCKER_COMPOSE := docker compose

# ================================================================
# Help
# ================================================================

help:
	@echo ""
	@echo "  VIF SmartShelf — Developer Commands"
	@echo "  ======================================"
	@echo ""
	@echo "  Development:"
	@echo "    make dev          Start full local stack (DB + API + Web)"
	@echo "    make api-dev      Start inference API only (hot-reload)"
	@echo "    make web-dev      Start Next.js frontend only (hot-reload)"
	@echo "    make db-start     Start PostgreSQL in Docker"
	@echo ""
	@echo "  Database:"
	@echo "    make db-migrate   Apply all pending migrations"
	@echo "    make db-reset     Drop + recreate DB and apply migrations (dev only)"
	@echo ""
	@echo "  Linting:"
	@echo "    make lint-api     Ruff + mypy on inference-api"
	@echo "    make lint-web     ESLint + tsc on web app"
	@echo "    make lint         Lint everything"
	@echo ""
	@echo "  Tests:"
	@echo "    make test-api     Run pytest for inference-api"
	@echo "    make test-web     Run Jest tests for web app"
	@echo "    make test         Run all tests"
	@echo ""
	@echo "  Docker:"
	@echo "    make docker-build Build all Docker images"
	@echo "    make docker-up    Start all services via docker compose"
	@echo "    make docker-down  Stop all services"
	@echo ""
	@echo "  Cleanup:"
	@echo "    make clean        Remove build artefacts and caches"
	@echo ""

# ================================================================
# Development
# ================================================================

dev: db-start
	@echo "Starting development stack..."
	@echo "API: http://localhost:8000"
	@echo "Web: http://localhost:3000"
	@echo "DB:  localhost:5432"
	@$(MAKE) -j2 api-dev web-dev

api-dev:
	@echo "Starting inference API..."
	cd $(API_DIR) && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

web-dev:
	@echo "Starting Next.js frontend..."
	cd $(WEB_DIR) && npm run dev

db-start:
	@echo "Starting PostgreSQL..."
	$(DOCKER_COMPOSE) up -d db
	@sleep 2
	@echo "PostgreSQL ready on localhost:5432"

# ================================================================
# Database
# ================================================================

db-migrate:
	@echo "Applying database migrations..."
	cd $(API_DIR) && alembic upgrade head

db-reset:
	@echo "WARNING: This will destroy all local data!"
	$(DOCKER_COMPOSE) down -v
	$(DOCKER_COMPOSE) up -d db
	@sleep 3
	cd $(API_DIR) && alembic upgrade head
	@echo "Database reset complete."

# ================================================================
# Linting
# ================================================================

lint-api:
	@echo "Linting inference API..."
	cd $(API_DIR) && ruff check . && mypy app/

lint-web:
	@echo "Linting web app..."
	cd $(WEB_DIR) && npm run lint && npm run type-check

lint: lint-api lint-web

# ================================================================
# Tests
# ================================================================

test-api:
	@echo "Running API tests..."
	cd $(API_DIR) && pytest tests/ -v

test-web:
	@echo "Running web tests..."
	cd $(WEB_DIR) && npm test

test: test-api test-web

# ================================================================
# Docker
# ================================================================

docker-build:
	@echo "Building Docker images..."
	docker build -t smartshelf-api:dev -f infra/docker/Dockerfile.api .

docker-up:
	$(DOCKER_COMPOSE) up -d

docker-down:
	$(DOCKER_COMPOSE) down

# ================================================================
# Cleanup
# ================================================================

clean:
	@echo "Cleaning build artefacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".next" -exec rm -rf {} + 2>/dev/null || true
	@echo "Clean complete."
