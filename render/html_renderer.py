"""Renders a list of FeedItem into a single, self-contained HTML dashboard."""

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
    meta_html = f'<div class="card-meta">{html.escape(meta_str)}</div>' if meta_str else ""
    link_html = (
        f'<a class="card-link" href="{html.escape(item.url)}" target="_blank" rel="noopener">Apri ↗</a>'
        if item.url
        else ""
    )

    return f"""
    <article class="card" data-source="{item.source}">
      <div class="card-header">
        <span class="badge badge-{item.source}">{SOURCE_ICONS.get(item.source, "")} {SOURCE_LABELS.get(item.source, item.source)}</span>
        <span class="card-time">{_format_timestamp(item.timestamp)}</span>
      </div>
      <div class="card-author">{html.escape(item.author)}</div>
      {title_html}
      <div class="card-content">{html.escape(item.content)}</div>
      <div class="card-footer">
        {meta_html}
        {link_html}
      </div>
    </article>
    """


def render_html(items):
    counts = {source: sum(1 for i in items if i.source == source) for source in SOURCE_LABELS}
    cards_html = "\n".join(_render_card(item) for item in items)

    filter_buttons = ['<button class="filter-btn active" data-filter="all">Tutti (' + str(len(items)) + ')</button>']
    for source, label in SOURCE_LABELS.items():
        filter_buttons.append(
            f'<button class="filter-btn" data-filter="{source}">{label} ({counts[source]})</button>'
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
  body {{
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: var(--bg);
    color: var(--text);
  }}
  header {{
    position: sticky;
    top: 0;
    z-index: 10;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 16px 20px;
  }}
  h1 {{
    margin: 0 0 12px 0;
    font-size: 1.4rem;
  }}
  .controls {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
  }}
  .filter-btn {{
    border: 1px solid var(--border);
    background: var(--surface);
    color: var(--text);
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 0.85rem;
    cursor: pointer;
  }}
  .filter-btn.active {{
    background: var(--accent);
    border-color: var(--accent);
    color: white;
  }}
  #search {{
    margin-left: auto;
    padding: 7px 12px;
    border-radius: 8px;
    border: 1px solid var(--border);
    background: var(--bg);
    color: var(--text);
    min-width: 200px;
  }}
  main {{
    max-width: 720px;
    margin: 0 auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }}
  .card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 16px;
  }}
  .card-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
  }}
  .badge {{
    font-size: 0.75rem;
    font-weight: 600;
    padding: 3px 9px;
    border-radius: 999px;
    color: white;
  }}
  .badge-twitter {{ background: var(--twitter); }}
  .badge-telegram {{ background: var(--telegram); }}
  .badge-email {{ background: var(--email); }}
  .card-time {{
    font-size: 0.78rem;
    color: var(--text-muted);
  }}
  .card-author {{
    font-weight: 600;
    margin-bottom: 2px;
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
  }}
  .card-footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 8px;
  }}
  .card-meta {{
    font-size: 0.78rem;
    color: var(--text-muted);
  }}
  .card-link {{
    font-size: 0.82rem;
    color: var(--accent);
    text-decoration: none;
  }}
  .empty-state {{
    text-align: center;
    color: var(--text-muted);
    padding: 40px 0;
  }}
</style>
</head>
<body>
<header>
  <h1>📡 Feed Unificato</h1>
  <div class="controls">
    {"".join(filter_buttons)}
    <input id="search" type="text" placeholder="Cerca...">
  </div>
</header>
<main id="feed">
{cards_html}
<div class="empty-state" id="empty-state" style="display:none;">Nessun risultato.</div>
</main>
<script>
  const buttons = document.querySelectorAll(".filter-btn");
  const search = document.getElementById("search");
  const cards = document.querySelectorAll(".card");
  const emptyState = document.getElementById("empty-state");
  let currentFilter = "all";

  function applyFilters() {{
    const query = search.value.trim().toLowerCase();
    let visibleCount = 0;
    cards.forEach(card => {{
      const matchesSource = currentFilter === "all" || card.dataset.source === currentFilter;
      const matchesQuery = !query || card.textContent.toLowerCase().includes(query);
      const visible = matchesSource && matchesQuery;
      card.style.display = visible ? "" : "none";
      if (visible) visibleCount++;
    }});
    emptyState.style.display = visibleCount === 0 ? "block" : "none";
  }}

  buttons.forEach(btn => {{
    btn.addEventListener("click", () => {{
      buttons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentFilter = btn.dataset.filter;
      applyFilters();
    }});
  }});

  search.addEventListener("input", applyFilters);
</script>
</body>
</html>
"""
