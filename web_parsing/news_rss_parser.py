from flask import Flask, jsonify
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
    "Reuters": "https://www.reutersagency.com/feed/?taxonomy=best-sectors&post_type=best"
}

def get_news_from_rss():
    """ Récupère les dernières news depuis les flux RSS. """
    global last_fetched_minute, cached_news
    current_minute = time.localtime().tm_min  # Récupère la minute actuelle

    if last_fetched_minute == current_minute:
        print("⏳ Same minute detected, returning cached news.")
        return cached_news  # Retourne le cache si la minute n'a pas changé

    print(f"🆕 Fetching fresh news at minute {current_minute}...")
    all_news = []

    for source, url in rss_feeds.items():
        print(f"🔍 Fetching news from {source}...")
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:  # Récupère les 10 dernières news par source
            news_item = {
                "source": source,
                "title": entry.title,
                "link": entry.link,
                "published": entry.published if "published" in entry else "Unknown"
            }
            all_news.append(news_item)

    last_fetched_minute = current_minute
    cached_news = all_news  # Met à jour le cache complet

    return filter_new_news(all_news)  # Filtre et retourne seulement les nouvelles news

def filter_new_news(all_news):
    """ Compare les nouvelles news avec le cache et retourne uniquement les inédites. """
    global cached_news_set
    new_news = []

    for news_item in all_news:
        news_identifier = news_item["title"] + news_item["link"]  # Clé unique basée sur titre + lien
        if news_identifier not in cached_news_set:
            cached_news_set.add(news_identifier)  # Ajoute la news au cache
            new_news.append(news_item)  # Ajoute aux nouvelles news à envoyer
    return new_news  # Retourne uniquement les nouvelles news