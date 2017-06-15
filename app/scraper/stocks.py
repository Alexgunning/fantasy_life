import datetime
import requests
import re
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
    ticker_symbols = ["A", "AAPL", "C", "FB", "GOOG", "HOG", "HPQ", "INTC", "KO", "LUV", "MMM", "MSFT"]

    players = db.players
    stock = db.stock
    stock.drop()
    users = players.find()
    for ticker_symbol, users in zip(ticker_symbols, users):
        data = {"associated_player_id": users['_id'], "ticker_symbol": ticker_symbol}
        _ = stock.insert(data)

def get_stock_metadata():
    """Get stock metadata (Full company names"""
    stock = db.stock

    ticker_symbols = [stock['ticker_symbol'] for stock in stock.find()]
    for ticker_symbol in ticker_symbols:
        query =  "https://www.quandl.com/api/v3/datasets/WIKI/%s/metadata.json?api_key=HsseMLtznjVcx2sHmDGt"%ticker_symbol
        stock_name = requests.get(query).json()['dataset']['name']
        stock_name = stock_name.split('(')[0]
        stock.update_one({
            'ticker_symbol': ticker_symbol
            }, {
                '$set': {
                    'stock_name': stock_name
                }
            })

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


create_stock_db()
get_stock_metadata()

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