# 🚀 Домашняя MLOps-лаборатория (sokstr)

Персональная инфраструктура для локального запуска LLM, генерации видео и RAG-систем.

## 🏗️ Архитектура
- **Гипервизор:** Proxmox VE (AMD RX 7700S + NVIDIA GTX 1660 SUPER)
- **Медиа-комбайн:** ComfyUI (Docker, ROCm) — Wan2.2 (Image-to-Video), SDXL Inpaint (CLIPSeg).
- **Оркестрация LLM:** Ollama (qwen2.5-coder, deepseek-r1) + OpenCode (Multi-agent: Cloud Planner + Local Executor).
- **RAG-система:** Dify + Obsidian Vault (105 заметок) + nomic-embed-text.
- **Автоматизация:** n8n (мониторинг, бэкапы).
- **Telegram-боты:** aiogram 3.x (@picturesok_bot, @obsidiansok_bot).

## 🧠 Экономия токенов (Multi-Agent)
Облачные LLM используются ТОЛЬКО для планирования. Вся рутина (чтение файлов, grep, bash) делегируется локальной модели `qwen2.5-coder:7b` на GTX 1660 SUPER.

## 🛠️ Стек
Proxmox, Docker, ROCm, Python, Ollama, ComfyUI, Dify, n8n, aiogram, Obsidian, Linux (Mint).

## 📊 Статус
- n8n: развернут в CT 134 (192.168.10.134:5678)
- Dify: VM 112 (192.168.10.112:3002), RAG по Obsidian Vault
- ComfyUI: Docker (ROCm), Wan2.2 TI2V-5B, SDXL Inpaint
- Ollama: CT 103 (AMD) + локально (GTX 1660)

## 📊 Мониторинг системы

Скрипт `sys_monitor.py` собирает CPU, RAM и свободное место на диске и шлёт в Telegram-бота. Запуск через Docker: docker build -t sys_monitor . && docker run -e TELEGRAM_BOT_TOKEN=xxx -e TELEGRAM_CHAT_ID=yyy sys_monitor.
EOF