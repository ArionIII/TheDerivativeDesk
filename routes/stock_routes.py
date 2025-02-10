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


matplotlib.use("Agg")

# Blueprints
stocks_routes = Blueprint("stocks_routes", __name__)
stock_chart_routes = Blueprint("stock_chart_routes", __name__)

# Fetch available tickers
ALL_TICKERS = combine_tickers_and_titles()

@stocks_routes.route("/api/stocks", methods=["GET"])
def get_random_stocks():
    """
    Fetch random stocks data from ALL_TICKERS.
    """
    search_term = request.args.get("search", "").lower()
    num_stocks = int(request.args.get("limit", 4))

    try:
        if search_term:
            possible_tickers = [
                ticker for ticker, title in ALL_TICKERS.items()
                if search_term in ticker.lower() or search_term in title.lower()
            ]
        else:
            possible_tickers = list(ALL_TICKERS.keys())

        if not possible_tickers:
            logger.warning("No stocks found matching the search criteria.")
            return jsonify({"error": "No stocks found"}), 404

        selected_tickers = random.sample(possible_tickers, min(len(possible_tickers), num_stocks * 3))
        valid_stocks = []

        for ticker in selected_tickers:
            stock = yf.Ticker(ticker)
            # time.sleep(1)  # Ajout d'un délai pour éviter un rate-limit
            info = stock.info

            # Vérification que l'info existe
            if not info or "quoteType" not in info or "regularMarketVolume" not in info:
                logger.warning(f"Skipping {ticker}: No valid market data found.")
                continue

            # Récupération des valeurs avec vérification
            current_price = info.get("currentPrice")
            previous_close = info.get("previousClose")
            history = stock.history(period="1mo", interval="1d")

            if history.empty or "Close" not in history:
                logger.warning(f"Skipping {ticker}: No historical data available.")
                continue

            first_price = history.iloc[0]["Close"] if not history.empty else None

            # Vérification avant de calculer les pourcentages
            change = (current_price - previous_close) / previous_close if current_price and previous_close else "N/A"
            change_monthly = (current_price - first_price) / first_price if current_price and first_price else "N/A"
            if not change or not change_monthly:
                logger.warning(f"Skipping {ticker}: Invalid price change data.")
                continue

            valid_stocks.append({
                "ticker": ticker,
                "title": ALL_TICKERS.get(ticker, "Unknown"),
                "price": current_price,
                "change": change if isinstance(change, float) else "N/A",
                "change_monthly": change_monthly if isinstance(change_monthly, float) else "N/A",
            })

            if len(valid_stocks) >= num_stocks:
                break

        if len(valid_stocks) < num_stocks:
            logger.warning(f"Only found {len(valid_stocks)} valid tickers out of {num_stocks} requested.")

        return jsonify({"stocks": valid_stocks[:num_stocks]}) 

    except Exception as e:
        logger.error(f"Error fetching stock data: {e}")
        return jsonify({"error": str(e)}), 500



# Cache pour éviter les doublons
generated_charts = set()

@stock_chart_routes.route("/api/stock-chart/<ticker>", methods=["GET"])
def get_stock_chart(ticker):
    try:
        global generated_charts

        # Empêcher les doublons
        if ticker in generated_charts:
            logger.warning(f"Skipping duplicate chart for {ticker}")
            return jsonify({"error": f"Chart for {ticker} already generated"}), 409

        stock = yf.Ticker(ticker)
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

        # Ajout au cache
        generated_charts.add(ticker)

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
        logger.error(f"Error fetching stock details for {ticker}: {e}")
        return jsonify({"error": str(e)}), 500

