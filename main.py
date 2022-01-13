import requests
from datetime import datetime
from time import sleep
from reddit import reddit_signal
from investopedia import investing_com_signal

use_time_checker = False # checks if U.S market is open

news = list()
trades = []

def open_trade(ticker, decision):
    global trades
    list_of_active = [list(item.keys()) for item in trades]
    list_of_active = [item for sublist in list_of_active for item in sublist]

    if ticker not in list_of_active:
        # get current ticker price
        # get api key from iexcloud.io
        apikey = "pk_d40b5f30ace045d9b25f7fc9cac8b0fd"
        headers = {'Content-Type': 'application/json'}
        url = f"https://cloud.iexapis.com/stable/stock/{ticker}/quote?token={apikey}"
        response = requests.get(url, headers=headers)
        price = response.json()["latestPrice"]
        trades.append({ticker:[decision, datetime.now(), price]})
    # write trades to txt
        with open("output.txt", "a") as file:
            file.writelines(f"{ticker}, {decision}, {price} {datetime.now().hour}:{datetime.now().minute}.\n")

    # generates global 'trades'

def time_checker():

    # get current time
    working_days = [0, 1, 2, 3, 4]  # monday to friday
    now = datetime.now()
    # check if during operational hours
    if datetime.today().weekday() not in working_days:
        raise RuntimeError("Stock markets are not open on weekends.")
    if now.hour >= 16 and now.hour <= 20:
        if now.hour == 16:
            if now.minute < 30:
                raise RuntimeError("Market not open at this time.")
        if now.hour == 20:
            if now.minute > 48:
                raise RuntimeError("Market closes soon. Cannot trade.")
    else:
        raise RuntimeError("Market not open at this time.")

# clear file on program start
with open("output.txt", "w") as _:
    pass

while True:
    if use_time_checker:
        time_checker()
    signals = reddit_signal()
    for pair in investing_com_signal():
        if list(pair.keys())[0] not in [list(item.keys())[0] for item in signals]:
            signals.append(pair)
        else:
            pass
    for combo in signals:
        open_trade(list(combo.keys())[0], combo.get(list(combo.keys())[0]))

    print("Trades written to output.txt.")
    print("Waiting 5s.")
    sleep(5)


