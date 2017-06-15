import datetime
import requests
from flask_pymongo import MongoClient

client = MongoClient()
db = client.fantasy

# quarter three start
# tracking delta between now and start 

QUARTER_THREE_START = datetime.date(2016,10,1)
CURRENT_DATE = datetime.datetime.now()

print(CURRENT_DATE)

api_key = "hssemltznjvcx2shmdgt"

def create_stock_db():
    """Make new database for stocks"""
    ticker_symbols = ["A", "AAPL", "C", "GOOG", "HOG", "HPQ", "INTC", "KO", "LUV", "MMM", "MSFT"]
    #"T", "TGT", "TXN", "WMT"]

    players = db.players
    stock = db.stock
    stock.drop()
    users = players.find()
    for ticker_symbols, users in zip(player_web_names, player_view_names, users):
        data = {"associated_player_id": users['_id'], "ticker_symbols": ticker_symbols}
        _ = stock.insert(data)

def get_stock_metadata():
    """Get stock metadata (Full company names"""
    ticker_symbols = ["A", "AAPL", "C", "GOOG", "HOG", "HPQ", "INTC", "KO", "LUV", "MMM", "MSFT"]
    #"T", "TGT", "TXN", "WMT"]

    players = db.players
    stock = db.stock
    stock.drop()
    users = players.find()
    for ticker_symbols, users in zip(player_web_names, player_view_names, users):
        data = {"associated_player_id": users['_id'], "ticker_symbols": ticker_symbols}
        _ = stock.insert(data)

def stock_data(stock):
    """Get stock data based on stock ticker"""

    query = "https://www.quandl.com/api/v3/datasets/WIKI/%s/data.json?api_key\
    =HsseMLtznjVcx2sHmDGt&start_date=2014-01-01"%stock

    daily_results = requests.get(query).json()['dataset_data']['data']
    #Get the most recent price (first in array)
    #Closing price is 5th element
    current_price = float(daily_results[0][4])
    #TODO Binary search
    #Or find postion based on start, stop and frequency
    for day in daily_results:
        if day == str(QUARTER_THREE_START):
            start_price = float(day[0][4])
            break
    delta = (current_price-start_price)/start_price
    return {"current_price" : current_price, "start_price" : start_price, "delta" : delta}





#print(res['data'])
# A – Agilent Technologies
# AAPL – Apple Inc.
# C – Citigroup
# GOOG – Alphabet Inc.
# HOG – Harley-Davidson Inc.
# HPQ – Hewlett-Packard
# INTC – Intel
# KO – The Coca-Cola Company
# LUV - Southwest Airlines (after their main hub at Love Field)
# MMM – Minnesota Mining and Manufacturing (3M)
# MSFT – Microsoft
# T - AT&T
# TGT – Target Corporation
# TXN – Texas Instruments
# WMT – Walmart