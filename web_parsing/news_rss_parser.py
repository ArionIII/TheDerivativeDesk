from flask import Flask
import feedparser
import time
from config import logger

app = Flask(__name__)

# Stocke la dernière minute où les news ont été fetch
last_fetched_minute = None
cached_news = []  # Stocke toutes les news fetchées
cached_news_set = set()  # Stocke uniquement les titres des news déjà envoyées

# Dictionnaire des flux RSS
rss_feeds = {
    "CNBC": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "Seeking Alpha": "https://seekingalpha.com/feed.xml",
    "Investing.com": "https://www.investing.com/rss/news.rss",
    "WSJ": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
    "Yahoo Finance": "https://finance.yahoo.com/news/rssindex",
    "Financial Times": "https://www.ft.com/rss/home",
    "Fortune": "https://fortune.com/feed/",
    "MarketWatch": "https://www.marketwatch.com/rss/topstories",
    "Reddit": "https://www.reddit.com/r/finance/.rss",
    "CNN Money": "https://money.cnn.com/services/rss/",
    "Reuters": "https://www.reutersagency.com/feed/?taxonomy=best-sectors&post_type=best",
}

last_fetched_minute = None
cached_news = []


def get_news_from_rss():
    logger.info("Fetching news...")
    global last_fetched_minute, cached_news
    current_minute = time.localtime().tm_min

    if last_fetched_minute == current_minute:
        return cached_news

    all_news = []
    for source, url in rss_feeds.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]:
            news_item = {
                "source": source,
                "title": entry.title,
                "link": entry.link,
                "published": entry.published if "published" in entry else "Unknown",
            }
            all_news.append(news_item)
    last_fetched_minute = current_minute
    cached_news = all_news
    return all_news
