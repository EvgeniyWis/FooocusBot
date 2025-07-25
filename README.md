# FooocusBot – Telegram-бот для генерации изображений

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![aiogram v3](https://img.shields.io/badge/aiogram-v3.x-green.svg)](https://docs.aiogram.dev/en/latest/)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)
[![Redis](https://img.shields.io/badge/redis-used-red)](https://redis.io/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Бот для генерации изображений по промптам с поддержкой AI-интеграций, асинхронной очередью задач и системой ролей.

## 🚀 Возможности

- 🖼️ Генерация наборов изображений по одному промпту
- 🤖 Поддержка нескольких AI-генераторов (RunPod, Kling)
- 🔄 Асинхронная очередь задач с восстановлением через Redis
- 👤 Обработка лиц через FaceFusion (интеграция с Docker)
- 👥 Разграничение доступа: пользователи, админы, девелоперы
- 📊 Мониторинг через Grafana с Loki/Promtail
- 🔒 Защищенный доступ к админ-панели

## 🛠️ Требования

- Ubuntu 20.04/22.04
- Docker 20.10.0+
- Docker Compose 2.0.0+
- 16 CPU / 20 ГБ RAM / 50+ ГБ SSD

## 🚀 Установка

### 1. Обновление системы и установка необходимых пакетов
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git make htop
```

### 2. Установка Docker
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker

# Установка Docker Compose
DOCKER_COMPOSE_VERSION="2.38.2"
sudo curl -SL https://github.com/docker/compose/releases/download/v${DOCKER_COMPOSE_VERSION}/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Проверка установки
docker --version
docker-compose --version
```

### 3. Установка facefusion-docker

1. Создайте директорию для проекта и перейдите в неё:
```bash
mkdir -p ~/bot
cd ~/bot
```

2. Клонируйте репозиторий facefusion-docker:
```bash
git clone https://github.com/macalistervadim/facefusion-docker.git
cd facefusion-docker
```

3. Запустите контейнер:
```bash
docker-compose -f docker-compose.cpu.yml up -d --build      
```

4. Проверьте, что контейнер запустился:
```bash
docker ps
```

5. Вернитесь в родительскую директорию:
```bash
cd ..
```

### 4. Клонирование репозитория FooocusBot
```bash
git clone https://github.com/EvgeniyWis/FooocusBot
cd FooocusBot
```

### 5. Настройка окружения
```bash
cp .env.example .env
nano .env  # Настройте переменные окружения
```

### 7. Настройка аутентификации Grafana
```bash
docker run --rm --entrypoint htpasswd httpd:2 -Bbn admin your-password > ./nginx/.htpasswd
```

## 🚀 Запуск

```bash
make build        # Сборка контейнеров
make up-all       # Запуск всех сервисов
make logs-bot     # Просмотр логов бота
```

## 📊 Мониторинг

Доступ к Grafana: http://localhost:8080/grafana/
- Логин/пароль: из файла .htpasswd
- Источник логов: Loki

## 🛠️ Управление

| Команда | Описание |
|---------|----------|
| `make up-all` | Запуск всех сервисов |
| `make down-all` | Остановка всех сервисов |
| `make logs-bot` | Просмотр логов бота |
| `make sh-bot` | Вход в контейнер бота |
| `make restart-bot` | Перезапуск бота |
к остальным сервисам по аналогии (up-*, down-*, logs-*, sh-*, restart-*).


## 🔒 Безопасность

- 🔐 Защита Grafana через nginx с basic auth
- 🔒 Закрытый доступ к Loki и Promtail
- 📊 Ротация логов через TimedRotatingFileHandler

## 📚 Документация

- [Aiogram v3](https://docs.aiogram.dev/en/latest/)
- [RunPod API](https://docs.runpod.io)
- [FaceFusion](https://github.com/facefusion/facefusion)
- [Grafana Loki](https://grafana.com/oss/loki/)

