from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('mongodb://test:test@localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index1.html')


## API 역할을 하는 부분

@app.route('/category', methods=['POST'])
def set_category():
    category_receive = request.form['category_give']
    fields_receive = request.form.getlist('fields_give[]')

    # 중복체크
    # category_receive 데이터가 존재하는지 조회
    category = db.category_info.find_one({'name': category_receive}, {'_id': False})
    if category is not None:
        # 데이터가 존재하면 저장하지 않음
        return jsonify({'result': 'false'})
    else:
        index = len(list(db.category_info.find({}))) + 1
        fields = [];
        for idx, val in enumerate(fields_receive):
            fields.append({'idx':idx, 'title':val})

        collection = {'name': category_receive, 'index': index, 'fields':fields}
        db.category_info.insert_one(collection)

    return jsonify({'result': 'success'})


@app.route('/category/data', methods=['POST'])
def set_data():
    request_recive = request.form.to_dict();

    index = db.category_info.find_one({'name': request_recive['category_give']})['index']
    info = {}
    for i in range(10):
        try:
            info['field' + request_recive['fields['+str(i)+'][idx]']] = request_recive['fields['+str(i)+'][content]']
        except:
            break

    db["collection" + str(index)].insert_one(info)

    return jsonify({'result': 'success', 'msg': '리뷰가 성공적으로 작성되었습니다.'})


@app.route('/category', methods=['GET'])
def bring_category():
    # 1. DB에서 리뷰 정보 모두 가져오기
    categories = list(db.category_info.find({}, {'_id': 0}))
    # 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'result': 'success', 'categories': categories})

@app.route('/category/data', methods=['GET'])
def bring_reviews():
    category_receive = request.args.get('category_give')
    index = db.category_info.find_one({'name': category_receive})['index']
    databases = list(db["collection" + str(index)].find({}, {'_id': 0}))
    category = db.category_info.find_one({'name': category_receive}, {'_id': False})
    return jsonify({'result': 'success', 'reviews': databases, 'category':category})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
