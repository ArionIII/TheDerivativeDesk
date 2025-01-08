import yfinance as yf
import random
from flask import Blueprint, jsonify, request, send_file
from config import logger
import matplotlib.pyplot as plt
from io import BytesIO
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import matplotlib
from fetch_tickers_and_titles import fetch_index_tickers, combine_tickers_and_titles

matplotlib.use("Agg")
# Blueprint for stock data
stocks_routes = Blueprint("stocks_routes", __name__)
stock_chart_routes = Blueprint("stock_chart_routes", __name__)


# Example list of S&P 500 tickers (can be replaced with a dynamic fetch)
SP500_TICKERS = [
    "AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "META", "NVDA", "JNJ", "XOM", "PG",  # Add more tickers
]

#TODO : Pas utile de fetch a chaque fois, autant s'output un csv 1 fois par semaine ou autre.
ALL_TICKERS = combine_tickers_and_titles()

@stocks_routes.route("/api/stocks", methods=["GET"])
def get_random_stocks():
    """
    Fetch random stocks data from ALL_TICKERS.
    """
    search_term = request.args.get("search", "").lower()
    num_stocks = int(request.args.get("limit", 4))

    try:
        # Filter based on search term or get random stocks
        if search_term:
            selected_tickers = [
                ticker for ticker, title in ALL_TICKERS.items()
                if search_term in ticker.lower() or search_term in title.lower()
            ]
        else:
            selected_tickers = random.sample(list(ALL_TICKERS.keys()), num_stocks)

        # Ensure we don't exceed the requested number of stocks
        selected_tickers = selected_tickers[:num_stocks]

        logger.info(f"Selected tickers: {selected_tickers}")

        # Fetch stock data
        stocks_data = []
        for ticker in selected_tickers:
            stock = yf.Ticker(ticker)
            info = stock.info
            current_price = info.get("currentPrice", None)
            previous_close = info.get("previousClose", None)
            
            if current_price is not None and previous_close is not None:
                change = (current_price - previous_close) / previous_close
            else:
                change = None

            stocks_data.append({
                "ticker": ticker,
                "title": ALL_TICKERS[ticker],
                "price": current_price if current_price is not None else "N/A",
                "change": change if change is not None else "N/A",
            })

        return jsonify({"stocks": stocks_data})
    except Exception as e:
        logger.error(f"Error fetching stock data: {e}")
        return jsonify({"error": str(e)}), 500


@stock_chart_routes.route("/api/stock-chart/<ticker>", methods=["GET"])
def get_stock_chart(ticker):
    try:
        # Fetch historical data
        stock = yf.Ticker(ticker)
        history = stock.history(period="1mo", interval="1d")

        if history.empty:
            logger.warning(f"No data available for ticker {ticker}")
            return jsonify({"error": f"No data available for {ticker}"}), 404

        # Plotting
        plt.figure(figsize=(4.5, 2.3))
        plt.plot(history.index, history["Close"], label=f"{ticker} Price", color="#007bff", linewidth=2)
        plt.title(f"{ticker} - Last 1 Month")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.grid(alpha=0.3)
        # plt.legend()
        ax = plt.gca()
        ax.xaxis.set_major_formatter(DateFormatter('%d'))
        # plt.xticks(rotation=45, fontsize=8)
        # plt.yticks(fontsize=8)


        # Save plot to buffer
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        plt.close()

        return send_file(buffer, mimetype="image/png")
    except Exception as e:
        logger.error(f"Error generating chart for {ticker}: {e}")
        return jsonify({"error": str(e)}), 500


@stocks_routes.route("/api/stock-details/<ticker>", methods=["GET"])
def get_stock_details(ticker):
    """
    Fetch detailed information about a specific stock.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Select key details to return
        stock_details = {
            "ticker": ticker,
            "name": info.get("shortName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "current_price": info.get("currentPrice", "N/A"),
            "day_high": info.get("dayHigh", "N/A"),
            "day_low": info.get("dayLow", "N/A"),
            "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
            "volume": info.get("volume", "N/A"),
            "average_volume": info.get("averageVolume", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "dividend_yield": info.get("dividendYield", "N/A"),
            "description": info.get("longBusinessSummary", "N/A"),
        }

        return jsonify({"details": stock_details})
    except Exception as e:
        logger.error(f"Error fetching stock details for {ticker}: {e}")
        return jsonify({"error": str(e)}), 500
