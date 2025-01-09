import requests
import pandas as pd
from config import logger

import os
import datetime

# Global variable to store the last fetch day
last_fetch_date = None

indices = {
    "S&P 500": {
        "url": "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
        "table_idx": 0,
        "symbol_col": "Symbol",
        "name_col": "Security"
    },
    "CAC 40": {
        "url": "https://fr.wikipedia.org/wiki/CAC_40",
        "table_idx": 2,
        "symbol_col": "Mnémo",
        "name_col": "Société"
    },
    "DOW JONES": {
        "url": "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average",
        "table_idx": 2,
        "symbol_col": "Symbol",
        "name_col": "Company"
    },
    "FTSE 100": {
        "url": "https://en.wikipedia.org/wiki/FTSE_100_Index",
        "table_idx": 4,
        "symbol_col": "Ticker",
        "name_col": "Company"
    },
    "DAX": {
        "url": "https://en.wikipedia.org/wiki/DAX",
        "table_idx": 4,
        "symbol_col": "Ticker",
        "name_col": "Company"
    },
    "Hang Seng": {
        "url": "https://en.wikipedia.org/wiki/Hang_Seng_Index",
        "table_idx": 6,
        "symbol_col": "Ticker",
        "name_col": "Name"
    },
    "Nasdaq-100": {
        "url": "https://en.wikipedia.org/wiki/NASDAQ-100",
        "table_idx": 4,
        "symbol_col": "Symbol",
        "name_col": "Company"
    },
    "BSE Sensex": {
        "url": "https://en.wikipedia.org/wiki/BSE_SENSEX",
        "table_idx": 2,
        "symbol_col": "Symbol",
        "name_col": "Company"
    },
    "ASX 200": {
        "url": "https://en.wikipedia.org/wiki/S%26P/ASX_200",
        "table_idx": 2,
        "symbol_col": "Code",
        "name_col": "Company"
    },
    "IBEX 35": {
        "url": "https://en.wikipedia.org/wiki/IBEX_35",
        "table_idx": 2,
        "symbol_col": "Ticker",
        "name_col": "Company"
    },
    "TSX Composite": {
        "url": "https://en.wikipedia.org/wiki/S%26P/TSX_Composite_Index",
        "table_idx": 3,
        "symbol_col": "Ticker",
        "name_col": "Company"
    },
    "Swiss Market Index": {
        "url": "https://en.wikipedia.org/wiki/Swiss_Market_Index",
        "table_idx": 2,
        "symbol_col": "Ticker",
        "name_col": "Name"
    },
    "AEX": {
        "url": "https://en.wikipedia.org/wiki/AEX_index",
        "table_idx": 3,
        "symbol_col": "Ticker symbol",
        "name_col": "Company"
    },
    "MIB": {
        "url": "https://en.wikipedia.org/wiki/FTSE_MIB",
        "table_idx": 1,
        "symbol_col": "Ticker",
        "name_col": "Company"
    },
    "PSI-20": {
        "url": "https://en.wikipedia.org/wiki/PSI-20",
        "table_idx": 2,
        "symbol_col": "Ticker",
        "name_col": "Company"
    },

    "OMX Stockholm 30": {
        "url": "https://en.wikipedia.org/wiki/OMX_Stockholm_30",
        "table_idx": 1,
        "symbol_col": "Symbol",
        "name_col": "Company"
    },
    "NZX 50": {
        "url": "https://en.wikipedia.org/wiki/NZX_50_Index",
        "table_idx": 1,
        "symbol_col": "Ticker symbol",
        "name_col": "Company"
    },
}


def fetch_index_tickers(index_name):
    """
    Fetch the tickers and titles for a given index. Fetches from the web
    only if the day of the month is a multiple of 3 and it hasn't run today.
    Otherwise, it reads the data from a CSV file.
    """
    global last_fetch_date

    # Get today's date
    today = datetime.date.today()

    # Check if the day is a multiple of 3 and if the function hasn't run today
    if today.day % 3 == 0 and (last_fetch_date is None or last_fetch_date != today):
        # Fetch data from the web
        index_data = indices.get(index_name)
        if not index_data:
            raise ValueError(f"Unsupported index: {index_name}")

        try:
            response = requests.get(index_data["url"])
            logger.info(f"Fetching data for {index_name} from {index_data['url']}")
            if response.status_code == 200:
                tables = pd.read_html(response.text)
                index_table = tables[index_data["table_idx"]]
                tickers = index_table[[index_data["symbol_col"], index_data["name_col"]]].dropna()

                # Update the last fetch date
                last_fetch_date = today

                # Convert the fetched data to a dictionary
                return {
                    row[index_data["symbol_col"]]: row[index_data["name_col"]]
                    for _, row in tickers.iterrows()
                }
            else:
                raise Exception(f"Failed to fetch data for {index_name}: {response.status_code}")
        except Exception as e:
            logger.error(f"Error fetching tickers for {index_name}: {e}")
            return {}

    else:
        # Load data from the CSV file
        try:
            csv_path = "static/data/combined_tickers.csv"
            logger.info(f"Loading data from CSV: {csv_path}")
            tickers_df = pd.read_csv(csv_path)

            # Directly convert the DataFrame to a dictionary
            tickers_dict = tickers_df.set_index("Ticker")["Title"].to_dict()
            logger.info("Tickers loaded from CSV successfully.")
            return tickers_dict
        except Exception as e:
            logger.error(f"Error loading tickers from CSV: {e}")
            return {}


# Combine tickers from all indices into a single dictionary
def combine_tickers_and_titles():
    """
    Combine all index tickers and titles into a single dictionary.
    """
    global_tickers = {}
    for index_name in indices.keys():
        tickers = fetch_index_tickers(index_name)
        for ticker, title in tickers.items():
            global_tickers[ticker] = title
    output_path = "static/data/combined_tickers.csv"
    pd.DataFrame(list(global_tickers.items()), columns=["Ticker", "Title"]).to_csv(output_path, index=False)
    return global_tickers