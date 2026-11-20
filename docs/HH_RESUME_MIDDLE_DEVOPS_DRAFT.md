# HH.ru — черновик резюме (Middle DevOps / MLOps Engineer)

> **Назначение:** готовый текст для переноса в HH-профиль/резюме (заголовок, «О себе», опыт, навыки, ссылки).  
> **Основано на фактах:** `~/workspace/sokstr-mlops/resume.md`, портфолио, runbooks, кейсы и статус лабы в этом репозитории.  
> **Важно:** переносить только подтверждённые факты; метрики/сроки добавлять только если точно известны.

---

## 1) Заголовок (выбрать один)

- `DevOps / MLOps Engineer (Linux, Docker, Proxmox, K8s/k3s, Monitoring)`
- `Middle DevOps Engineer | Linux, Docker, CI/CD, Prometheus/Grafana, K8s`
- `DevOps Engineer (эксплуатация, автоматизация, AI-инфраструктура)`

**Желаемая зарплата:** от 120 000 ₽ (обсуждаемо)  
**Формат:** удалёнка (приоритет) / гибрид, Воронеж

---

## 2) Контакты и ссылки (обязательно добавить в HH)

- 📧 Email: `358630cok@mail.ru`
- 📱 Телефон: `+7 (960) 107-19-92`
- 💬 Telegram: `@sokstr` (https://t.me/sokstr)
- 🧑‍💻 GitHub/портфолио: `https://github.com/358630ccok-sys/sokstr`
- 🔗 LinkedIn: `https://www.linkedin.com/in/%D0%B0%D0%BB%D0%B5%D0%BA%D1%81%D0%B5%D0%B9-%D1%81%D0%B0%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9-34224a185/` (после доступности редактирования)

> В HH в блоке «Другие способы связи» добавить минимум **GitHub** и **Telegram**.

---

## 3) «Обо мне» (готовый текст)

```text
DevOps / MLOps Engineer (Middle). Эксплуатация Linux-инфраструктуры, контейнеризация, мониторинг, автоматизация и AI-инфраструктура. Production-поддержка в enterprise (Лента: инциденты, SLA, диагностика, документирование) + собственная платформа на Proxmox VE: 18+ сервисов (LXC/VM, Docker).

Практика и стек:
• Linux/Docker/Proxmox: развёртывание и сопровождение сервисов, диагностика (systemd, journalctl, логи, сеть, ресурсы)
• Наблюдаемость: Prometheus + Grafana, дашборды, healthchecks
• CI/CD и автоматизация: Git, GitLab CI/CD, Bash, Python, n8n, Telegram Bot API
• K8s/IaC (hands-on lab): k3s, Helm, Terraform, Ansible (деплой приложений/CronJob, воспроизводимая конфигурация)
• AI/MLOps: Ollama (локальный inference, GPU/ROCm), RAG (SQLite + embeddings), Dify, Qdrant, ComfyUI
• Надёжность/эксплуатация: runbooks, разбор инцидентов, PostgreSQL backup/restore с проверкой восстановления (pg_dump/pg_restore, практический restore-test PASS в изолированном окружении)

Портфолио, кейсы, runbooks, скриншоты: https://github.com/358630ccok-sys/sokstr
```

---

## 4) Опыт работы (перепаковка под DevOps/MLOps)

### 4.1 Инженер технической поддержки / Специалист по IT — Лента, федеральная розничная сеть
**Период:** 2023 — н.в. (уточнить фактические даты в HH при необходимости)  
**Фокус:** эксплуатация и поддержка ИТ-инфраструктуры в production-среде

- **Инцидент-менеджмент (SLA):** диагностика и восстановление работоспособности сервисов/оборудования, приоритизация и устранение сбоев в срок.
- **Диагностика:** анализ логов и симптомов, локализация первопричин проблем ПО/конфигурации/оборудования.
- **Эксплуатация и изменения:** участие в обновлениях, настройке и вводе в работу ПО/терминалов; проверка после изменений.
- **Коммуникация/эскалация:** передача сложных кейсов смежным командам с воспроизводимыми шагами и результатами диагностики.
- **Документирование:** фиксация решений и типовых кейсов для снижения повторяемости инцидентов.

### 4.2 DevOps / MLOps Engineer (проектная практика, self-operated) — Home-lab / Proxmox платформа
**Период:** 2025 — н.в.  
**Ссылка:** https://github.com/358630ccok-sys/sokstr

- **Инфраструктура:** спроектировал и сопровождаю платформу на Proxmox VE (**18+ сервисов**, LXC/VM, Docker): деплой, конфигурация, контроль ресурсов.
- **Мониторинг:** развернул Prometheus + Grafana, дашборды и healthchecks для контроля состояния инфраструктуры и сервисов.
- **Автоматизация:** n8n, Bash/Python, Telegram-интеграции; разработал **Job Hunter Bot** (hh.ru API + LinkedIn, aiogram, Docker, `--demo`, отчёт в Telegram).
- **CI/CD:** GitLab + GitLab Runner (базовые пайплайны build/test/deploy).
- **AI/MLOps:** Ollama (GPU/ROCm), RAG (SQLite + embeddings), Dify/Qdrant, ComfyUI.
- **K8s/IaC (hands-on):** k3s, Helm, Terraform, Ansible — развёртывание и отработка сценариев в lab-среде.
- **Надёжность:** runbooks (инциденты, PostgreSQL backup/restore), практический **restore-test PASS** в изолированном окружении.

### 4.3 Предыдущий опыт (кратко, без потери сути)
- **Связной** (2022–2023), инженер выездной техподдержки: диагностика на стороне клиента, восстановление работоспособности, настройка ПО/оборудования.
- **Системный администратор** (2021–2023): поддержка рабочих станций/серверов/сети, устранение неисправностей, взаимодействие с поставщиками.

> Рекомендация: в HH явно выделить блок 4.2 как релевантный DevOps/MLOps опыт (если формат резюме позволяет — как отдельное место опыта/проект).

---

## 5) Ключевые навыки (для поля «Навыки» в HH)

**Core DevOps / Ops:** Linux, Bash, systemd, journalctl, SSH, Networking (basics), Troubleshooting, Incident Management  
**Containers / Virtualization:** Docker, Docker Compose, Proxmox VE, LXC, VM  
**CI/CD / SCM:** Git, GitLab, GitLab CI/CD, GitLab Runner  
**Monitoring / Observability:** Prometheus, Grafana, Metrics, Dashboards, Healthchecks, Log analysis  
**IaC / Orchestration (hands-on):** Kubernetes, k3s, kubectl, Helm, Terraform, Ansible  
**Automation / Scripting:** Python, n8n, API integrations, Telegram Bot API  
**AI / MLOps:** Ollama, ROCm/GPU (basic), RAG, Embeddings, Dify, Qdrant, ComfyUI  
**Data / DB (ops basics):** SQL, PostgreSQL (backup/restore, pg_dump/pg_restore, restore verification)  
**Web/Infra services:** Nginx (reverse proxy), VPN (WireGuard/AmneziaWG, basic)

---

## 6) Что добавить в разделы HH (чтобы поднять видимость)

- **Портфолио:** ссылка на `https://github.com/358630ccok-sys/sokstr` + упоминание кейсов/runbooks/скриншотов.
- **Обо мне / достижения:** вынести 3–5 буллетов с результатами (18+ сервисов, мониторинг, автоматизация, restore-test PASS, k3s/Helm/Terraform/Ansible lab).
- **Курсы/проекты:** добавить практические проекты (Home-lab DevOps/MLOps, Job Hunter Bot, k8s/IaC lab) с ссылками на репозиторий.
- **Настройки поиска:** проверить желаемую должность/специализации (DevOps, SRE, MLOps, Platform), формат работы (удалёнка), ключевые слова в тексте.
- **Подтверждения навыков:** при возможности пройти релевантные (Linux/Docker/Git/Python/SQL/English).

---

## 7) Чек-лист перед сохранением на HH

- [ ] Заголовок соответствует целевым вакансиям (Middle DevOps/MLOps, не «общая поддержка»)
- [ ] В «Обо мне» есть GitHub и ключевой стек (Docker, CI/CD, Monitoring, K8s/IaC, PostgreSQL backup/restore)
- [ ] Опыт содержит достижения и артефакты, а не только обязанности
- [ ] Добавлены Telegram/GitHub/LinkedIn (где доступно)
- [ ] Нет секретов/внутренних данных/чувствительных деталей инфраструктуры
- [ ] Все указанные навыки/кейсы подтверждаемы (репозиторий, runbooks, demo)
