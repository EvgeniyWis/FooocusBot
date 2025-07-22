export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

all: down-all build up-all up-bot down-bot logs-bot restart-bot sh-bot up-redis down-redis logs-redis restart-redis sh-redis up-loki down-loki logs-loki restart-loki sh-loki up-promtail down-promtail logs-promtail restart-promtail sh-promtail up-grafana down-grafana logs-grafana restart-grafana sh-grafana up-nginx down-nginx logs-nginx restart-nginx sh-nginx

build:
	docker-compose build

up-all:
	docker-compose up -d

down-all:
	docker-compose down

restart-all:
	docker-compose restart

up-bot:
	docker-compose up -d telegram_bot

down-bot:
	docker-compose down telegram_bot

logs-bot:
	docker-compose logs telegram_bot | tail -300

restart-bot:
	docker-compose restart telegram_bot

sh-bot:
	docker-compose exec telegram_bot /bin/sh

up-redis:
	docker-compose up -d redis

down-redis:
	docker-compose down redis

logs-redis:
	docker-compose logs redis

restart-redis:
	docker-compose restart redis

sh-redis:
	docker-compose exec redis_container /bin/sh

up-loki:
	docker-compose up -d loki

down-loki:
	docker-compose down loki

logs-loki:
	docker-compose logs loki | tail -700

restart-loki:
	docker-compose restart loki

sh-loki:
	docker-compose exec loki /bin/sh

up-promtail:
	docker-compose up -d promtail

down-promtail:
	docker-compose down promtail

logs-promtail:
	docker-compose logs promtail | tail -700

restart-promtail:
	docker-compose restart promtail

sh-promtail:
	docker-compose exec promtail /bin/sh

up-grafana:
	docker-compose up -d grafana

down-grafana:
	docker-compose down grafana

logs-grafana:
	docker-compose logs grafana | tail -700

restart-grafana:
	docker-compose restart grafana

sh-grafana:
	docker-compose exec grafana /bin/sh

up-nginx:
	docker-compose up -d nginx

down-nginx:
	docker-compose down nginx

logs-nginx:
	docker-compose logs nginx | tail -700

restart-nginx:
	docker-compose restart nginx

sh-nginx:
	docker-compose exec nginx /bin/sh
