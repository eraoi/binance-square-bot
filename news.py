from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from html import unescape
import re
from typing import Iterable

import feedparser


@dataclass
class NewsItem:
    source: str
    title: str
    summary: str
    link: str
    published: str


FEEDS = [
    ("BBC World", "https://feeds.bbci.co.uk/news/world/rss.xml"),
    ("The Guardian World", "https://www.theguardian.com/world/rss"),
    ("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
    ("Cointelegraph", "https://cointelegraph.com/rss"),
]


def clean_html(value: str) -> str:
    text = unescape(value or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def fetch_feed(source: str, url: str, limit: int = 12) -> list[NewsItem]:
    feed = feedparser.parse(url)
    items: list[NewsItem] = []

    for entry in feed.entries[:limit]:
        title = clean_html(getattr(entry, "title", ""))
        summary = clean_html(
            getattr(entry, "summary", "")
            or getattr(entry, "description", "")
        )
        link = getattr(entry, "link", "")
        published = getattr(entry, "published", "") or getattr(entry, "updated", "")

        if title and link:
            items.append(
                NewsItem(
                    source=source,
                    title=title,
                    summary=summary[:700],
                    link=link,
                    published=published,
                )
            )
    return items


def fetch_all() -> list[NewsItem]:
    all_items: list[NewsItem] = []
    for source, url in FEEDS:
        try:
            all_items.extend(fetch_feed(source, url))
        except Exception as exc:
            print(f"[warn] failed feed: {source}: {exc}")
    return dedupe(all_items)


def dedupe(items: Iterable[NewsItem]) -> list[NewsItem]:
    seen = set()
    output = []
    for item in items:
        key = re.sub(r"\W+", "", item.title.lower())
        if key in seen:
            continue
        seen.add(key)
        output.append(item)
    return output


KEYWORDS = {
    "geopolitics": [
        "war", "missile", "ceasefire", "sanction", "iran", "israel",
        "russia", "ukraine", "china", "taiwan", "nato", "attack",
        "military", "election", "trump", "white house"
    ],
    "macro": [
        "fed", "inflation", "interest rate", "jobs", "gdp", "oil",
        "tariff", "treasury", "dollar", "recession", "central bank",
        "gold", "stocks", "market"
    ],
    "crypto": [
        "bitcoin", "btc", "ethereum", "eth", "crypto", "stablecoin",
        "etf", "binance", "coinbase", "solana", "token", "blockchain"
    ],
    "ai": [
        "artificial intelligence", " ai ", "openai", "nvidia",
        "google", "anthropic", "chip", "semiconductor", "data center"
    ],
}


def score_item(item: NewsItem) -> int:
    text = f" {item.title.lower()} {item.summary.lower()} "
    score = 0

    for category, words in KEYWORDS.items():
        for word in words:
            if word in text:
                score += 3 if category in ("crypto", "macro") else 2

    # Prefer substantive summaries and well-known sources.
    if len(item.summary) > 120:
        score += 1
    if item.source in ("BBC World", "The Guardian World", "CoinDesk"):
        score += 1

    return score


def select_top(items: list[NewsItem], limit: int = 8) -> list[NewsItem]:
    ranked = sorted(items, key=score_item, reverse=True)
    selected = []
    source_counts = {}

    for item in ranked:
        count = source_counts.get(item.source, 0)
        if count >= 3:
            continue
        selected.append(item)
        source_counts[item.source] = count + 1
        if len(selected) >= limit:
            break

    return selected
