import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.tododb


@app.route('/')
def todo():
    _items = db.tododb.find()
    items = [item for item in _items]
    itemsStr = str(items)
    return itemStr
    


@app.route('/new', methods=['POST'])
def new():

    item_doc = {
        'name': request.form['name'],
        'description': request.form['description']
    }
    db.tododb.insert_one(item_doc)

    return "Inserted"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
