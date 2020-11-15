from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=80, debug=True)