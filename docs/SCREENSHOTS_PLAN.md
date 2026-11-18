# 📸 План скриншотов для портфолио

> Скриншоты — визуальное доказательство компетенций. Добавляйте в `docs/screenshots/` и вставляйте в README/LinkedIn.

---

## 📁 Структура папок

```
docs/
├── screenshots/
│   ├── grafana/          # Дашборды мониторинга
│   ├── n8n/              # Workflow автоматизации
│   ├── proxmox/          # Панель управления CT/VM
│   ├── ai/               # ComfyUI, Dify, Ollama
│   ├── terminal/         # Выводы команд, логи
│   └── telegram/         # Отчёты ботов
├── architecture/         # Схемы (draw.io, Excalidraw, PNG)
└── runbooks/             # Инструкции по инцидентам
```

---

## 📋 Чеклист скриншотов (приоритет)

### 🔴 Критичные (сделать в первую очередь)

| # | Скриншот | Что показывает | Где сохранить | Подпись для README/LinkedIn |
|---|---|---|---|---|
| 1 | **Grafana дашборд** `ai-monitoring-2026` | Мониторинг инфраструктуры и AI-метрик (CPU, RAM, GPU, Ollama) | `screenshots/grafana/ai-monitoring.png` | «Наблюдаемость: Prometheus + Grafana, контроль состояния 18+ сервисов» |
| 2 | **Proxmox панель** — список CT/VM | Управление виртуализацией, 18+ сервисов | `screenshots/proxmox/cluster-overview.png` | «Production home-lab: Proxmox VE, LXC/VM, Docker» |
| 3 | **n8n workflow** — healthcheck или Career Agent | Автоматизация, оркестрация, интеграции | `screenshots/n8n/workflow-healthcheck.png` | «Автоматизация процессов: n8n workflow, healthchecks» |
| 4 | **Telegram отчёт** от job_bot | Автоматический сбор вакансий | `screenshots/telegram/job-bot-report.png` | «Job Hunter Bot: автоматический сбор вакансий hh.ru/LinkedIn» |

### 🟡 Важные (сделать на второй день)

| # | Скриншот | Что показывает | Где сохранить | Подпись |
|---|---|---|---|---|
| 5 | **Ollama ps / GPU** | Локальный LLM inference на GPU | `screenshots/terminal/ollama-gpu.png` | «AI-инфраструктура: Ollama, GPU inference (ROCm)» |
| 6 | **ComfyUI pipeline** | Генерация изображений, SDXL + IPAdapter | `screenshots/ai/comfyui-pipeline.png` | «MLOps: ComfyUI, SDXL, IPAdapter FaceID» |
| 7 | **Dify интерфейс** | AI-приложения, RAG | `screenshots/ai/dify-apps.png` | «AI-платформа: Dify, RAG, векторный поиск» |
| 8 | **Терминал** — `docker ps` | Контейнеры в эксплуатации | `screenshots/terminal/docker-ps.png` | «Production-контейнеры: Docker, эксплуатация сервисов» |

### 🟢 Дополнительные (по возможности)

| # | Скриншот | Что показывает | Где сохранить |
|---|---|---|---|
| 9 | **GitLab CI pipeline** | CI/CD автоматизация | `screenshots/ci-cd/gitlab-pipeline.png` |
| 10 | **Nginx config / proxy** | Reverse proxy, маршрутизация | `screenshots/terminal/nginx-config.png` |
| 11 | **Prometheus targets** | Сбор метрик, targets up/down | `screenshots/grafana/prometheus-targets.png` |
| 12 | **Архитектурная схема** | Связи сервисов, сети | `architecture/infra-diagram.png` |

---

## 📐 Требования к скриншотам

| Параметр | Рекомендация |
|---|---|
| **Разрешение** | 1920x1080 или выше (для читаемости) |
| **Формат** | PNG (для интерфейсов), JPG (для фото) |
| **Без секретов** | Убедитесь, что токены, пароли, IP-адреса внутренних сервисов не видны (или замазаны) |
| **Подписи** | Добавляйте краткую подпись: что видно и какую проблему решает |
| **Обновляемость** | Дата скриншота не должна быть старше 3 месяцев |

---

## 🖼️ Как сделать скриншоты (команды)

### Linux (локально)
```bash
# Скриншот всего экрана
gnome-screenshot -f screenshot.png

# Скриншот выделенной области
gnome-screenshot -a -f screenshot.png

# Скриншот окна
gnome-screenshot -w -f screenshot.png
```

### Через SSH (Proxmox / серверы)
```bash
# Скриншот терминала (текстовый вывод)
ssh proxmox "docker ps" > docs/screenshots/terminal/docker-ps.txt

# Скриншот веб-интерфейса (если есть браузер на сервере)
ssh proxmox "chromium --headless --screenshot=/tmp/grafana.png http://192.168.10.106:3000" 2>/dev/null
scp proxmox:/tmp/grafana.png docs/screenshots/grafana/
```

### Через браузер (рекомендуется для веб-интерфейсов)
1. Откройте Grafana/n8n/Proxmox в браузере
2. Нажмите `Ctrl+Shift+S` (Firefox) или используйте расширение
3. Сохраните в `docs/screenshots/<категория>/`

---

## 📝 Как вставить скриншот в README

```markdown
### 📊 Мониторинг (Grafana)
![Grafana Dashboard](docs/screenshots/grafana/ai-monitoring.png)
*Наблюдаемость: Prometheus + Grafana, контроль состояния 18+ сервисов*
```

---

## ✅ Итоговый чеклист

- [ ] Создать папки `docs/screenshots/*`
- [ ] Сделать 4 критичных скриншота (Grafana, Proxmox, n8n, Telegram)
- [ ] Сделать 4 важных скриншота (Ollama, Dify, Docker) — **ComfyUI готов:** `screenshots/ai/comfyui-pipeline.png`
- [ ] Проверить отсутствие секретов на всех скриншотах
- [ ] Добавить скриншоты в README.md
- [ ] Добавить 1-2 скриншота в LinkedIn-посты
- [ ] Закоммитить и запушить в GitHub

## ⚠️ Безопасность
- **НЕ** показывайте: токены, пароли, внутренние IP (если публично), персональные данные
- **МОЖНО** показывать: дашборды, схемы, метрики (без секретов), терминальный вывод (без токенов)
- При сомнении — замазывайте или обрезайте
