import requests
from datetime import datetime
from investopedia import investopedia_signal

trades = []
api_data = {}

def run_engine():
    global trades
    trades = []
    print("Running scraper ...")

    def open_trade(ticker, decision, sentence):
        global trades
        now = datetime.now()
        minute = now.strftime("%M")
        list_of_active = []
        if ticker not in list_of_active:
            # get current ticker price
            # get api key from iexcloud.io
            apikey = "pk_d40b5f30ace045d9b25f7fc9cac8b0fd"
            headers = {'Content-Type': 'application/json'}
            url = f"https://cloud.iexapis.com/stable/stock/{ticker}/quote?token={apikey}"
            response = requests.get(url, headers=headers)
            if response.ok is False:
                return None
            price = response.json()["latestPrice"]
            trades.append({ticker: [decision, f"{datetime.now().hour}:{minute}", price, sentence]})
        # returns global 'trades'

    signals = investopedia_signal()

    for combo in signals:
        open_trade(list(combo[0].keys())[0], list(combo[0].values())[0], combo[1])
    for trade in trades:
        symbol = list(trade.keys())[0]
        array = list(trade.values())[0]
        signal = array[0]
        time = array[1]
        price = array[2]
        statement = array[3]
        api_data[symbol] = {"signal": signal, "time": time, "price": price, "statement": statement}
    return [trades, api_data]

