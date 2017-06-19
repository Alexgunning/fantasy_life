"""Pulling down data for stocks"""
import datetime
import requests
from flask_pymongo import MongoClient

client = MongoClient()
db = client.fantasy

# quarter three start
# tracking delta between now and start

QUARTER_THREE_START = datetime.date(2016, 10, 3)
CURRENT_DATE = datetime.datetime.now()

print(CURRENT_DATE)

api_key = "h81FgPPmka77HPc_Mnkj"


#TODO Change to use Quandl library and may be able to bundle requests

def create_stock_db():
    """Make new database for stocks"""
    ticker_symbols = ["A", "AAPL", "FB", "GOOG", "HOG", "HPQ", "INTC", "KO", "LUV",\
     "MMM", "MSFT", "WMT"]

    players = db.players
    stocks = db.stocks
    stocks.drop()
    users = players.find()
    for ticker_symbol, user in zip(ticker_symbols, users):
        data = {"associated_player_id": user['_id'], "ticker_symbol": ticker_symbol}
        _ = stocks.insert(data)

def get_stock_metadata():
    """Get stock metadata (Full company names)"""
    stock = db.stocks
    ticker_symbols = [stocks['ticker_symbol'] for stocks in stock.find()]

    for ticker_symbol in ticker_symbols:
        query = "https://www.quandl.com/api/v3/datasets/WIKI/%s/metadata.json?api_key=%s"\
        %(ticker_symbol, api_key)
        stock_name = requests.get(query).json()['dataset']['name']
        shortened_stock_name = stock_name.split('(')[0].strip()
        stock.update_one({
            'ticker_symbol': ticker_symbol
            }, {
                '$set': {
                    'stock_name': shortened_stock_name
                }
            })

def stock_data(stock):
    """Get stock data based on stock ticker"""

    query = "https://www.quandl.com/api/v3/datasets/WIKI/%s/data.json?api_key=%s"%(stock, api_key)
    daily_results = requests.get(query).json()['dataset_data']['data']
    #Get the most recent price (first in array)
    #Closing price is 5th element
    current_price = float(daily_results[0][4])
    #TODO Binary search
    #Or find postion based on start, stop and frequency
    for day in daily_results:
        if day[0] == str(QUARTER_THREE_START):
            # start_price = float(day[0][4])
            start_price = float(day[4])
            break
    delta = (current_price-start_price)/start_price
    return {"ticker_symbol": stock, "current_price" : current_price, "start_price" : start_price,\
    "delta" : delta}

def update_stock_data():
    """Get all off the stocks data and update the database"""
    stock = db.stocks
    ticker_symbols = [stocks['ticker_symbol'] for stocks in stock.find()]
    stock_info = [stock_data(ticker_symbol) for ticker_symbol in ticker_symbols]
    for stock_price in stock_info:
        stock.update_one({
            'ticker_symbol': stock_price['ticker_symbol']
            }, {
                '$set': {
                    'current_price': stock_price['current_price'],
                    'start_price': stock_price['start_price'],
                    'delta': stock_price['delta']
                }
            })


create_stock_db()
get_stock_metadata()
update_stock_data()

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
