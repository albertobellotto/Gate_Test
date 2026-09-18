#!/usr/bin/env python3
"""Generate a unified feed dashboard from Twitter, Telegram and email."""

import sys
from pathlib import Path

from feeds.aggregator import collect_all
from render.html_renderer import render_html

try:
    from dotenv import load_dotenv
except ImportError:  # optional dependency, only needed for real API credentials
    load_dotenv = None

OUTPUT_PATH = Path(__file__).parent / "output" / "feed.html"


def main():
    if load_dotenv:
        load_dotenv()

    items = collect_all()
    html_output = render_html(items)

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    OUTPUT_PATH.write_text(html_output, encoding="utf-8")
    print(f"Generati {len(items)} elementi -> {OUTPUT_PATH}")

    if "--no-open" not in sys.argv:
        import webbrowser

        webbrowser.open(f"file://{OUTPUT_PATH.resolve()}")


if __name__ == "__main__":
    main()
