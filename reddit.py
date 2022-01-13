from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import json

stocks_ticker = list()
signals = []
def reddit_signal():
    global trades
    # reddit socket
    url = "https://www.reddit.com/r/stocks/?f=flair_name%3A%22Company%20News%22"
    response = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    webpage = urlopen(response).read()

    # pull article titles
    soup = BeautifulSoup(webpage, "html.parser")
    raw_titles = soup.find_all("h3", {"class": "_eYtD2XCVieq6emjKBH3m"})

    # pull data for each US & CA stock, previously loaded from dumbstockapi.com
    with open("j.json", "r") as file:
        stocks_dict = json.load(file)

    # create list with all stock names
    for stock in stocks_dict:
        dict_element = {stock.get("name").split()[0]:stock.get("ticker").split()[0]}
        stocks_ticker.append(dict_element)

    # build keyword lists
    with open("prohibited.txt", "r") as file:
        prohibited_words = file.read().splitlines()
    with open("positive.txt", "r") as file:
        positive_keywords = file.read().splitlines()
    with open("negative.txt", "r") as file:
        negative_keywords = file.read().splitlines()
    # iterate through each title found
    for sentence in raw_titles:
        news = []
        referred_stock = None
        decision = None
        for positive_combo, negative_combo in zip(positive_keywords, negative_keywords):
            if positive_combo.lower() in sentence.string.lower():
                decision = "Buy"
                #print(f"Recognized {decision} from title {sentence.string}, because of word: {positive_combo.lower()}")
            if negative_combo.lower() in sentence.string.lower():
                decision = "Sell"
                #print(f"Recognized {decision} from title {sentence.string}, because of word: {negative_combo.lower()}")

    # iterate through each word of each sentence
        for word in sentence.string.split():
            news.append(word)
            if word in set().union(*(d.keys() for d in stocks_ticker)) and word not in prohibited_words:
                referred_stock = word
                #print(f"Recognized {referred_stock} from title {sentence.string}")
                break
        if decision is not None and referred_stock is not None:
            referred_ticker = [pair.get(referred_stock) for pair in stocks_ticker if referred_stock in pair]
            print(f"    Signal: {decision} {referred_ticker[0]} from", f"article: {sentence.string}. Source: reddit")
            signals.append({referred_ticker[0]:decision})

        pass
    return signals
