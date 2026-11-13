# Архитектура домашней MLOps-лаборатории

## Схема потока данных

```
Cloud (OpenCode planner) 
  -> Local Executor (qwen2.5-coder:7b на GTX 1660) 
     -> n8n (автоматизация, мониторинг)
        -> Dify (RAG по Obsidian Vault)
           -> Telegram-боты (@obsidiansok_bot)
```

## Компоненты

### 1. Гипервизор (Proxmox VE)
- Хост: AMD RX 7700S (8 ГБ VRAM) + NVIDIA GTX 1660 SUPER (6 ГБ VRAM)
- CT 103: Ollama (AMD ROCm) — qwen2.5-coder:7b, deepseek-r1:7b, nomic-embed-text
- VM 112: Dify (RAG, Knowledge Base "Obsidian Vault", 105 документов)
- CT 134: n8n (автоматизация, мониторинг)
- VM 111: Docker host

### 2. Локальный AI (OpenCode Multi-Agent)
- **Cloud Planner:** облачная LLM для планирования и сложного кода
- **Local Executor:** qwen2.5-coder:7b на GTX 1660 (context 4096, OLLAMA_FLASH_ATTENTION=1, OLLAMA_KV_CACHE_TYPE=q8_0)
- Вся рутина (ls, cat, grep, bash) делегируется локальной модели

### 3. Медиа (ComfyUI)
- Docker контейнер (ROCm)
- Wan2.2 TI2V-5B (Image-to-Video)
- SDXL Inpaint (CLIPSeg, кисть по тексту)
- IPAdapter FaceID (портреты)

### 4. RAG (Dify + Obsidian)
- Dify: Chatflow app "Obsidian Chat" с Knowledge Retrieval
- Obsidian Vault: 105 заметок (синхронизация через SFTP + rsync таймер)
- Embedding: nomic-embed-text (Ollama)
- LLM: deepseek-r1:7b

### 5. Telegram-боты
- @picturesok_bot: видео/inpaint (ComfyUI)
- @obsidiansok_bot: RAG-чат по Obsidian (Dify)
- aiogram 3.x, фильтр по @sokstr

### 6. Сетевая инфраструктура
- Proxmox: 192.168.10.100
- Основной ПК (Mint): 192.168.10.84 / 192.168.20.121
- ТВ-ПК 1 (Зал): 192.168.20.211 (x11vnc, Remmina)
- ТВ-ПК 2 (Кухня): 192.168.20.233 (x11vnc, Remmina)
- OpenWrt роутер: 192.168.10.1 / 192.168.20.1
EOF