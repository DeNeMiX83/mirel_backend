DOCKER_COMPOSE := deploy/docker-compose.yml
DOCKER_ENV := deploy/.env
DOCKER_COMPOSE_RUNNER := docker compose
PROJECT_NAME := mirel
ROOT_PATH := /mirel/api/v1
ifneq ($(ENV),)
	DOCKER_COMPOSE := deploy/dev.docker-compose.yml
	DOCKER_COMPOSE_RUNNER := docker compose
	ifeq ($(ENV),docker)
		DOCKER_ENV := deploy/.env.dev
		include deploy/.env.dev
		export $(shell sed 's/=.*//' deploy/.env.dev)
	else ifeq ($(ENV),local)
		DOCKER_ENV := deploy/.env.dev.local
		include deploy/.env.dev.local
		export $(shell sed 's/=.*//' deploy/.env.dev.local)
	endif
endif


.PHONY: run-backend
run-backend:
	poetry run gunicorn mirel.presentation.api.main:app --reload -b $(HOST):$(BACKEND_PORT) \
	--worker-class uvicorn.workers.UvicornWorker \
	--log-level $(LOG_LEVEL)

.PHONY: run-backend-uvi
run-backend-uvi:
	poetry run uvicorn mirel.presentation.api.main:app --reload --host $(HOST) --port $(BACKEND_PORT) --root-path $(ROOT_PATH)

.PHONY: set-type-objects
set-type-objects:
	poetry run python -m mirel.presentation.cli.add_type_objects

.PHONY: set-type-solution
set-type-solution:
	poetry run python -m mirel.presentation.cli.add_type_solution

.PHONY: migrate-create
migrate-create:
	poetry run alembic -c mirel/config/alembic.ini revision --autogenerate

.PHONY: migrate-up
migrate-up:
	poetry run alembic -c mirel/config/alembic.ini upgrade head

.PHONY: compose-up
compose-up:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) \
	-p $(PROJECT_NAME) up

.PHONY: compose-build
compose-build:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) \
	-p $(PROJECT_NAME) build

.PHONY: compose-pull
compose-pull:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) \
	-p $(PROJECT_NAME) pull

.PHONY: compose-down
compose-down:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) \
	-p $(PROJECT_NAME) down

.PHONY: compose-logs
compose-logs:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) \
	-p $(PROJECT_NAME) logs -f

.PHONY: compose-set-type-objects
compose-set-type-objects:
	docker exec -it mirel_backend set-type-objects

.PHONY: compose-set_type_solution
compose-set-type-solution:
	docker exec -it mirel_backend set-type-solution

.PHONY: get-yandex-disk-token
get-yandex-disk-token:
	poetry run python -m mirel.presentation.cli.get_yandex_token