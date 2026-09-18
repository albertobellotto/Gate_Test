# Feed Unificato

Un'unica dashboard locale che aggrega i tuoi flussi informativi — Twitter/X,
un canale Telegram ed email — in tre colonne separate su un'unica pagina
HTML, responsive e con ricerca.

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

- **Twitter/X**: modo consigliato, una **X List** (lista curata di account).
  Richiede `TWITTER_BEARER_TOKEN` + `TWITTER_LIST_ID` (l'ID è il numero
  nell'URL della lista, es. `https://x.com/i/lists/1234567890123456789`).
  ⚠️ L'endpoint delle liste richiede un piano API a pagamento (Basic o
  superiore) — non è disponibile nel piano gratuito di sviluppo. In
  alternativa puoi usare `TWITTER_USERNAMES` (account singoli separati da
  virgola), usato solo se `TWITTER_LIST_ID` è vuoto.
- **Telegram**: un solo canale **pubblico**, impostando `TELEGRAM_CHANNEL`
  (username senza @, es. `durov`). Non serve creare un bot: i messaggi
  vengono letti dall'anteprima pubblica del canale (`t.me/s/<canale>`).
  Funziona solo con canali pubblici.
- **Email**: richiede host IMAP, utente e password (per Gmail, usa una
  "App Password" con la verifica in due passaggi attiva). Funziona con
  qualsiasi account — anche diverso da quello eventualmente collegato a
  Claude — perché le credenziali restano solo nel tuo `.env` locale e non
  transitano da nessuna parte legata a questa sessione.

Rilancia `python main.py` ogni volta che vuoi un aggiornamento del feed.

## Struttura del progetto

```
feeds/
  models.py          # modello dati unificato (FeedItem)
  mock_data.py        # dati di esempio per ogni fonte
  twitter_feed.py      # fetch da X List (o account singoli) + fallback mock
  telegram_feed.py     # fetch da un canale pubblico + fallback mock
  email_feed.py         # fetch reale (IMAP) + fallback mock
  aggregator.py         # unisce e ordina tutte le fonti
render/
  html_renderer.py     # genera la dashboard HTML (colonne, ricerca)
main.py                # entry point
```

## Estendere con nuove fonti

Per aggiungere una nuova fonte (es. RSS, Slack, Mastodon):

1. Crea `feeds/<nome>_feed.py` con una funzione `fetch()` che ritorna una
   lista di `FeedItem` (vedi `feeds/models.py`).
2. Aggiungi dati di esempio in `mock_data.py` per il fallback.
3. Registra la fonte in `feeds/aggregator.py`.
4. Aggiungi un colore/etichetta per la nuova fonte in
   `render/html_renderer.py` (`SOURCE_LABELS`, `SOURCE_ICONS` e le regole CSS
   per il bordo colonna).

## Note

- Nessun database: ogni esecuzione rigenera `output/feed.html` da zero.
- Nessun dato viene inviato altrove: tutto rimane sulla tua macchina.
- Le chiamate alle API reali falliscono in modo silenzioso verso i dati mock
  (con un messaggio in console), così la dashboard funziona sempre.
