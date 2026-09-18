from . import email_feed, telegram_feed, twitter_feed


def collect_all():
    """Fetch every source and return a single list sorted by recency."""
    items = []
    items.extend(twitter_feed.fetch())
    items.extend(telegram_feed.fetch())
    items.extend(email_feed.fetch())
    items.sort(key=lambda item: item.timestamp, reverse=True)
    return items
