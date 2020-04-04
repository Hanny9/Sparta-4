from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient  # pymongo를 임포트 하기

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('homework.html')

## API 역할을 하는 부분
@app.route('/orders', methods=['POST'])
def write_orders():
    # id_receive로 클라이언트가 준 데이터 가져오기
    name_receive = request.form['name_give']
    quantity_receive = request.form['quantity_give']
    address_receive = request.form['address_give']
    mobile_receive = request.form['mobile_give']

    # DB에 삽입할 purchase_order 만들기
    purchase_order = {
        'name': name_receive,
        'quantity': quantity_receive,
        'address': address_receive,
        'mobile': mobile_receive,
    }
    # purchase_orders에 purchase_order 저장하기
    db.purchase_orders.insert_one(purchase_order)
    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success', 'msg': '주문이 성공적으로 접수되었습니다.'})

@app.route('/orders', methods=['GET'])
def read_orders():
	# 1. DB에서 주문 정보 모두 가져오기
    order_history = list(db.purchase_orders.find({},{'_id':0}))
	# 2. 성공 여부 & 주문내역 반환하기
    return jsonify({'result': 'success', 'order_history': order_history})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)