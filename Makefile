COMPOSE=docker compose

APP=bookroom-api
NETWORK=bookroom_default
ENV_FILE=.env.docker

ADMIN_EMAIL ?= admin@bookroom.com
ADMIN_PASSWORD ?= admin123

.PHONY: up down build logs migrate seed admin rebuild

up:
	$(COMPOSE) up --build -d

stop:
	$(COMPOSE) stop

down:
	$(COMPOSE) down -v

build:
	$(COMPOSE) build

logs:
	$(COMPOSE) logs -f

migrate:
	docker run --rm \
		--network=$(NETWORK) \
		--env-file $(ENV_FILE) \
		$(APP) migrate

seed:
	docker run --rm \
		--network=$(NETWORK) \
		--env-file $(ENV_FILE) \
		$(APP) seed

admin:
	docker run --rm \
		--network=$(NETWORK) \
		--env-file $(ENV_FILE) \
		-e ADMIN_EMAIL=$(ADMIN_EMAIL) \
		-e ADMIN_PASSWORD=$(ADMIN_PASSWORD) \
		$(APP) create-admin

rebuild:
	$(COMPOSE) down -v
	$(COMPOSE) build --no-cache
	$(COMPOSE) up -d
