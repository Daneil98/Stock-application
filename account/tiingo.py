import requests


headers = {
        'Content-Type': 'application/json',
    }

def get_meta_data(ticker):
    requestResponse = requests.get("https://api.tiingo.com/tiingo/daily/{}?token=   ".format(ticker), headers=headers)
    return requestResponse.json()

def get_price(ticker):
    requestResponse = requests.get("https://api.tiingo.com/tiingo/daily/{}/prices?token=   ".format(ticker), headers=headers)
    return requestResponse.json()[0]
