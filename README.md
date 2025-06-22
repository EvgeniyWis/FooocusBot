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

---

## 🚀 Быстрый старт
```bash
make build
make up-bot
make logs-bot
```

## Использование Makefile

### Поддерживаются следующие команды:

<table>
  <tr>
    <th>Команда</th>
    <th>Описание</th>
  </tr>
  <tr>
    <td>make build</td>
    <td>Собрать Docker-образы</td>
  </tr>
  <tr>
    <td>make up-bot</td>
    <td>Запустить только бота</td>
  </tr>
  <tr>
    <td>make down-bot</td>
    <td>Остановить только бота</td>
  </tr>
  <tr>
    <td>make up-all</td>
    <td>Запустить все сервисы (бот, Redis)</td>
  </tr>
  <tr>
    <td>make down-all</td>
    <td>Остановить все сервисы</td>
  </tr>
  <tr>
    <td>make logs-bot</td>
    <td>Последние логи бота</td>
  </tr>
  <tr>
    <td>make logs-redis</td>
    <td>Последние логи Redis</td>
  </tr>
  <tr>
    <td>make sh-bot</td>
    <td>Войти внутрь контейнера бота</td>
  </tr>
  <tr>
    <td>make restart-bot</td>
    <td>Перезапустить бот</td>
  </tr>
</table>