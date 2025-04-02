import requests

TOKEN = os.environ.get("TIINGO_TOKEN")

headers = {
        'Content-Type': 'application/json',
    }

def get_meta_data(ticker):
    requestResponse = requests.get("https://api.tiingo.com/tiingo/daily/{}?token=   ".format(ticker, TOKEN), headers=headers)
    return requestResponse.json()

def get_price(ticker):
    requestResponse = requests.get("https://api.tiingo.com/tiingo/daily/{}/prices?token=   ".format(ticker, TOKEN), headers=headers)
    return requestResponse.json()[0]
