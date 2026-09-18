"""Renders a list of FeedItem into a single, self-contained HTML dashboard.

Layout: one independent column per source (Twitter, Telegram, Email), side
by side on wide screens and stacked on narrow/mobile screens.
"""

import html
from datetime import date

SOURCE_LABELS = {
    "twitter": "Twitter / X",
    "telegram": "Telegram",
    "email": "Email",
}

SOURCE_ICONS = {
    "twitter": "𝕏",
    "telegram": "✈",
    "email": "✉",
}


def _format_timestamp(ts):
    today = date.today()
    if ts.date() == today:
        return f"Oggi · {ts.strftime('%H:%M')}"
    return ts.strftime("%d %b · %H:%M")


def _render_meta(item):
    parts = []
    if item.meta.get("likes") is not None:
        parts.append(f"♥ {item.meta['likes']:,}")
    if item.meta.get("retweets") is not None:
        parts.append(f"⟲ {item.meta['retweets']:,}")
    if item.meta.get("channel_members") is not None:
        parts.append(f"{item.meta['channel_members']:,} iscritti")
    return " · ".join(parts)


def _render_card(item):
    title_html = (
        f'<div class="card-title">{html.escape(item.title)}</div>' if item.title else ""
    )
    meta_str = _render_meta(item)
    meta_html = f'<span class="card-meta">{html.escape(meta_str)}</span>' if meta_str else ""
    link_html = (
        f'<a class="card-link" href="{html.escape(item.url)}" target="_blank" rel="noopener">Apri ↗</a>'
        if item.url
        else ""
    )

    return f"""
    <article class="card">
      <div class="card-header">
        <span class="card-author">{html.escape(item.author)}</span>
        <span class="card-time">{_format_timestamp(item.timestamp)}</span>
      </div>
      {title_html}
      <div class="card-content">{html.escape(item.content)}</div>
      <div class="card-footer">
        {meta_html}
        {link_html}
      </div>
    </article>
    """


def _render_column(source, items):
    if items:
        cards_html = "\n".join(_render_card(item) for item in items)
        search_empty_html = '<div class="column-empty-search">Nessun risultato.</div>'
    else:
        cards_html = '<div class="column-empty">Nessun elemento.</div>'
        search_empty_html = ""

    return f"""
    <section class="column" data-source="{source}">
      <div class="column-header">
        <span class="column-title">{SOURCE_ICONS.get(source, "")} {SOURCE_LABELS.get(source, source)}</span>
        <span class="column-count">{len(items)}</span>
      </div>
      <div class="column-body">
        {cards_html}
        {search_empty_html}
      </div>
    </section>
    """


def render_html(items):
    columns_by_source = {source: [i for i in items if i.source == source] for source in SOURCE_LABELS}
    columns_html = "\n".join(
        _render_column(source, columns_by_source[source]) for source in SOURCE_LABELS
    )

    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Feed Unificato</title>
<style>
  :root {{
    --bg: #f5f6f8;
    --surface: #ffffff;
    --text: #1a1d21;
    --text-muted: #6b7280;
    --border: #e5e7eb;
    --accent: #2563eb;
    --twitter: #1d9bf0;
    --telegram: #2aabee;
    --email: #d97706;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg: #0f1115;
      --surface: #1a1d23;
      --text: #e5e7eb;
      --text-muted: #9ca3af;
      --border: #2a2e37;
      --accent: #60a5fa;
    }}
  }}
  * {{ box-sizing: border-box; }}
  html, body {{
    margin: 0;
    height: 100%;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: var(--bg);
    color: var(--text);
  }}
  header {{
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 14px 20px;
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    align-items: center;
  }}
  h1 {{
    margin: 0;
    font-size: 1.3rem;
    white-space: nowrap;
  }}
  #search {{
    margin-left: auto;
    padding: 8px 12px;
    border-radius: 8px;
    border: 1px solid var(--border);
    background: var(--bg);
    color: var(--text);
    min-width: 220px;
    max-width: 100%;
  }}
  .board {{
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 16px;
    padding: 16px;
    align-items: start;
  }}
  .column {{
    display: flex;
    flex-direction: column;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
    height: calc(100vh - 90px);
  }}
  .column-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 14px;
    border-bottom: 1px solid var(--border);
    font-weight: 700;
    flex-shrink: 0;
  }}
  .column[data-source="twitter"] .column-header {{ border-top: 3px solid var(--twitter); }}
  .column[data-source="telegram"] .column-header {{ border-top: 3px solid var(--telegram); }}
  .column[data-source="email"] .column-header {{ border-top: 3px solid var(--email); }}
  .column-count {{
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--text-muted);
    background: var(--bg);
    border-radius: 999px;
    padding: 2px 9px;
  }}
  .column-body {{
    overflow-y: auto;
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    flex: 1;
  }}
  .card {{
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 14px;
  }}
  .card-header {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 8px;
    margin-bottom: 4px;
  }}
  .card-author {{
    font-weight: 600;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }}
  .card-time {{
    font-size: 0.75rem;
    color: var(--text-muted);
    white-space: nowrap;
  }}
  .card-title {{
    font-weight: 600;
    margin-bottom: 4px;
    color: var(--text);
  }}
  .card-content {{
    color: var(--text);
    line-height: 1.45;
    white-space: pre-line;
    font-size: 0.92rem;
  }}
  .card-footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 8px;
  }}
  .card-meta {{
    font-size: 0.76rem;
    color: var(--text-muted);
  }}
  .card-link {{
    font-size: 0.8rem;
    color: var(--accent);
    text-decoration: none;
  }}
  .column-empty,
  .column-empty-search {{
    text-align: center;
    color: var(--text-muted);
    padding: 24px 0;
    font-size: 0.88rem;
  }}
  .column-empty-search {{
    display: none;
  }}

  @media (max-width: 900px) {{
    .board {{
      grid-template-columns: 1fr;
    }}
    .column {{
      height: auto;
      max-height: 70vh;
    }}
    #search {{
      min-width: 0;
      flex: 1 1 100%;
      margin-left: 0;
    }}
  }}
</style>
</head>
<body>
<header>
  <h1>📡 Feed Unificato</h1>
  <input id="search" type="text" placeholder="Cerca in tutti i feed...">
</header>
<div class="board">
{columns_html}
</div>
<script>
  const search = document.getElementById("search");
  const columns = document.querySelectorAll(".column");

  function applyFilter() {{
    const query = search.value.trim().toLowerCase();
    columns.forEach(column => {{
      const cards = column.querySelectorAll(".card");
      let visibleCount = 0;
      cards.forEach(card => {{
        const matches = !query || card.textContent.toLowerCase().includes(query);
        card.style.display = matches ? "" : "none";
        if (matches) visibleCount++;
      }});
      const countEl = column.querySelector(".column-count");
      if (countEl) countEl.textContent = visibleCount;
      const emptySearchEl = column.querySelector(".column-empty-search");
      if (emptySearchEl) {{
        emptySearchEl.style.display = (query && visibleCount === 0 && cards.length > 0) ? "block" : "none";
      }}
    }});
  }}

  search.addEventListener("input", applyFilter);
</script>
</body>
</html>
"""
