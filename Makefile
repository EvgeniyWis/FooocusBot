export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

all: down-all build up-all up-bot down-bot logs-bot restart-bot sh-bot

build:
	docker-compose build

up-all:
	docker-compose up -d

down-all:
	docker-compose down

up-bot:
	docker-compose up -d telegram_bot

down-bot:
	docker-compose down telegram_bot

logs-bot:
	docker-compose logs telegram_bot | tail -700

logs-redis:
	docker-compose logs redis | tail -700

restart-bot:
	docker-compose restart telegram_bot

sh-bot:
	docker exec -it telegram_bot_container sh