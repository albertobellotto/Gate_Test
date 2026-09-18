"""Twitter/X fetcher.

Uses the Twitter API v2 (app-only auth) to pull the latest tweets from a
configurable list of usernames. Falls back to mock data when
TWITTER_BEARER_TOKEN / TWITTER_USERNAMES are not set, or when the API call
fails for any reason.
"""

import os
from datetime import datetime

import requests

from .mock_data import get_mock_twitter
from .models import FeedItem

API_BASE = "https://api.twitter.com/2"


def fetch():
    bearer = os.getenv("TWITTER_BEARER_TOKEN")
    usernames = os.getenv("TWITTER_USERNAMES")
    if not bearer or not usernames:
        return get_mock_twitter()

    headers = {"Authorization": f"Bearer {bearer}"}
    items = []
    try:
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
                        timestamp=datetime.fromisoformat(
                            tweet["created_at"].replace("Z", "+00:00")
                        ),
                        content=tweet["text"],
                        url=f"https://twitter.com/{username}/status/{tweet['id']}",
                        meta=tweet.get("public_metrics", {}),
                    )
                )
    except requests.RequestException as exc:
        print(f"[twitter] fetch failed, falling back to mock data: {exc}")
        return get_mock_twitter()

    return items or get_mock_twitter()
