"""Twitter/X fetcher.

Primary mode: pulls the latest tweets from an X List (a curated list of
accounts) via the Twitter API v2 `GET /2/lists/:id/tweets` endpoint. This
needs TWITTER_BEARER_TOKEN + TWITTER_LIST_ID. Note: the list-tweets
endpoint requires a paid API access tier (Basic or above) — it is not
available on the free tier.

Fallback mode: if no list ID is set but TWITTER_USERNAMES is, fetches each
account's own timeline individually instead.

Falls back to mock data when nothing is configured, or when any API call
fails.
"""

import os
from datetime import datetime

import requests

from .mock_data import get_mock_twitter
from .models import FeedItem

API_BASE = "https://api.twitter.com/2"


def _fetch_from_list(headers, list_id, limit=25):
    resp = requests.get(
        f"{API_BASE}/lists/{list_id}/tweets",
        headers=headers,
        params={
            "max_results": limit,
            "tweet.fields": "created_at,public_metrics,author_id",
            "expansions": "author_id",
            "user.fields": "username",
        },
        timeout=10,
    )
    resp.raise_for_status()
    payload = resp.json()
    usernames_by_id = {u["id"]: u["username"] for u in payload.get("includes", {}).get("users", [])}

    items = []
    for tweet in payload.get("data", []):
        username = usernames_by_id.get(tweet.get("author_id"), "unknown")
        items.append(
            FeedItem(
                source="twitter",
                author=f"@{username}",
                timestamp=datetime.fromisoformat(tweet["created_at"].replace("Z", "+00:00")),
                content=tweet["text"],
                url=f"https://twitter.com/{username}/status/{tweet['id']}",
                meta=tweet.get("public_metrics", {}),
            )
        )
    return items


def _fetch_from_usernames(headers, usernames):
    items = []
    for username in [u.strip().lstrip("@") for u in usernames.split(",") if u.strip()]:
        user_resp = requests.get(
            f"{API_BASE}/users/by/username/{username}", headers=headers, timeout=10
        )
        user_resp.raise_for_status()
        user_id = user_resp.json()["data"]["id"]

        tweets_resp = requests.get(
            f"{API_BASE}/users/{user_id}/tweets",
            headers=headers,
            params={"max_results": 5, "tweet.fields": "created_at,public_metrics"},
            timeout=10,
        )
        tweets_resp.raise_for_status()

        for tweet in tweets_resp.json().get("data", []):
            items.append(
                FeedItem(
                    source="twitter",
                    author=f"@{username}",
                    timestamp=datetime.fromisoformat(tweet["created_at"].replace("Z", "+00:00")),
                    content=tweet["text"],
                    url=f"https://twitter.com/{username}/status/{tweet['id']}",
                    meta=tweet.get("public_metrics", {}),
                )
            )
    return items


def fetch():
    bearer = os.getenv("TWITTER_BEARER_TOKEN")
    list_id = os.getenv("TWITTER_LIST_ID")
    usernames = os.getenv("TWITTER_USERNAMES")

    if not bearer or not (list_id or usernames):
        return get_mock_twitter()

    headers = {"Authorization": f"Bearer {bearer}"}
    try:
        if list_id:
            items = _fetch_from_list(headers, list_id)
        else:
            items = _fetch_from_usernames(headers, usernames)
    except requests.RequestException as exc:
        print(f"[twitter] fetch failed, falling back to mock data: {exc}")
        return get_mock_twitter()

    items.sort(key=lambda item: item.timestamp, reverse=True)
    return items or get_mock_twitter()
