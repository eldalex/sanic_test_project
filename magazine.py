import hashlib
import requests
import random
from control_db import Control_database

base_url = 'http://127.0.0.1:8000'
private_key = 'very_secret_key!forget it!'


def login_user(username, password):
    res_login = '/auth'
    headers = {'Content-Type': 'application/json'}
    login_body = {'username': username,
                  'password': password}
    url = base_url + res_login
    result = requests.post(url, json=login_body, headers=headers)
    try:
        token = result.json()['access_token']
    except:
        token = 'Authentication Failed.'
    return token


def show_products(username, password, token=None):
    res_show_products = '/get/products'
    if token == None:
        token = login_user(username, password)
    headers_for_validate = {
        "Authorization": f"Bearer {token}"
    }
    url = base_url + res_show_products
    result = requests.get(url, headers=headers_for_validate)
    if result.status_code == 200:
        products = result.json()
        for product in products:
            name = products[product]['Product_header']
            desc = products[product]['Product_description']
            price = products[product]['Product_price']
            print(f"id:{product}, name:{name}, desc:{desc}, price:{price}")

    else:
        print("Ошибка авторизации", result.status_code, result.json())


def deposit_money(username, password, bill_id, amount=0, token=None):
    res_deposit = '/payment/webhook'
    if token == None:
        token = login_user(username, password)
    headers_for_validate = {
        "Authorization": f"Bearer {token}"
    }
    inc_transaction_id = random.randrange(1000, 9999)
    try:
        user_id = Control_database.get_user_id(username)
        amount = amount
        signature = hashlib.sha1()
        signature.update(f'{private_key}:{inc_transaction_id}:{user_id}:{bill_id}:{amount}'.encode())
        body_transaction = {
            "signature": signature.hexdigest(),
            "transaction_id": inc_transaction_id,
            "user_id": user_id,
            "bill_id": bill_id,
            "amount": amount}
        url = base_url + res_deposit
        result = requests.post(url, json=body_transaction, headers=headers_for_validate).json()
    except:
        result = {"error:": "Пользователь не существует"}
    print(result)


def buy_products(login, password, token=None):
    res_buy_products = '/put/bill/buyproduct'
    if token == None:
        token = login_user(login, password)
    headers_for_validate = {
        "Authorization": f"Bearer {token}"
    }
    body_for_buy = {"product_id": 1,
                    "bill_id": 654123}
    url = base_url + res_buy_products
    result = requests.put(url, json=body_for_buy, headers=headers_for_validate)
    print(result.json())


def bill_history(username, password, token=None):
    res_get_bill_history = '/get/bill/history'
    if token == None:
        token = login_user(username, password)
    headers_for_validate = {
        "Authorization": f"Bearer {token}"
    }
    body_for_history = {
        "username": username
    }
    url = base_url + res_get_bill_history
    result = requests.get(url, json=body_for_history, headers=headers_for_validate)
    print(result.json())


def admin_show_users(username, password, token=None):
    res_get_show_users = '/get/admin/showusers'
    if token == None:
        token = login_user(username, password)
    headers_for_validate = {
        "Authorization": f"Bearer {token}"
    }
    body = {
        "username":username
    }
    url = base_url+res_get_show_users
    result = requests.get(url,json=body,headers=headers_for_validate)
    print(result.json())

def admin_act_users(username, password,user_to_act, token=None):
    res_put_admin_act = '/put/admin/endisuser'
    if token == None:
        token = login_user(username, password)
    headers_for_validate = {
        "Authorization": f"Bearer {token}"
    }
    body = {
        "username":username,
        "user_to_act":user_to_act
    }
    url = base_url+res_put_admin_act
    result = requests.put(url,json=body,headers=headers_for_validate)
    print(result.json())

def admin_create_product(username, password,product_header,product_description,product_price, token=None):
    res_post_admin_create = '/post/admin/createproduct'
    if token == None:
        token = login_user(username, password)
    headers_for_validate = {
        "Authorization": f"Bearer {token}"
    }
    body = {
        "username":username,
        "product_header":product_header,
        "product_description":product_description,
        "product_price":product_price
    }
    url = base_url+res_post_admin_create
    result = requests.post(url,json=body,headers=headers_for_validate)
    print(result.json())

def admin_update_product(username, password,product_id, product_header,product_description,product_price, token=None):
    res_put_admin_update = '/put/admin/updateproduct'
    if token == None:
        token = login_user(username, password)
    headers_for_validate = {
        "Authorization": f"Bearer {token}"
    }
    body = {
        "username":username,
        "product_id": product_id,
        "product_header":product_header,
        "product_description":product_description,
        "product_price":product_price
    }
    url = base_url+res_put_admin_update
    result = requests.put(url,json=body,headers=headers_for_validate)
    print(result.json())


def admin_delete_product(username, password,product_id, token=None):
    res_delete_admin_delete = '/delete/admin/deleteproduct'
    if token == None:
        token = login_user(username, password)
    headers_for_validate = {
        "Authorization": f"Bearer {token}"
    }
    body = {
        "username":username,
        "product_id": product_id,
    }
    url = base_url+res_delete_admin_delete
    result = requests.delete(url,json=body,headers=headers_for_validate)
    print(result.json())


if __name__ == '__main__':
    # show_products('Alex2', 'QWErty123')
    # buy_products('Alex2', 'QWErty123')
    # bill_history('Alex', 'QWErty123')
    # deposit_money('Alex', 'QWErty123', 654123, 300)
    # deposit_money("Alex",654123)
    # admin_show_users()
    # admin_act_users('Alex', 'QWErty123',"Alex1")
    # admin_create_product('Alex', 'QWErty123',"Когтеточка","Когтеточка 'столбик', 60 см",35)
    # admin_update_product('Alex', 'QWErty123',3,None,None,30)
    admin_delete_product('Alex', 'QWErty123',5)
    # Control_database.get_users()
