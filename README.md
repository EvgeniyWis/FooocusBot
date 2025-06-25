# FocuuusBot – Telegram-бот с генерацией изображений по API

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![aiogram v3](https://img.shields.io/badge/aiogram-v3.x-green.svg)](https://docs.aiogram.dev/en/latest/)
[![Dockerized](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)
[![Redis](https://img.shields.io/badge/redis-used-red)](https://redis.io/)

Бот разработан по техническому заданию заказчика и предназначен для генерации набора изображений по одному промпту, с поддержкой AI-интеграций (RunPod, Kling), обработкой изображений (в том числе через FaceFusion), асинхронной очередью задач и системой ролей.

---

## Функции

- Поддержка нескольких AI-генераторов по API
- Асинхронная очередь задач с восстановлением через Redis
- Модуль FaceFusion (Docker-интеграция с другим контейнером)
- Разграничение доступа: пользователи, админы, девелоперы
- Поддержка разных режимов генерации (mock/test/dev)
- Интеграция с внешним FaceFusion контейнером через `docker exec`
- Система логирования с бэкапами и просмотром логов через Grafana (Loki/Promtail)
- Безопасный доступ к Grafana через nginx с Basic Auth

---

## 🚀 Быстрый старт
```bash
make build
make up-all
make logs-bot
```

## Использование Makefile

- `make up-all` — запустить все сервисы
- `make down-all` — остановить все сервисы
- `make up-bot` / `make down-bot` — запустить/остановить только Telegram-бота
- `make up-redis` / `make down-redis` — запустить/остановить Redis
- `make up-loki` / `make down-loki` — запустить/остановить Loki
- `make up-promtail` / `make down-promtail` — запустить/остановить Promtail
- `make up-grafana` / `make down-grafana` — запустить/остановить Grafana
- `make up-nginx` / `make down-nginx` — запустить/остановить nginx (прокси)
- `make logs-<service>` — посмотреть логи сервиса (например, `make logs-bot`)
- `make restart-<service>` — перезапустить сервис
- `make sh-<service>` — войти внутрь контейнера (bash/sh)

## Доступ к логам и Grafana

- Просмотр логов и мониторинг осуществляется через Grafana, которая доступна только через nginx-прокси по адресу:  
  `http://localhost:8080/grafana/`  
  (или по вашему домену, если настроен)
- Для доступа требуется логин/пароль (basic auth), который хранится в файле `nginx/.htpasswd`.
- Прямого доступа к Grafana, Loki и Promtail снаружи нет — только через nginx.

## Генерация .htpasswd для nginx

Для создания пользователя и пароля для доступа к Grafana через nginx:
```sh
docker run --rm --entrypoint htpasswd httpd:2 -Bbn <user> <password> > ./nginx/.htpasswd
```

---

