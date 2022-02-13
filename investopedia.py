from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import json

def investopedia_signal():

    stocks_ticker = list()
    tickers_only = list()
    signals = []
    # reddit socket
    url = "https://www.investopedia.com/company-news-4427705"
    response = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    webpage = urlopen(response).read()

    # pull article titles
    soup = BeautifulSoup(webpage, "html.parser")
    mydivs = soup.find_all("span", {"class": "card__title-text"})

    # pull data for each US & CA stock, previously loaded from dumbstockapi.com
    with open("j.json", "r") as file:
        stocks_dict = json.load(file)

    # create list with all stock names and ticker symbols
    for stock in stocks_dict:
        dict_element = {stock.get("name").split()[0]:stock.get("ticker").split()[0]}
        stocks_ticker.append(dict_element)
        tickers_only.append(stock.get("ticker").split()[0])

    # build keyword lists
    with open("prohibited.txt", "r") as file:
        prohibited_words = file.read().splitlines()
    with open("positive.txt", "r") as file:
        positive_keywords = file.read().splitlines()
    with open("negative.txt", "r") as file:
        negative_keywords = file.read().splitlines()
    with open("prohibited_tickers.txt", "r") as file:
        prohibited_tickers = file.read().splitlines()

    # iterate through each title found
    for sentence in mydivs:
        #print(sentence)
        referred_stock = None
        referred_ticker = None
        decision = None

        ##DETECTS SENTIMENT WORDS IN TITLE
        for positive_combo, negative_combo in zip(positive_keywords, negative_keywords):
            if positive_combo.lower() in sentence.string.lower():
                decision = "Buy"
                #print(f"Recognized {decision} from title {sentence.string}, because of word: {positive_combo.lower()}")
            if negative_combo.lower() in sentence.string.lower():
                decision = "Sell"
                #print(f"Recognized {decision} from title {sentence.string}, because of word: {negative_combo.lower()}")

    # iterate through each word of each sentence
        for word in sentence.string.split():
            if word in tickers_only:
                if word not in prohibited_tickers:
                    ##DETECTS TICKER SYMBOLS IN TITLE
                    referred_ticker = word
                    #print(f"Recognized {referred_ticker} from article: {sentence.string}, source: investopedia.")
                    break

            ##DETECTS COMPANY NAME FROM TITLE
            if word in set().union(*(d.keys() for d in stocks_ticker)) and word not in prohibited_words:
                referred_stock = word
                #print(f"Recognized {referred_stock} from article: {sentence.string}, source: investopedia.")
                break

        if decision is not None:
            if referred_ticker is not None:
                signals.append([{referred_ticker[0]:decision},sentence.string])
                #print(f"    Signal: {decision} {referred_ticker[0]} from", f"article: {sentence.string}. Source: investopedia")
            if referred_stock is not None and referred_ticker is None:
                referred_ticker = [pair.get(referred_stock) for pair in stocks_ticker if referred_stock in pair]
                #print(f"    Signal: {decision} {referred_ticker[0]} from", f"article: {sentence.string}. Source: investopedia")
                signals.append([{referred_ticker[0]:decision},sentence.string])
        pass
    return signals
