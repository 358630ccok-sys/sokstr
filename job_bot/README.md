# Job Hunter Bot (`job_bot/`)

Telegram-бот/скрипт для автоматического поиска вакансий (**hh.ru API + LinkedIn guest/RSS fallback**) и отправки отчёта в Telegram.

## Возможности
- Поиск вакансий по ключевым запросам (DevOps/MLOps и др.)
- Форматирование результатов (название, зарплата, ссылка)
- Отправка отчёта в Telegram
- Запуск по расписанию (cron/systemd timer/контейнер) или вручную
- Конфигурация через переменные окружения (`.env`, без секретов в git)

## Структура
- `job_hunter.py` — основная логика сбора, обработки и отправки
- `requirements.txt` — зависимости Python
- `.env.example` — шаблон переменных окружения
- `Dockerfile` — контейнеризация

## Быстрый старт (локально)
```bash
cd job_bot
cp .env.example .env
# заполнить TG_TOKEN/TG_BOT_TOKEN, TELEGRAM_CHAT_ID (и при необходимости HH_TOKEN)

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python job_hunter.py
```

## Демо-режим (без сети и без отправки в Telegram)
Позволяет безопасно проверить формат отчёта и логику сборки сообщения:
```bash
python3 job_bot/job_hunter.py --demo

# сохранить demo-отчёт в файл (воспроизводимый артефакт)
python3 job_bot/job_hunter.py --demo --out docs/screenshots/telegram/job_bot_demo_YYYY-MM-DD.txt
```
Примеры вывода/артефактов:
- [`docs/screenshots/telegram/job_bot_demo.txt`](../docs/screenshots/telegram/job_bot_demo.txt)
- [`docs/screenshots/telegram/job_bot_demo_2026-11-20.txt`](../docs/screenshots/telegram/job_bot_demo_2026-11-20.txt)
- [`docs/screenshots/telegram/job_bot_sample_report.md`](../docs/screenshots/telegram/job_bot_sample_report.md)
- [`docs/screenshots/telegram/job_bot_anonymized_delivery_example.md`](../docs/screenshots/telegram/job_bot_anonymized_delivery_example.md) (обезличенный шаблон формата доставки)

> Для обычного запуска также доступно сохранение сформированного отчёта: `python3 job_bot/job_hunter.py --out /tmp/job_bot_report.txt` (без публикации секретов).

## Запуск в Docker
```bash
cd job_bot
docker build -t job-bot .
docker run --rm --env-file .env job-bot
```

## Пример формата отчёта (демо)
```text
🔎 Найдено вакансий: 5

1) DevOps Engineer — 180 000–250 000 RUB gross
   https://hh.ru/vacancy/...

2) MLOps Engineer — Не указана
   https://hh.ru/vacancy/...

...
```

## Проверка корректности (как валидируется результат)
- Сверка части результатов с источником (hh.ru/LinkedIn)
- Контроль ошибок запросов/парсинга в логах
- Проверка формата сообщения и доставки в Telegram
- Повторный прогон при изменениях (регресс-проверка)

## Безопасность
- Не коммитить `.env` и токены
- Передавать секреты только через переменные окружения/секрет-хранилище
- Ограничивать права бота/чата и доступ к runtime-окружению
