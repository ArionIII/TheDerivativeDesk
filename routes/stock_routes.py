import yfinance as yf
import random
from flask import Blueprint, jsonify, request, send_file
from config import logger
import matplotlib.pyplot as plt
from io import BytesIO
import matplotlib.dates as mdates
import matplotlib
matplotlib.use("Agg")
# Blueprint for stock data
stocks_routes = Blueprint("stocks_routes", __name__)
stock_chart_routes = Blueprint("stock_chart_routes", __name__)


# Example list of S&P 500 tickers (can be replaced with a dynamic fetch)
SP500_TICKERS = [
    "AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "META", "NVDA", "JNJ", "XOM", "PG",  # Add more tickers
]

@stocks_routes.route("/api/stocks", methods=["GET"])
def get_random_stocks():
    """
    Fetch random stocks data from the S&P 500.
    """
    search_term = request.args.get("search", "").lower()
    num_stocks = int(request.args.get("limit", 4))

    try:
        # Filter or get random stocks
        selected_tickers = (
            [ticker for ticker in SP500_TICKERS if search_term in ticker.lower()]
            if search_term
            else random.sample(SP500_TICKERS, num_stocks)
        )
        logger.info(f"Selected tickers: {selected_tickers}")
        # Fetch stock data
        stocks_data = []
        for ticker in selected_tickers:
            stock = yf.Ticker(ticker)
            info = stock.info
            logger.warning(f"Stock info: ({info.get('currentPrice')}, {info.get('previousClose')})")
            stocks_data.append({
                "ticker": ticker,
                "title": info.get("shortName", ticker),
                "price": info.get("currentPrice", "N/A"),
                "change": ((info.get("currentPrice") - info.get("previousClose")) / info.get("previousClose"))
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
        plt.figure(figsize=(6, 4))
        plt.plot(history.index, history["Close"], label=f"{ticker} Price", color="#007bff", linewidth=2)
        plt.title(f"{ticker} - Last 1 Month")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.grid(alpha=0.3)
        plt.legend()

        # Save plot to buffer
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        plt.close()

        return send_file(buffer, mimetype="image/png")
    except Exception as e:
        logger.error(f"Error generating chart for {ticker}: {e}")
        return jsonify({"error": str(e)}), 500
