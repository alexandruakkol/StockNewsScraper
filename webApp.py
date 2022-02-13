from flask import Flask, render_template
from engine import run_engine
import json
from time import sleep
from time_checker import time_checker
import concurrent.futures

engine = dict()
tickers, decisions, times, prices, sentences = [], [], [], [], []
app = Flask(__name__)
opn = time_checker()

@app.route("/")
def home():
    return render_template('index.html', opn=opn)

#TODO make multithreading & generate in real-time button/page
@app.route("/signal")
def signal():
    tickers, decisions, times, prices, sentences = [], [], [], [], []
    engine = run_engine()
    for combo in engine:
        tickers.append(list(combo.keys())[0])
        decisions.append(list(combo.values())[0][0])
        times.append(list(combo.values())[0][1])
        prices.append(list(combo.values())[0][2])
        sentences.append(list(combo.values())[0][3])
    return render_template('signal.html', max=max, zip=zip, tickers=tickers, decisions=decisions, times=times, prices=prices, sentences=sentences)

#TODO make dict with classified vars
@app.route("/api", methods=["GET"])
def api():
    return json.dumps(engine)

if __name__ == '__main__':
    app_process = app.run(port=7777, debug=True)


