import requests
import pandas as pd
from config import logger

def fetch_index_tickers(index_name):
    """
    Fetch the tickers and titles for a given index.
    """
    if index_name == "S&P 500":
        url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        table_idx = 0
        symbol_col, name_col = "Symbol", "Security"
    elif index_name == "CAC 40":
        url = "https://en.wikipedia.org/wiki/CAC_40"
        table_idx = 3
        symbol_col, name_col = "Ticker", "Company"
    elif index_name == "DOW JONES":
        url = "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average"
        table_idx = 1
        symbol_col, name_col = "Symbol", "Company"
    elif index_name == "NIKKEI":
        url = "https://en.wikipedia.org/wiki/Nikkei_225"
        table_idx = 2
        symbol_col, name_col = "Ticker", "Company"
    else:
        raise ValueError(f"Unsupported index: {index_name}")

    try:
        response = requests.get(url)
        logger.warning(f"Fetching data for {index_name} from {url}")
        logger.error(f"Response status code: {response.status_code}")
        if response.status_code == 200:
            tables = pd.read_html(response.text)
            index_table = tables[table_idx]
            tickers = index_table[[symbol_col, name_col]].dropna()
            return {
                row[symbol_col]: row[name_col]
                for _, row in tickers.iterrows()
            }
        else:
            raise Exception(f"Failed to fetch data for {index_name}")
    except Exception as e:
        print(f"Error fetching tickers for {index_name}: {e}")
        return {}

# Combine tickers into a single dictionary
def combine_tickers_and_titles():
    all_indices = {
    "S&P 500": fetch_index_tickers("S&P 500"),
    "CAC 40": fetch_index_tickers("CAC 40"),
    "DOW JONES": fetch_index_tickers("DOW JONES"),
    "NIKKEI": fetch_index_tickers("NIKKEI"),
}
    """
    Combine all index tickers and titles into a single dictionary.
    """
    global_tickers = {}
    for index, tickers in all_indices.items():
        for ticker, title in tickers.items():
            global_tickers[ticker] = title
    return global_tickers

