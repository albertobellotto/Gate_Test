"""Telegram fetcher.

Uses the Telegram Bot API's getUpdates method to read the most recent
channel posts / messages the configured bot has visibility on (the bot
must be added as an admin to any channel you want to track). Falls back to
mock data when TELEGRAM_BOT_TOKEN is not set, or when the API call fails.
"""

import os
from datetime import datetime

import requests

from .mock_data import get_mock_telegram
from .models import FeedItem


def fetch():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        return get_mock_telegram()

    items = []
    try:
        resp = requests.get(f"https://api.telegram.org/bot{token}/getUpdates", timeout=10)
        resp.raise_for_status()
        for update in resp.json().get("result", []):
            post = update.get("channel_post") or update.get("message")
            if not post or "text" not in post:
                continue
            chat = post.get("chat", {})
            items.append(
                FeedItem(
                    source="telegram",
                    author=chat.get("title") or chat.get("username") or "Telegram",
                    timestamp=datetime.fromtimestamp(post["date"]),
                    content=post["text"],
                    meta={},
                )
            )
    except requests.RequestException as exc:
        print(f"[telegram] fetch failed, falling back to mock data: {exc}")
        return get_mock_telegram()

    return items or get_mock_telegram()
