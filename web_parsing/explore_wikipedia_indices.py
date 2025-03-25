import pandas as pd
import requests

# Dictionnaire contenant les indices et leurs URLs
indices = {
    "S&P 500": {
        "url": "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
    },
    "CAC 40": {
        "url": "https://fr.wikipedia.org/wiki/CAC_40",
    },
    "DOW JONES": {
        "url": "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average",
    },
    "NIKKEI": {
        "url": "https://en.wikipedia.org/wiki/Nikkei_225",
    },
    "FTSE 100": {
        "url": "https://en.wikipedia.org/wiki/FTSE_100_Index",
    },
    "DAX": {
        "url": "https://en.wikipedia.org/wiki/DAX",
    },
    "Hang Seng": {
        "url": "https://en.wikipedia.org/wiki/Hang_Seng_Index",
    },
    "Nasdaq-100": {
        "url": "https://en.wikipedia.org/wiki/NASDAQ-100",
    },
    "Russell 2000": {
        "url": "https://en.wikipedia.org/wiki/Russell_2000_Index",
    },
    "Shanghai Composite": {
        "url": "https://en.wikipedia.org/wiki/Shanghai_Composite",
    },
    "Euro Stoxx 50": {
        "url": "https://en.wikipedia.org/wiki/EURO_STOXX_50",
    },
    "BSE Sensex": {
        "url": "https://en.wikipedia.org/wiki/BSE_SENSEX",
    },
    "ASX 200": {
        "url": "https://en.wikipedia.org/wiki/S%26P/ASX_200",
    },
    "KOSPI": {
        "url": "https://en.wikipedia.org/wiki/KOSPI",
    },
    "IBEX 35": {
        "url": "https://en.wikipedia.org/wiki/IBEX_35",
    },
    "TSX Composite": {
        "url": "https://en.wikipedia.org/wiki/S%26P/TSX_Composite_Index",
    },
    "Swiss Market Index": {
        "url": "https://en.wikipedia.org/wiki/Swiss_Market_Index",
    },
    "AEX": {
        "url": "https://en.wikipedia.org/wiki/AEX_index",
    },
    "MIB": {
        "url": "https://en.wikipedia.org/wiki/FTSE_MIB",
    },
    "PSI-20": {
        "url": "https://en.wikipedia.org/wiki/PSI-20",
    },
    "BEL 20": {
        "url": "https://en.wikipedia.org/wiki/BEL20",
    },
    "OMX Stockholm 30": {
        "url": "https://en.wikipedia.org/wiki/OMX_Stockholm_30",
    },
    "NZX 50": {
        "url": "https://en.wikipedia.org/wiki/NZX_50_Index",
    },
    "Bovespa": {
        "url": "https://en.wikipedia.org/wiki/Índice_Bovespa",
    },
    "JSE": {
        "url": "https://en.wikipedia.org/wiki/JSE_Limited",
    },
}


# Fonction pour afficher les tableaux et leurs indices
def inspect_tables(indices):
    for index_name, data in indices.items():
        url = data["url"]
        print(f"\nInspecting index: {index_name}")
        print(f"URL: {url}")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                tables = pd.read_html(response.text)
                for idx, table in enumerate(tables):
                    print(f"Table Index: {idx}")
                    print(
                        table.head()
                    )  # Affiche les premières lignes de chaque tableau
                    print("\n")
            else:
                print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
        except Exception as e:
            print(f"Error fetching data for {index_name}: {e}")


# Exécution du script
if __name__ == "__main__":
    inspect_tables(indices)
