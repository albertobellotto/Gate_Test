"""Telegram fetcher.

Reads the most recent posts from a single **public** Telegram channel via
its public web preview (https://t.me/s/<channel>) — no bot, token or admin
access required. Falls back to mock data when TELEGRAM_CHANNEL is not set,
or when the page can't be fetched/parsed (e.g. the channel is private or
doesn't exist).
"""

import html
import os
import re
from datetime import datetime

import requests

from .mock_data import get_mock_telegram
from .models import FeedItem

MESSAGE_RE = re.compile(
    r'<div class="tgme_widget_message_text[^"]*"[^>]*>(?P<text>.*?)</div>.*?'
    r'<a class="tgme_widget_message_date" href="(?P<link>[^"]+)">\s*'
    r'<time[^>]*datetime="(?P<dt>[^"]+)"',
    re.DOTALL,
)


def _strip_html(raw_text):
    text = re.sub(r"<br\s*/?>", "\n", raw_text)
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text).strip()


def fetch(limit=10):
    channel = os.getenv("TELEGRAM_CHANNEL")
    if not channel:
        return get_mock_telegram()

    channel = channel.strip().lstrip("@")
    items = []
    try:
        resp = requests.get(
            f"https://t.me/s/{channel}",
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        resp.raise_for_status()

        for match in MESSAGE_RE.finditer(resp.text):
            content = _strip_html(match.group("text"))
            if not content:
                continue
            timestamp = datetime.fromisoformat(match.group("dt")).astimezone().replace(tzinfo=None)
            items.append(
                FeedItem(
                    source="telegram",
                    author=f"@{channel}",
                    timestamp=timestamp,
                    content=content,
                    url=match.group("link"),
                    meta={},
                )
            )
    except (requests.RequestException, ValueError) as exc:
        print(f"[telegram] fetch failed, falling back to mock data: {exc}")
        return get_mock_telegram()

    if not items:
        return get_mock_telegram()

    items.sort(key=lambda item: item.timestamp, reverse=True)
    return items[:limit]
