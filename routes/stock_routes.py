import yfinance as yf
import random
from flask import Blueprint, jsonify, request, send_file
from config import logger
import matplotlib.pyplot as plt
from io import BytesIO
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import matplotlib
import time
from web_parsing.fetch_tickers_and_titles import fetch_index_tickers, combine_tickers_and_titles
import feedparser
import ipdb

matplotlib.use("Agg")
GOOGLE_NEWS_RSS_URL = "https://news.google.com/rss/search?q={ticker}+stock&hl=en-US&gl=US&ceid=US:en"

# Blueprints
stocks_routes = Blueprint("stocks_routes", __name__)
stock_chart_routes = Blueprint("stock_chart_routes", __name__)
stock_news_routes = Blueprint("stock_news_routes", __name__)

# Fetch available tickers
ALL_TICKERS = combine_tickers_and_titles()
@stocks_routes.route("/api/stocks", methods=["GET"])
def get_random_stocks():
    #TODO : Séparer en 2 fonctions...
    """
    Fetch stock data from ALL_TICKERS.
    - Si c'est une recherche rapide (search_term != "" et detailed=False), on renvoie juste les tickers et titres.
    - Si `detailed=True`, on récupère uniquement le stock demandé avec toutes ses données.
    - Sinon, on retourne une sélection aléatoire de stocks avec leurs données complètes.
    """
    search_term = request.args.get("search", "").lower()
    num_stocks = int(request.args.get("limit", 4))
    detailed = request.args.get("detailed", "false").lower() == "true"

    try:
        if search_term and not detailed:
            logger.info(f"Searching for stocks matching: {search_term} (Quick Search Mode)")
            # **⚡ Mode recherche rapide : ne renvoyer que tickers et titres**
            possible_tickers = [
                {"ticker": ticker, "title": title}
                for ticker, title in ALL_TICKERS.items()
                if search_term in ticker.lower() or search_term in title.lower()
            ]
            logger.info(f"Found {len(possible_tickers)} matching stocks")
            return jsonify({"stocks": possible_tickers[:num_stocks]})

        if detailed:
            search_term = request.args.get("search", "").upper()
            if not search_term or search_term not in ALL_TICKERS:
                logger.warning(f"Invalid detailed search: No valid ticker found for '{search_term}'")
                return jsonify({"error": "Invalid ticker for detailed search"}), 400

            logger.info(f"Fetching detailed data for stock: {search_term}")

            stock = yf.Ticker(search_term)
            info = stock.info

            if not info or "quoteType" not in info or "regularMarketVolume" not in info:
                logger.warning(f"Skipping {search_term}: No valid market data found.")
                return jsonify({"error": "No valid market data available"}), 404

            current_price = info.get("currentPrice")
            previous_close = info.get("previousClose")
            history = stock.history(period="1mo", interval="1d")

            if history.empty or "Close" not in history:
                logger.warning(f"Skipping {search_term}: No historical data available.")
                return jsonify({"error": "No historical data available"}), 404

            first_price = history.iloc[0]["Close"] if not history.empty else None

            change = (current_price - previous_close) / previous_close if current_price and previous_close else "N/A"
            change_monthly = (current_price - first_price) / first_price if current_price and first_price else "N/A"

            stock_data = {
                "ticker": search_term,
                "title": ALL_TICKERS.get(search_term, "Unknown"),
                "price": current_price,
                "change": change if isinstance(change, float) else "N/A",
                "change_monthly": change_monthly if isinstance(change_monthly, float) else "N/A",
            }

            return jsonify({"stocks": [stock_data]})

        # **🔹 Mode normal : sélection aléatoire avec toutes les vérifications**
        logger.info(f"Fetching random stocks data ({num_stocks} stocks)")
        possible_tickers = list(ALL_TICKERS.keys())
        selected_tickers = random.sample(possible_tickers, min(len(possible_tickers), num_stocks * 3))
        valid_stocks = []
        logger.warning(selected_tickers)
        for ticker in selected_tickers:
            stock = yf.Ticker(ticker)
            logger.warning(stock)
            try:
                info = stock.info
            except Exception:
                #TODO : Un peu sale comme solution mais bug majeur qui a pop avec la 
                # MAJ 0.14 de yfinance --> a voir si je peux régler ça 
                # (impossible de rétrograder car les autres sont déprécated : peut etre 0.13 a tester)
                
                # AUSSI : Dans le search bah s'il clique dessus et que y'a pas d'info, ca fait 
                # juste rien --> afficher message d'indisponibilité ?
                logger.error('skipping an error stock')
                continue
            logger.info("info for the stock")
            # ipdb.set_trace()
            if not info or "quoteType" not in info or "regularMarketVolume" not in info:
                logger.warning(f"Skipping {ticker}: No valid market data found.")
                continue

            current_price = info.get("currentPrice")
            previous_close = info.get("previousClose")
            history = stock.history(period="1mo", interval="1d")
            # ipdb.set_trace()
            if history.empty or "Close" not in history or history["Close"].isna().all():
                logger.warning(f"Skipping {ticker}: No historical data available.")
                continue

            first_price = history.iloc[0]["Close"] if not history.empty else None
            # ipdb.set_trace()
            change = (current_price - previous_close) / previous_close if current_price and previous_close else "N/A"
            change_monthly = (current_price - first_price) / first_price if current_price and first_price else "N/A"
            # ipdb.set_trace()
            valid_stocks.append({
                "ticker": ticker,
                "title": ALL_TICKERS.get(ticker, "Unknown"),
                "price": current_price,
                "change": change if isinstance(change, float) else "N/A",
                "change_monthly": change_monthly if isinstance(change_monthly, float) else "N/A",
            })
            # ipdb.set_trace()

            if len(valid_stocks) >= num_stocks:
                break

        return jsonify({"stocks": valid_stocks[:num_stocks]}) 

    except Exception as e:
        logger.info('Get random stocks')
        logger.error(f"Error fetching stock data: {e}")
        return jsonify({"error": str(e)}), 500





@stock_chart_routes.route("/api/stock-chart/<ticker>", methods=["GET"])
def get_stock_chart(ticker):
    try:
        logger.warning('Entering random stock get')
        stock = yf.Ticker(ticker)
        logger.warning(stock)
        # time.sleep(1)  # Ajout d'un délai pour éviter un rate-limit
        history = stock.history(period="1mo", interval="1d")

        if history.empty:
            logger.warning(f"No data available for {ticker}")
            return jsonify({"error": f"No data available for {ticker}"}), 404

        # Vérification de la colonne "Close"
        if "Close" not in history or history["Close"].isna().all():
            logger.warning(f"No 'Close' price available for {ticker}")
            return jsonify({"error": f"No 'Close' price available for {ticker}"}), 404

        # Vérification des valeurs min/max
        min_price = history["Close"].min()
        max_price = history["Close"].max()
        if min_price is None or max_price is None or min_price == max_price:
            logger.warning(f"Invalid price range for {ticker}")
            return jsonify({"error": f"Invalid price range for {ticker}"}), 404

        # Empêcher les graphes avec une échelle 0-1
        if max_price - min_price < 0.01:
            logger.warning(f"Skipping {ticker} chart: Insufficient price variation (min={min_price}, max={max_price})")
            return jsonify({"error": f"Price variation too small for {ticker}"}), 404

        # Création propre du graphique
        plt.close('all')  # Nettoyage avant de créer un nouveau graphe
        fig, ax = plt.subplots(figsize=(4.5, 2.3))  # Création propre de la figure
        
        ax.plot(history.index, history["Close"], label=f"{ticker} Price", color="#007bff", linewidth=2)
        ax.set_title(f"{ticker} - Last 1 Month")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (USD)")
        ax.set_ylim(min_price * 0.95, max_price * 1.05)
        ax.grid(alpha=0.3)
        ax.xaxis.set_major_formatter(DateFormatter('%d'))

        # Sauvegarde et envoi de l'image
        buffer = BytesIO()
        fig.savefig(buffer, format="png")
        # fig.savefig(f"static/debug/{ticker}_debug_chart.png")
        buffer.seek(0)

        # time.sleep(1)  # Ajout d'un délai pour éviter des conflits
        plt.close(fig)  # Fermeture propre du graphe

        return send_file(buffer, mimetype="image/png")

    except Exception as e:
        logger.error(f"Error generating chart for {ticker}: {e}")
        return jsonify({"error": str(e)}), 500


@stocks_routes.route("/api/stock-details/<ticker>", methods=["GET"])
def get_stock_details(ticker):
    """
    Fetch detailed information and historical data for a specific stock.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        history = stock.history(period="6mo", interval="1d")  # 6 months daily data

        if history.empty:
            return jsonify({"error": "No historical data available"}), 404
        
        stock_details = {
            # Informations de base
            "ticker": ticker,
            "name": info.get("shortName", ticker),
            "long_name": info.get("longName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "country": info.get("country", "N/A"),
            "website": info.get("website", "N/A"),
            "description": info.get("longBusinessSummary", "N/A"),

            # Capitalisation boursière et valeurs de marché
            "market_cap": info.get("marketCap", "N/A"),
            "enterprise_value": info.get("enterpriseValue", "N/A"),
            "currency": info.get("currency", "N/A"),
            "exchange": info.get("exchange", "N/A"),
            "quote_type": info.get("quoteType", "N/A"),

            # Prix actuels et historiques
            "current_price": info.get("currentPrice", "N/A"),
            "previous_close": info.get("previousClose", "N/A"),
            "open_price": info.get("open", "N/A"),
            "day_high": info.get("dayHigh", "N/A"),
            "day_low": info.get("dayLow", "N/A"),
            "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
            "50_day_average": info.get("fiftyDayAverage", "N/A"),
            "200_day_average": info.get("twoHundredDayAverage", "N/A"),

            # Volume et liquidité
            "volume": info.get("volume", "N/A"),
            "average_volume": info.get("averageVolume", "N/A"),
            "average_volume_10d": info.get("averageVolume10days", "N/A"),
            "bid": info.get("bid", "N/A"),
            "ask": info.get("ask", "N/A"),
            "bid_size": info.get("bidSize", "N/A"),
            "ask_size": info.get("askSize", "N/A"),

            # Ratios financiers
            "pe_ratio": info.get("trailingPE", "N/A"),
            "forward_pe": info.get("forwardPE", "N/A"),
            "peg_ratio": info.get("trailingPegRatio", "N/A"),
            "price_to_sales": info.get("priceToSalesTrailing12Months", "N/A"),
            "price_to_book": info.get("priceToBook", "N/A"),
            "book_value": info.get("bookValue", "N/A"),

            # Rentabilité et marges
            "return_on_assets": info.get("returnOnAssets", "N/A"),
            "return_on_equity": info.get("returnOnEquity", "N/A"),
            "profit_margins": info.get("profitMargins", "N/A"),
            "operating_margins": info.get("operatingMargins", "N/A"),
            "gross_margins": info.get("grossMargins", "N/A"),
            "ebitda_margins": info.get("ebitdaMargins", "N/A"),

            # Dividendes
            "dividend_rate": info.get("dividendRate", "N/A"),
            "dividend_yield": info.get("dividendYield", "N/A"),
            "payout_ratio": info.get("payoutRatio", "N/A"),
            "ex_dividend_date": info.get("exDividendDate", "N/A"),
            "five_year_avg_div_yield": info.get("fiveYearAvgDividendYield", "N/A"),

            # Dettes et cashflow
            "total_debt": info.get("totalDebt", "N/A"),
            "total_cash": info.get("totalCash", "N/A"),
            "cash_per_share": info.get("totalCashPerShare", "N/A"),
            "debt_to_equity": info.get("debtToEquity", "N/A"),
            "operating_cashflow": info.get("operatingCashflow", "N/A"),
            "free_cashflow": info.get("freeCashflow", "N/A"),
            "ebitda": info.get("ebitda", "N/A"),

            # Analystes et prévisions
            "recommendation": info.get("recommendationKey", "N/A"),
            "recommendation_mean": info.get("recommendationMean", "N/A"),
            "number_of_analyst_opinions": info.get("numberOfAnalystOpinions", "N/A"),
            "target_high_price": info.get("targetHighPrice", "N/A"),
            "target_low_price": info.get("targetLowPrice", "N/A"),
            "target_mean_price": info.get("targetMeanPrice", "N/A"),
            "target_median_price": info.get("targetMedianPrice", "N/A"),

            # Données historiques sur 1 an
            "chart_data": {
                "dates": history.index.strftime("%Y-%m-%d").tolist(),
                "prices": history["Close"].tolist(),
                "volumes": history["Volume"].tolist(),
                "dividends": history["Dividends"].tolist() if "Dividends" in history else ["N/A"] * len(history),
                "splits": history["Stock Splits"].tolist() if "Stock Splits" in history else ["N/A"] * len(history),
            },

            # Autres métriques
            "beta": info.get("beta", "N/A"),
            "sandp_52_week_change": info.get("SandP52WeekChange", "N/A"),
            "enterprise_to_revenue": info.get("enterpriseToRevenue", "N/A"),
            "enterprise_to_ebitda": info.get("enterpriseToEbitda", "N/A"),
        }
        # logger.warning(f"stock_details : {stock_details}")
        return jsonify({"details": stock_details})
    except Exception as e:
        logger.info('Get Stock Details')
        logger.error(f"Error fetching stock details for {ticker}: {e}")
        return jsonify({"error": str(e)}), 500



@stock_news_routes.route("/api/stock-news/<ticker>", methods=["GET"])
def get_stock_news(ticker):
    """
    Fetch news articles related to a given stock ticker from Google News RSS.
    """
    try:
        formatted_ticker = ticker.upper()
        rss_url = GOOGLE_NEWS_RSS_URL.format(ticker=formatted_ticker)
        
        logger.info(f"Fetching news for {formatted_ticker} from {rss_url}")

        feed = feedparser.parse(rss_url)

        if not feed.entries:
            logger.warning(f"No news found for {formatted_ticker}")
            return jsonify({"error": "No news found"}), 404

        news_articles = []
        for entry in feed.entries[:10]:  # Limit to 10 articles
            news_articles.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.published,
                "summary": entry.summary,
                "source": entry.get("source", {}).get("title", "Unknown Source"),
            })

        return jsonify({"news": news_articles})

    except Exception as e:
        logger.info('Get Stock News')
        logger.error(f"Error fetching news for {ticker}: {e}")
        return jsonify({"error": str(e)}), 500
