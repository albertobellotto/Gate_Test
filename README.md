# Feed Unificato

Un'unica dashboard locale che aggrega i tuoi flussi informativi — Twitter/X,
canali Telegram ed email — in una sola pagina HTML, ordinata cronologicamente
e filtrabile per fonte.

## Avvio rapido (dati di esempio)

Senza alcuna configurazione, il progetto genera la dashboard con dati mock
realistici per ogni fonte, utile per vedere subito come funziona:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Verrà creato `output/feed.html` e aperto automaticamente nel browser
(usa `python main.py --no-open` per saltare l'apertura automatica).

## Collegare le fonti reali

Copia `.env.example` in `.env` e compila solo le sezioni che ti interessano.
Le fonti non configurate continuano a mostrare dati di esempio.

- **Twitter/X**: richiede un `TWITTER_BEARER_TOKEN` (developer.twitter.com) e
  la lista di username da seguire in `TWITTER_USERNAMES`.
- **Telegram**: richiede un `TELEGRAM_BOT_TOKEN` creato con @BotFather. Il bot
  deve essere aggiunto come admin ai canali che vuoi monitorare.
- **Email**: richiede host IMAP, utente e password (per Gmail, usa una
  "App Password" con la verifica in due passaggi attiva).

Rilancia `python main.py` ogni volta che vuoi un aggiornamento del feed.

## Struttura del progetto

```
feeds/
  models.py          # modello dati unificato (FeedItem)
  mock_data.py        # dati di esempio per ogni fonte
  twitter_feed.py      # fetch reale + fallback mock
  telegram_feed.py     # fetch reale + fallback mock
  email_feed.py         # fetch reale (IMAP) + fallback mock
  aggregator.py         # unisce e ordina tutte le fonti
render/
  html_renderer.py     # genera la dashboard HTML (badge, filtri, ricerca)
main.py                # entry point
```

## Estendere con nuove fonti

Per aggiungere una nuova fonte (es. RSS, Slack, Mastodon):

1. Crea `feeds/<nome>_feed.py` con una funzione `fetch()` che ritorna una
   lista di `FeedItem` (vedi `feeds/models.py`).
2. Aggiungi dati di esempio in `mock_data.py` per il fallback.
3. Registra la fonte in `feeds/aggregator.py`.
4. Aggiungi un colore/etichetta per la nuova fonte in
   `render/html_renderer.py` (`SOURCE_LABELS`, `SOURCE_ICONS`, CSS `.badge-*`).

## Note

- Nessun database: ogni esecuzione rigenera `output/feed.html` da zero.
- Nessun dato viene inviato altrove: tutto rimane sulla tua macchina.
- Le chiamate alle API reali falliscono in modo silenzioso verso i dati mock
  (con un messaggio in console), così la dashboard funziona sempre.
