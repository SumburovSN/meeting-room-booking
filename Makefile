COMPOSE=docker compose

APP=bookroom-api

.PHONY: up down build logs migrate seed admin test rebuild

up:
	$(COMPOSE) up --build

down:
	$(COMPOSE) down -v

build:
	$(COMPOSE) build

logs:
	$(COMPOSE) logs -f

migrate:
	docker run --network=bookroom_default $(APP) migrate

seed:
	docker run --network=bookroom_default $(APP) seed

admin:
	docker run --network=bookroom_default \
		-e ADMIN_EMAIL=admin@bookroom.local \
		-e ADMIN_PASSWORD=admin123 \
		$(APP) create-admin

rebuild:
	$(COMPOSE) down -v
	$(COMPOSE) build --no-cache
	$(COMPOSE) up
