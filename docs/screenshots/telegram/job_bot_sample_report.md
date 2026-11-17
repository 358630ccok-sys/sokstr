# Job Hunter — пример отчёта (обезличенный формат)

Ниже пример структуры Telegram-отчёта, который формирует `job_bot/job_hunter.py` (данные примерные/обезличенные, для демонстрации формата).

```text
Вакансии hh.ru:
- DevOps Engineer (Remote), 180 000-250 000 RUB gross, https://hh.ru/vacancy/123456
- MLOps Engineer, от 220 000 RUB net, https://hh.ru/vacancy/234567
- Site Reliability Engineer, Не указана, https://hh.ru/vacancy/345678

Вакансии LinkedIn:
- DevOps Engineer (Kubernetes), Не указана, https://www.linkedin.com/jobs/view/1111111111
- AI Infrastructure Engineer, Не указана, https://www.linkedin.com/jobs/view/2222222222
```

## Как воспроизвести безопасно
```bash
python3 job_bot/job_hunter.py --demo
```
- Без сетевых запросов к источникам (в demo-режиме)
- Без отправки сообщений в Telegram
- Без использования реальных токенов/чат-ID
