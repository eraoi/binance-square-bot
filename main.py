from __future__ import annotations

import argparse
import os
import sys

from .news import fetch_all, select_top
from .summarizer import build_post
from .binance_square import publish_text, BinanceSquareError


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate post but do not publish",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    print("[1/4] Fetching news...")
    items = fetch_all()
    if not items:
        print("[error] No news fetched.")
        return 2

    print(f"[2/4] Selecting top stories from {len(items)} items...")
    selected = select_top(items, limit=8)

    print("[3/4] Building Binance Square post...")
    post = build_post(selected).strip()

    if not post:
        print("[error] Empty post.")
        return 3

    print("\n========== POST PREVIEW ==========\n")
    print(post)
    print("\n========== END PREVIEW ==========\n")

    if args.dry_run or os.getenv("DRY_RUN", "").lower() in {"1", "true", "yes"}:
        print("[dry-run] Skipping publish.")
        return 0

    print("[4/4] Publishing to Binance Square...")
    try:
        content_id, link = publish_text(post)
    except BinanceSquareError as exc:
        print(f"[error] {exc}")
        return 4

    print("[success] Published.")
    if content_id:
        print(f"ID: {content_id}")
    if link:
        print(f"Link: {link}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
