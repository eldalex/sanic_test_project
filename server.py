from sanic.response import json
from sanic.response import html
from sanic.response import text
from control_db import Control_database
from sanic import Sanic
from sanic_jwt import exceptions
from sanic_jwt import initialize
from sanic_jwt.decorators import protected

app = Sanic(name='My_sanic')


async def authenticate(request):
    if request.method == 'POST':
        username = request.json.get("username")
        password = request.json.get("password")
        user = Control_database.check_user_password(username, password)
        if user != 'fail':
            return user
        else:
            raise exceptions.AuthenticationFailed("Authentication Failed.")


initialize(app, authenticate=authenticate)


@app.route('/', methods=['GET'])
async def get(request):
    test = f'<!DOCTYPE html PUBLIC "-//IETF//DTD HTML 2.0//EN"><HTML><HEAD><TITLE>Так. работаем!</TITLE></HEAD>' \
           '<BODY><H1>Hi there!</H1><P>write something. Maybe hi? </P></BODY></HTML>'
    return html(test)


@app.route('/post/user/create', methods=['POST'])
async def post_user_create(request):
    print(request)
    request_body = request.json
    user_name = request_body['user_name']
    user_pass = request_body['user_pass']
    result = Control_database.create_user(user_name, user_pass)
    if result['status_code'] == 200:
        return json({'user_name': user_name,
                     'user_pass': user_pass,
                     'user_hash': result['result'],
                     "link_for_activation": f"http://127.0.0.1:8000/put/user/activate?key={result['result']}"},
                    status=200)
    else:
        return text(f"user_name: {user_name}; Error: {result['result']}", status=result['status_code'])


@app.route('/get/user/activate', methods=['GET'])
async def get_user_activate(request):
    result = Control_database.activate_user(request.args['key'])
    if result['status_code'] == 200:
        return text(f"{result['result']}", status=200)
    else:
        return text(f"{result['result']}", status=result['status_code'])


@app.route('/get/products', methods=['GET'])
@protected(app)
async def get_products(request):
    products = Control_database.get_all_products()
    return json(products, status=200)


@app.route('/payment/webhook', methods=['POST'])
@protected(app)
async def payment_webhook(request):
    request_body = request.json
    signature = request_body["signature"]
    transaction_id = request_body["transaction_id"]
    user_id = request_body["user_id"]
    bill_id = request_body["bill_id"]
    amount = request_body["amount"]
    if Control_database.check_user_id(user_id):
        if not Control_database.check_bill_id(bill_id):
            Control_database.add_new_bill(user_id, bill_id)
        result = Control_database.deposit_money(bill_id, amount, signature, transaction_id)
        return json(result['result'], status=result['status_code'])
    else:
        return json({"error:": "Пользователь не существует"}, status=501)


@app.route('/put/bill/buyproduct', methods=['PUT'])
@protected(app)
async def put_bill_buy_product(request):
    body = request.json
    product_id = body['product_id']
    bill_id = body['bill_id']
    if Control_database.check_product_id(product_id):
        if Control_database.check_bill_id(bill_id):
            result = Control_database.pay_for_a_purchase(bill_id, product_id)
            print('3')
        else:
            result = {"status_code": 502, "result": f"Ошибка: Такого счета не существует"}
    else:
        result = {"status_code": 503, "result": f"Ошибка: Такого продукта не существует"}

    return json(result['result'], status=result['status_code'])


@app.route('/get/bill/history', methods=['GET'])
@protected(app)
async def get_bill_history(request):
    body = request.json
    username = body['username']
    if Control_database.check_is_enable(username):
        result = Control_database.get_bill_history(username)
    else:
        result = {"status_code": 401, "result": "Пользователь отключен"}
    return json(result['result'], status=result['status_code'])


@app.route('/get/admin/showusers', methods=['GET'])
@protected(app)
async def get_all_users(request):
    body = request.json
    username = body['username']
    if Control_database.check_is_enable(username):
        if Control_database.check_is_admin(username):
            result = Control_database.get_users()
        else:
            result = {"status_code": 400, "result": "Вы не являетесь администратором"}
    else:
        result = {"status_code": 401, "result": "Пользователь отключен"}
    return json(result["result"], status=result["status_code"])


@app.route('/put/admin/endisuser', methods=['PUT'])
@protected(app)
async def put_admin_endisuser(request):
    body = request.json
    username = body['username']
    user_to_act = body['user_to_act']
    if Control_database.check_is_enable(username):
        if Control_database.check_is_admin(username):
            result = Control_database.enable_disable_user(user_to_act)
        else:
            result = {"status_code": 400, "result": "Вы не являетесь администратором"}
    else:
        result = {"status_code": 401, "result": "Пользователь отключен"}
    return json(result["result"], status=result["status_code"])


@app.route('/post/admin/createproduct', methods=['POST'])
@protected(app)
async def post_admin_create_product(request):
    body = request.json
    username = body['username']
    product_header = body["product_header"]
    product_description = body["product_description"]
    product_price = body["product_price"]
    if Control_database.check_is_enable(username):
        if Control_database.check_is_admin(username):
            result = Control_database.create_product(product_header, product_description, product_price)
        else:
            result = {"status_code": 400, "result": "Вы не являетесь администратором"}
    else:
        result = {"status_code": 401, "result": "Пользователь отключен"}
    return json(result["result"], status=result["status_code"])


@app.route('/put/admin/updateproduct', methods=['PUT'])
@protected(app)
async def put_admin_update_product(request):
    body = request.json
    username = body['username']
    product_id = body["product_id"]
    product_header = body["product_header"]
    product_description = body["product_description"]
    product_price = body["product_price"]
    if Control_database.check_is_enable(username):
        if Control_database.check_is_admin(username):
            result = Control_database.update_product(product_id, product_header, product_description, product_price)
        else:
            result = {"status_code": 400, "result": "Вы не являетесь администратором"}
    else:
        result = {"status_code": 401, "result": "Пользователь отключен"}
    return json(result["result"], status=result["status_code"])


@app.route('/delete/admin/deleteproduct', methods=['DELETE'])
@protected(app)
async def del_admin_delete_product(request):
    body = request.json
    username = body['username']
    product_id = body["product_id"]
    if Control_database.check_is_enable(username):
        if Control_database.check_is_admin(username):
            result = Control_database.delete_product(product_id)
        else:
            result = {"status_code": 400, "result": "Вы не являетесь администратором"}
    else:
        result = {"status_code": 401, "result": "Пользователь отключен"}
    return json(result["result"], status=result["status_code"])


if __name__ == '__main__':
    Control_database.create_tables()
    app.run(host='0.0.0.0', port=8000)
