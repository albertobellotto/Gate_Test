"""Realistic sample data used whenever real API credentials are not configured."""

from datetime import datetime, timedelta

from .models import FeedItem


def _ago(minutes: int) -> datetime:
    return datetime.now() - timedelta(minutes=minutes)


def get_mock_twitter():
    return [
        FeedItem(
            source="twitter",
            author="@nasa",
            timestamp=_ago(12),
            content="Splashdown confirmed! Welcome home to our Crew-9 astronauts after 171 days aboard the @Space_Station. 🚀",
            url="https://twitter.com/nasa/status/1000000000001",
            meta={"likes": 15234, "retweets": 3021},
        ),
        FeedItem(
            source="twitter",
            author="@github",
            timestamp=_ago(47),
            content="Copilot code review is now generally available for all plans. Ship with more confidence.",
            url="https://twitter.com/github/status/1000000000002",
            meta={"likes": 4210, "retweets": 612},
        ),
        FeedItem(
            source="twitter",
            author="@ilpost",
            timestamp=_ago(90),
            content="Le previsioni meteo per il weekend: in arrivo un peggioramento al Nord, tempo stabile al Sud.",
            url="https://twitter.com/ilpost/status/1000000000003",
            meta={"likes": 88, "retweets": 14},
        ),
        FeedItem(
            source="twitter",
            author="@ycombinator",
            timestamp=_ago(150),
            content="Applications for the Winter batch close Friday. Don't wait until the last minute.",
            url="https://twitter.com/ycombinator/status/1000000000004",
            meta={"likes": 980, "retweets": 121},
        ),
        FeedItem(
            source="twitter",
            author="@vercel",
            timestamp=_ago(260),
            content="Next.js 16 release candidate is out, with faster builds and a smaller runtime footprint.",
            url="https://twitter.com/vercel/status/1000000000005",
            meta={"likes": 2310, "retweets": 340},
        ),
    ]


def get_mock_telegram():
    return [
        FeedItem(
            source="telegram",
            author="Il Post - Canale Notizie",
            timestamp=_ago(8),
            content="Ultim'ora: approvato il decreto in Consiglio dei Ministri, entrerà in vigore da lunedì.",
            meta={"channel_members": 84213},
        ),
        FeedItem(
            source="telegram",
            author="Dev Notes IT",
            timestamp=_ago(35),
            content="Rilasciata la nuova versione di PostgreSQL 18: miglioramenti su indicizzazione e replica logica.",
            meta={"channel_members": 12040},
        ),
        FeedItem(
            source="telegram",
            author="Crypto Daily Brief",
            timestamp=_ago(70),
            content="BTC stabile sopra i 60k, volumi in calo dell'8% rispetto a ieri. Analisi completa nel link.",
            meta={"channel_members": 55870},
        ),
        FeedItem(
            source="telegram",
            author="Startup Italia",
            timestamp=_ago(180),
            content="Round da 4M€ per una scaleup milanese nel settore fintech B2B. I dettagli nel prossimo post.",
            meta={"channel_members": 9310},
        ),
        FeedItem(
            source="telegram",
            author="Weather Alert",
            timestamp=_ago(300),
            content="Allerta gialla per temporali forti nelle prossime 12 ore in Lombardia ed Emilia-Romagna.",
            meta={"channel_members": 21044},
        ),
    ]


def get_mock_email():
    return [
        FeedItem(
            source="email",
            author="GitHub <notifications@github.com>",
            timestamp=_ago(5),
            title="[gate_test] New review requested on your pull request",
            content="A reviewer was requested for your pull request unified-information-feeds. Review it when you have a moment.",
            meta={},
        ),
        FeedItem(
            source="email",
            author="Google Calendar <calendar-notification@google.com>",
            timestamp=_ago(60),
            title="Promemoria: Sync settimanale alle 15:00",
            content="Il tuo evento inizia tra un'ora. Partecipa con Google Meet.",
            meta={},
        ),
        FeedItem(
            source="email",
            author="Banca Widget <no-reply@bancawidget.it>",
            timestamp=_ago(130),
            title="Estratto conto disponibile",
            content="Il tuo estratto conto mensile è pronto per la consultazione nell'area riservata.",
            meta={},
        ),
        FeedItem(
            source="email",
            author="Newsletter - Il Punto",
            timestamp=_ago(220),
            title="Le 5 notizie tech della settimana",
            content="Questa settimana: nuovi modelli AI, un round importante nel settore climate-tech, e altro.",
            meta={},
        ),
        FeedItem(
            source="email",
            author="Amazon <shipment-tracking@amazon.it>",
            timestamp=_ago(400),
            title="Il tuo pacco è in consegna oggi",
            content="Il corriere consegnerà il tuo ordine entro le 21:00 di oggi.",
            meta={},
        ),
    ]
