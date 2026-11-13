#!/usr/bin/env python3
import asyncio
import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List

import feedparser
import requests
from aiogram import Bot
from bs4 import BeautifulSoup
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger("job_hunter")

BASE_DIR = Path(__file__).resolve().parent
RESUME_PATH = (BASE_DIR / ".." / "resume.md").resolve()
load_dotenv(BASE_DIR / ".env")


def get_config() -> Dict[str, str]:
    tg_token = os.getenv("TG_TOKEN") or os.getenv("TG_BOT_TOKEN") or ""
    hh_token = os.getenv("HH_TOKEN") or ""
    chat_id = os.getenv("TELEGRAM_CHAT_ID") or ""
    if not tg_token or not chat_id:
        logger.error("Missing TG_TOKEN/TG_BOT_TOKEN or TELEGRAM_CHAT_ID")
    return {"tg_token": tg_token, "hh_token": hh_token, "chat_id": chat_id}


def read_resume_keywords() -> List[str]:
    defaults = ["MLOps", "DevOps", "Python", "Linux", "Proxmox", "Docker", "Ollama", "RAG"]
    try:
        text = RESUME_PATH.read_text(encoding="utf-8", errors="ignore")
        found = [k for k in defaults if re.search(rf"\b{re.escape(k)}\b", text, re.I)]
        keywords = found or defaults
        logger.info("Resume keywords: %s", ", ".join(keywords))
        return keywords
    except Exception as e:
        logger.warning("Cannot read resume.md (%s), using defaults", e)
        return defaults


def format_salary(salary: Any) -> str:
    if not salary:
        return "Не указана"
    if isinstance(salary, dict):
        frm = salary.get("from")
        to = salary.get("to")
        cur = salary.get("currency") or ""
        gross = "gross" if salary.get("gross") else "net"
        parts = []
        if frm and to:
            parts.append(f"{frm}-{to}")
        elif frm:
            parts.append(f"от {frm}")
        elif to:
            parts.append(f"до {to}")
        if cur:
            parts.append(cur)
        if parts:
            parts.append(gross)
            return " ".join(str(p) for p in parts)
    return str(salary)


def fetch_hh_vacancies(hh_token: str) -> List[Dict[str, str]]:
    url = "https://api.hh.ru/vacancies?text=MLOps+OR+DevOps&area=113&per_page=5"
    headers = {"User-Agent": "job-hunter-bot/1.0"}
    if hh_token:
        headers["Authorization"] = f"Bearer {hh_token}"
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        results = []
        for item in items:
            results.append({
                "title": item.get("name") or "Без названия",
                "salary": format_salary(item.get("salary")),
                "url": item.get("alternate_url") or item.get("url") or "",
            })
        return results
    except Exception as e:
        logger.warning("hh.ru request failed: %s", e)
        return []


def fetch_linkedin_jobs() -> List[Dict[str, str]]:
    # Try guest jobs endpoint and parse minimal info; fallback to stub on failure/block
    url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=MLOps%20OR%20DevOps&location=Worldwide&start=0"
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.select("li")[:5]
        jobs = []
        for card in cards:
            title_el = card.select_one(".base-search-card__title") or card.select_one("h3")
            link_el = card.select_one("a.base-card__full-link") or card.select_one("a")
            if not title_el or not link_el:
                continue
            title = title_el.get_text(strip=True)
            link = link_el.get("href", "").split("?")[0]
            jobs.append({"title": title or "LinkedIn vacancy", "salary": "Не указана", "url": link})
        if jobs:
            return jobs
    except Exception as e:
        logger.warning("LinkedIn fetch/parse failed: %s", e)

    # RSS fallback attempt (may be unavailable)
    try:
        rss_url = "https://www.linkedin.com/jobs/search/?keywords=MLOps%20DevOps&f_TPR=r86400&position=1&pageNum=0&format=rss"
        feed = feedparser.parse(rss_url)
        jobs = []
        for entry in getattr(feed, "entries", [])[:5]:
            jobs.append({
                "title": entry.get("title", "LinkedIn vacancy"),
                "salary": "Не указана",
                "url": entry.get("link", ""),
            })
        if jobs:
            return jobs
    except Exception as e:
        logger.warning("LinkedIn RSS failed: %s", e)

    return [{"title": "LinkedIn: недоступно (RSS/парсинг)", "salary": "-", "url": ""}]


def build_message(hh_jobs: List[Dict[str, str]], li_jobs: List[Dict[str, str]]) -> str:
    lines = ["Вакансии hh.ru:"]
    if hh_jobs:
        for j in hh_jobs:
            lines.append(f"- {j['title']}, {j['salary']}, {j['url']}")
    else:
        lines.append("- Нет данных (ошибка запроса или пусто)")
    lines.append("")
    lines.append("Вакансии LinkedIn:")
    if li_jobs:
        for j in li_jobs:
            parts = [j.get("title", ""), j.get("salary", "-")]
            if j.get("url"):
                parts.append(j["url"])
            lines.append("- " + ", ".join([p for p in parts if p]))
    else:
        lines.append("- LinkedIn: недоступно (RSS/парсинг)")
    msg = "\n".join(lines)
    # Telegram message limit safety
    return msg[:3900]


async def send_telegram(token: str, chat_id: str, text: str) -> None:
    bot = Bot(token=token)
    try:
        await bot.send_message(chat_id=chat_id, text=text)
        logger.info("Sent Telegram message")
    finally:
        await bot.session.close()


async def main() -> None:
    cfg = get_config()
    read_resume_keywords()  # informs logs/search context
    hh_jobs = fetch_hh_vacancies(cfg["hh_token"])
    li_jobs = fetch_linkedin_jobs()
    message = build_message(hh_jobs, li_jobs)

    if not cfg["tg_token"] or not cfg["chat_id"]:
        logger.error("Cannot send Telegram: missing TG_TOKEN/TELEGRAM_CHAT_ID. Message:\n%s", message)
        return
    try:
        await send_telegram(cfg["tg_token"], cfg["chat_id"], message)
    except Exception as e:
        logger.error("Telegram send failed: %s", e)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error("Fatal error: %s", e)
        raise SystemExit(0)
