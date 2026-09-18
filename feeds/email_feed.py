"""Email fetcher.

Uses plain IMAP (stdlib) to read the most recent messages from INBOX. Works
with Gmail and most providers using an app password. Falls back to mock
data when EMAIL_IMAP_HOST / EMAIL_USER / EMAIL_PASSWORD are not set, or
when the connection fails.
"""

import email
import imaplib
import os
from datetime import datetime
from email.header import decode_header
from email.utils import mktime_tz, parsedate_tz

from .mock_data import get_mock_email
from .models import FeedItem


def _decode(value):
    if not value:
        return ""
    decoded = ""
    for text, encoding in decode_header(value):
        if isinstance(text, bytes):
            decoded += text.decode(encoding or "utf-8", errors="ignore")
        else:
            decoded += text
    return decoded


def _extract_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain" and not part.get("Content-Disposition"):
                charset = part.get_content_charset() or "utf-8"
                return part.get_payload(decode=True).decode(charset, errors="ignore")
        return ""
    charset = msg.get_content_charset() or "utf-8"
    payload = msg.get_payload(decode=True)
    return payload.decode(charset, errors="ignore") if payload else ""


def fetch(limit=10):
    host = os.getenv("EMAIL_IMAP_HOST")
    user = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    if not (host and user and password):
        return get_mock_email()

    items = []
    try:
        with imaplib.IMAP4_SSL(host) as imap:
            imap.login(user, password)
            imap.select("INBOX")
            _, data = imap.search(None, "ALL")
            message_ids = data[0].split()[-limit:]

            for msg_id in reversed(message_ids):
                _, msg_data = imap.fetch(msg_id, "(RFC822)")
                msg = email.message_from_bytes(msg_data[0][1])

                date_tuple = parsedate_tz(msg.get("Date"))
                timestamp = (
                    datetime.fromtimestamp(mktime_tz(date_tuple)) if date_tuple else datetime.now()
                )

                items.append(
                    FeedItem(
                        source="email",
                        author=_decode(msg.get("From")),
                        timestamp=timestamp,
                        title=_decode(msg.get("Subject")),
                        content=_extract_body(msg).strip()[:500],
                        meta={},
                    )
                )
    except (imaplib.IMAP4.error, OSError) as exc:
        print(f"[email] fetch failed, falling back to mock data: {exc}")
        return get_mock_email()

    return items or get_mock_email()
