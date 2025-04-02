import requests
import os
from django.core.cache import cache  # Optional: Cache API responses

TOKEN = os.environ.get("TIINGO_TOKEN")
if not TOKEN:
    raise ValueError("Tiingo API token not configured in environment variables.")

headers = {
    'Content-Type': 'application/json',
}

def get_meta_data(ticker):
    """Fetch metadata for a ticker from Tiingo."""
    try:
        url = f"https://api.tiingo.com/tiingo/daily/{ticker}?token={TOKEN}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Tiingo API (meta) failed for {ticker}: {str(e)}")
        return None

def get_price(ticker):
    """Fetch price data for a ticker from Tiingo."""
    try:
        url = f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?token={TOKEN}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if not data:
            print(f"No price data found for {ticker}")
            return None
        return data[0]  # Return latest price entry
    except requests.exceptions.RequestException as e:
        print(f"Tiingo API (price) failed for {ticker}: {str(e)}")
        return None
