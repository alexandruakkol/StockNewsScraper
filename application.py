from flask import Flask, render_template, request
from engine import run_engine
from time_checker import time_checker

engine = dict()
tickers, decisions, times, prices, sentences = [], [], [], [], []
application = Flask(__name__)
opn = time_checker()

engine = run_engine()

@application.route("/")
def home():
    return render_template('index.html', opn=opn)

#TODO make multithreading
@application.route("/signal",methods=["GET"])
def signal():
    print('client time:',request.__dict__.items())
    tickers, decisions, times, prices, sentences = [], [], [], [], []

    for combo in engine[0]:
        tickers.append(list(combo.keys())[0])
        decisions.append(list(combo.values())[0][0])
        times.append(list(combo.values())[0][1])
        prices.append(list(combo.values())[0][2])
        sentences.append(list(combo.values())[0][3])
    return render_template('signal.html', max=max, zip=zip, tickers=tickers, decisions=decisions, times=times, prices=prices, sentences=sentences)

@application.route("/realtime")
def realtime():

    engine = run_engine() #what differenciates /realtime from /signal => data run_engine is called on function

    tickers, decisions, times, prices, sentences = [], [], [], [], []

    for combo in engine[0]:
        tickers.append(list(combo.keys())[0])
        decisions.append(list(combo.values())[0][0])
        times.append(list(combo.values())[0][1])
        prices.append(list(combo.values())[0][2])
        sentences.append(list(combo.values())[0][3])
    print('realtime engine in app:',engine)
    return render_template('signal.html', max=max, zip=zip, tickers=tickers, decisions=decisions, times=times, prices=prices, sentences=sentences)

#TODO make dict with classified vars
@application.route("/api", methods=["GET"])
def api():
    return engine[1]

if __name__ == '__main__':
    app_process = application.run(port=7777, debug=True)



