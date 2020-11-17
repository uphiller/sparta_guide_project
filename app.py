from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
client = MongoClient('mongodb://test:test@localhost',27017)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/place', methods=['POST'])
def save_place():
    x_receive = request.form['x_give']
    y_receive = request.form['y_give']
    comment_receive = request.form['comment_give']
    place = {'x': x_receive, 'y': y_receive, 'comment':comment_receive}
    db.places.insert_one(place)
    return jsonify({'result': 'success'})

@app.route('/place', methods=['GET'])
def show_place():
    x_receive = request.args.get('x_give')
    y_receive = request.args.get('y_give')
    place = db.places.find_one({'x': x_receive, 'y': y_receive}, {'_id': 0})
    return jsonify({'result': 'success', 'place': place})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)