from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class FeedItem:
    """A single normalized entry coming from any information source."""

    source: str  # "twitter" | "telegram" | "email"
    author: str
    timestamp: datetime
    content: str
    title: Optional[str] = None
    url: Optional[str] = None
    meta: dict = field(default_factory=dict)
