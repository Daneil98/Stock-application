import requests


headers = {
        'Content-Type': 'application/json',
    }

def get_meta_data(ticker):
    requestResponse = requests.get("https://api.tiingo.com/tiingo/daily/{}?token=ade8eea34c1658569b3997046a22003af1a3ad08".format(ticker), headers=headers)
    return requestResponse.json()

def get_price(ticker):
    requestResponse = requests.get("https://api.tiingo.com/tiingo/daily/{}/prices?token=ade8eea34c1658569b3997046a22003af1a3ad08".format(ticker), headers=headers)
    return requestResponse.json()[0]