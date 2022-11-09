import hashlib
import json
import random

from requests import Response
from http_method import Http_methods

base_url = 'http://127.0.0.1:8000'
private_key = 'very_secret_key!forget it!'


class Test_custom_api():

    @staticmethod
    def login_user(username, password):
        res_login = '/auth'
        headers = {'Content-Type': 'application/json'}
        login_body = {'username': username,
                      'password': password}
        url = base_url + res_login
        result = Http_methods.post(url, login_body, headers)
        try:
            token = result.json()['access_token']
        except:
            token = 'Authentication Failed.'
        return token

    @staticmethod
    def test_create_new_user():
        post_body = {"user_name": f"Alex{random.randint(1, 1000)}",
                     "user_pass": "QWErty123"}
        res_create = '/post/user/create'
        res_activate = '/get/user/activate'
        url = base_url + res_create
        result = Http_methods.post(url, post_body)
        assert result.status_code == 200
        js_res = result.json()
        url = js_res["link_for_activation"]
        print(f'Пользователь успешно создан! ссылка на активацию:{url}')
        print('Переходим по ссылке...')
        result = Http_methods.get(url)
        assert result.status_code == 200
        print(result.text)

    @staticmethod
    def test_repeat_create_user():
        post_body = {"user_name": f"test_user",
                     "user_pass": "test_user"}
        res_create = '/post/user/create'
        res_activate = '/get/user/activate'
        url = base_url + res_create
        result = Http_methods.post(url, post_body)
        assert result.status_code == 501
        print(result.text)

    @staticmethod
    def test_activate_new_user():
        put_body = {}
        res = '/get/user/activate'
        key = '?key=a08372b70196c21a9229cf04db6b7cea'
        url = base_url + res + key
        result = Http_methods.get(url)
        print(result.text)

    @staticmethod
    def test_success_login_user():
        res_login = '/auth'
        headers = {'Content-Type': 'application/json'}
        login_body = {'username': "test_user",
                      'password': "test_user"}
        url = base_url + res_login
        result = Http_methods.post(url, login_body, headers)
        assert result.status_code == 200
        print(f"Аутентификация успешна! ваш токен:{result.json()['access_token']}")

    @staticmethod
    def test_fail_login_user():
        res_login = '/auth'
        headers = {'Content-Type': 'application/json'}
        login_body = {'username': "fake_login",
                      'password': "fake_login"}
        url = base_url + res_login
        result = Http_methods.post(url, login_body, headers)
        assert result.status_code == 500
        print('Аутентификация провалена!')

    @staticmethod
    def test_show_products_auth():
        res_show_products = '/get/products'
        token = Test_custom_api.login_user('test_user', "test_user")
        headers_for_validate = {
            "Authorization": f"Bearer {token}"
        }
        url = base_url + res_show_products
        result = Http_methods.get(url, headers=headers_for_validate)
        assert result.status_code == 200
        products = result.json()
        for product in products:
            name = products[product]['Product_header']
            desc = products[product]['Product_description']
            price = products[product]['Product_price']
            print(f"id:{product}, name:{name}, desc:{desc}, price:{price}")

    @staticmethod
    def test_show_products_no_auth():
        res_show_products = '/get/products'
        token = Test_custom_api.login_user('fake_login', "fake_login")
        headers_for_validate = {
            "Authorization": f"Bearer {token}"
        }
        url = base_url + res_show_products
        result = Http_methods.get(url, headers=headers_for_validate)
        assert result.status_code == 401
        print('Неудачная авторизация')

    @staticmethod
    def test_deposit_money():
        res_deposit = '/payment/webhook'
        token = Test_custom_api.login_user('test_user', 'test_user')
        headers_for_validate = {"Authorization": f"Bearer {token}"}
        inc_transaction_id = random.randrange(1000, 9999)
        user_id = 2
        amount = 1000
        bill_id = 999999
        signature = hashlib.sha1()
        signature.update(f'{private_key}:{inc_transaction_id}:{user_id}:{bill_id}:{amount}'.encode())
        body_transaction = {
            "signature": signature.hexdigest(),
            "transaction_id": inc_transaction_id,
            "user_id": user_id,
            "bill_id": bill_id,
            "amount": amount}
        url = base_url + res_deposit
        result = Http_methods.post(url, body_transaction, headers_for_validate)
        assert result.status_code == 200
        print(json.dumps(result.json(), indent=2, ensure_ascii=False))

    @staticmethod
    def test_deposit_one_money():
        res_deposit = '/payment/webhook'
        token = Test_custom_api.login_user('test_user', 'test_user')
        headers_for_validate = {"Authorization": f"Bearer {token}"}
        inc_transaction_id = random.randrange(1000, 9999)
        user_id = 2
        amount = 1
        bill_id = 999998
        signature = hashlib.sha1()
        signature.update(f'{private_key}:{inc_transaction_id}:{user_id}:{bill_id}:{amount}'.encode())
        body_transaction = {
            "signature": signature.hexdigest(),
            "transaction_id": inc_transaction_id,
            "user_id": user_id,
            "bill_id": bill_id,
            "amount": amount}
        url = base_url + res_deposit
        result = Http_methods.post(url, body_transaction, headers_for_validate)
        assert result.status_code == 200
        print(json.dumps(result.json(), indent=2, ensure_ascii=False))

    @staticmethod
    def test_fail_deposit_money():
        res_deposit = '/payment/webhook'
        token = Test_custom_api.login_user('fake_login', 'fake_login')
        headers_for_validate = {"Authorization": f"Bearer {token}"}
        inc_transaction_id = random.randrange(1000, 9999)
        user_id = 2222
        amount = 1000
        bill_id = 88888
        signature = hashlib.sha1()
        signature.update(f'{private_key}:{inc_transaction_id}:{user_id}:{bill_id}:{amount}'.encode())
        body_transaction = {
            "signature": signature.hexdigest(),
            "transaction_id": inc_transaction_id,
            "user_id": user_id,
            "bill_id": bill_id,
            "amount": amount}
        url = base_url + res_deposit
        result = Http_methods.post(url, body_transaction, headers_for_validate)
        assert result.status_code == 401
        print(json.dumps(result.json(), indent=2, ensure_ascii=False))

    @staticmethod
    def test_buy_products():
        res_buy_products = '/put/bill/buyproduct'
        token = Test_custom_api.login_user('test_user', 'test_user')
        headers_for_validate = {
            "Authorization": f"Bearer {token}"
        }
        body_for_buy = {"product_id": 1,
                        "bill_id": 999999}
        url = base_url + res_buy_products
        result = Http_methods.put(url, body_for_buy, headers_for_validate)
        assert result.status_code == 200
        print(json.dumps(result.json(), indent=2, ensure_ascii=False))

    @staticmethod
    def test_fail_buy_products():
        res_buy_products = '/put/bill/buyproduct'
        token = Test_custom_api.login_user('test_user', 'test_user')
        headers_for_validate = {
            "Authorization": f"Bearer {token}"
        }
        body_for_buy = {"product_id": 1,
                        "bill_id": 999998}
        url = base_url + res_buy_products
        result = Http_methods.put(url, body_for_buy, headers_for_validate)
        assert result.status_code == 400
        print(json.dumps(result.json(), indent=2, ensure_ascii=False))

    @staticmethod
    def test_fail_login_buy_products():
        res_buy_products = '/put/bill/buyproduct'
        token = Test_custom_api.login_user('fake_login', 'fake_login')
        headers_for_validate = {
            "Authorization": f"Bearer {token}"
        }
        body_for_buy = {"product_id": 1,
                        "bill_id": 999999}
        url = base_url + res_buy_products
        result = Http_methods.put(url, body_for_buy, headers_for_validate)
        assert result.status_code == 401
        print(json.dumps(result.json(), indent=2, ensure_ascii=False))

    @staticmethod
    def test_bill_history():
        res_get_bill_history = '/get/bill/history'
        token = Test_custom_api.login_user('test_user', 'test_user')
        headers_for_validate = {"Authorization": f"Bearer {token}"}
        body_for_history = {"username": 'test_user'}
        url = base_url + res_get_bill_history
        result = Http_methods.get(url, body_for_history, headers_for_validate)
        assert result.status_code == 200
        print(json.dumps(result.json(), indent=2, ensure_ascii=False))

    @staticmethod
    def test_fail_bill_history():
        res_get_bill_history = '/get/bill/history'
        token = Test_custom_api.login_user('fake_login', 'fake_login')
        headers_for_validate = {"Authorization": f"Bearer {token}"}
        body_for_history = {"username": 'test_user'}
        url = base_url + res_get_bill_history
        result = Http_methods.get(url, body_for_history, headers_for_validate)
        assert result.status_code == 401
        print(json.dumps(result.json(), indent=2, ensure_ascii=False))

    @staticmethod
    def test_admin_show_users():
        res_get_show_users = '/get/admin/showusers'
        token = Test_custom_api.login_user('admin', 'admin')
        headers_for_validate = {"Authorization": f"Bearer {token}"}
        body = {"username": "admin"}
        url = base_url + res_get_show_users
        result = Http_methods.get(url, body, headers_for_validate)
        assert result.status_code == 200
        print(json.dumps(result.json(), indent=2, ensure_ascii=False))

    @staticmethod
    def test_user_show_users():
        res_get_show_users = '/get/admin/showusers'
        token = Test_custom_api.login_user('test_user', 'test_user')
        headers_for_validate = {"Authorization": f"Bearer {token}"}
        body = {"username": "test_user"}
        url = base_url + res_get_show_users
        result = Http_methods.get(url, body, headers_for_validate)
        assert result.status_code == 400
        print(json.dumps(result.json(), indent=2, ensure_ascii=False))

    @staticmethod
    def test_disable_user_show_users():
        res_get_show_users = '/get/admin/showusers'
        token = Test_custom_api.login_user('disable_user', 'disable_user')
        headers_for_validate = {"Authorization": f"Bearer {token}"}
        body = {"username": "disable_user"}
        url = base_url + res_get_show_users
        result = Http_methods.get(url, body, headers_for_validate)
        assert result.status_code == 401
        print(json.dumps(result.json(), indent=2, ensure_ascii=False))

    @staticmethod
    def test_admin_disable_users():
        res_put_admin_act = '/put/admin/endisuser'
        token = Test_custom_api.login_user('admin', 'admin')
        headers_for_validate = {"Authorization": f"Bearer {token}"}
        body = {"username": 'admin',
                "user_to_act": 'test_user'}
        url = base_url + res_put_admin_act
        result = Http_methods.put(url, body, headers_for_validate)
        print(json.dumps(result.json(), indent=2, ensure_ascii=False))

    @staticmethod
    def test_admin_enable_users():
        res_put_admin_act = '/put/admin/endisuser'
        token = Test_custom_api.login_user('admin', 'admin')
        headers_for_validate = {"Authorization": f"Bearer {token}"}
        body = {"username": 'admin',
                "user_to_act": 'test_user'}
        url = base_url + res_put_admin_act
        result = Http_methods.put(url, body, headers_for_validate)
        print(json.dumps(result.json(), indent=2, ensure_ascii=False))


    @staticmethod
    def test_admin_create_product():
        res_post_admin_create = '/post/admin/createproduct'
        token = Test_custom_api.login_user('admin', 'admin')
        headers_for_validate = {"Authorization": f"Bearer {token}"}
        body = {
            "username": 'admin',
            "product_header": f"Test product{random.randint(10, 100)}",
            "product_description": f"Test product description",
            "product_price": random.randint(10, 100)
        }
        url = base_url + res_post_admin_create
        result = Http_methods.post(url, body, headers_for_validate)
        assert result.status_code == 200
        print(json.dumps(result.json(), indent=2, ensure_ascii=False))

    @staticmethod
    def test_user_create_product():
        res_post_admin_create = '/post/admin/createproduct'
        token = Test_custom_api.login_user('test_user', 'test_user')
        headers_for_validate = {"Authorization": f"Bearer {token}"}
        body = {
            "username": 'test_user',
            "product_header": f"Test product{random.randint(10, 100)}",
            "product_description": f"Test product description",
            "product_price": random.randint(10, 100)
        }
        url = base_url + res_post_admin_create
        result = Http_methods.post(url, body, headers_for_validate)
        assert result.status_code == 400
        print(json.dumps(result.json(), indent=2, ensure_ascii=False))

    @staticmethod
    def test_disable_user_create_product():
        res_post_admin_create = '/post/admin/createproduct'
        token = Test_custom_api.login_user('disable_user', 'disable_user')
        headers_for_validate = {"Authorization": f"Bearer {token}"}
        body = {
            "username": 'disable_user',
            "product_header": f"Test product{random.randint(10, 100)}",
            "product_description": f"Test product description",
            "product_price": random.randint(10, 100)
        }
        url = base_url + res_post_admin_create
        result = Http_methods.post(url, body, headers_for_validate)
        assert result.status_code == 401
        print(json.dumps(result.json(), indent=2, ensure_ascii=False))

    @staticmethod
    def test_admin_update_product():
        res_put_admin_update = '/put/admin/updateproduct'
        token = Test_custom_api.login_user('admin', 'admin')
        headers_for_validate = {"Authorization": f"Bearer {token}"}
        body = {
            "username": 'admin',
            "product_id": 1,
            "product_header": "New product header",
            "product_description": "New product description",
            "product_price": 200
        }
        url = base_url + res_put_admin_update
        result = Http_methods.put(url, body, headers_for_validate)
        assert result.status_code == 200
        print(json.dumps(result.json(), indent=2, ensure_ascii=False))

    @staticmethod
    def test_user_update_product():
        res_put_admin_update = '/put/admin/updateproduct'
        token = Test_custom_api.login_user('test_user', 'test_user')
        headers_for_validate = {"Authorization": f"Bearer {token}"}
        body = {
            "username": 'test_user',
            "product_id": 1,
            "product_header": "New product header",
            "product_description": "New product description",
            "product_price": 200
        }
        url = base_url + res_put_admin_update
        result = Http_methods.put(url, body, headers_for_validate)
        assert result.status_code == 400
        print(json.dumps(result.json(), indent=2, ensure_ascii=False))

    @staticmethod
    def test_disable_user_update_product():
        res_put_admin_update = '/put/admin/updateproduct'
        token = Test_custom_api.login_user('disable_user', 'disable_user')
        headers_for_validate = {"Authorization": f"Bearer {token}"}
        body = {
            "username": 'disable_user',
            "product_id": 1,
            "product_header": "New product header",
            "product_description": "New product description",
            "product_price": 200
        }
        url = base_url + res_put_admin_update
        result = Http_methods.put(url, body, headers_for_validate)
        assert result.status_code == 401
        print(json.dumps(result.json(), indent=2, ensure_ascii=False))

    @staticmethod
    def test_admin_delete_product():
        res_delete_admin_delete = '/delete/admin/deleteproduct'
        token = Test_custom_api.login_user('admin', 'admin')
        headers_for_validate = {"Authorization": f"Bearer {token}"}
        body = {
            "username": 'admin',
            "product_id": 1,
        }
        url = base_url + res_delete_admin_delete
        result = Http_methods.delete(url, body, headers_for_validate)
        assert result.status_code == 200
        print(json.dumps(result.json(), indent=2, ensure_ascii=False))

    @staticmethod
    def test_admin_alredy_delete_product():
        res_delete_admin_delete = '/delete/admin/deleteproduct'
        token = Test_custom_api.login_user('admin', 'admin')
        headers_for_validate = {"Authorization": f"Bearer {token}"}
        body = {"username": 'admin',
            "product_id": 2}
        url = base_url + res_delete_admin_delete
        result = Http_methods.delete(url, body, headers_for_validate)
        assert result.status_code == 500
        print(json.dumps(result.json(), indent=2, ensure_ascii=False))

    @staticmethod
    def test_user_delete_product():
        res_delete_admin_delete = '/delete/admin/deleteproduct'
        token = Test_custom_api.login_user('test_user', 'test_user')
        headers_for_validate = {"Authorization": f"Bearer {token}"}
        body = {"username": 'test_user',
            "product_id": 2}
        url = base_url + res_delete_admin_delete
        result = Http_methods.delete(url, body, headers_for_validate)
        assert result.status_code == 400
        print(json.dumps(result.json(), indent=2, ensure_ascii=False))

    @staticmethod
    def test_disable_user_delete_product():
        res_delete_admin_delete = '/delete/admin/deleteproduct'
        token = Test_custom_api.login_user('disable_user', 'disable_user')
        headers_for_validate = {"Authorization": f"Bearer {token}"}
        body = {"username": 'disable_user',
            "product_id": 2}
        url = base_url + res_delete_admin_delete
        result = Http_methods.delete(url, body, headers_for_validate)
        assert result.status_code == 401
        print(json.dumps(result.json(), indent=2, ensure_ascii=False))

# Test_custom_api.test_create_new_user()      #Создание нового пользователя
# Test_custom_api.test_repeat_create_user()      #Создание пользователя который уже существует
# Test_custom_api.test_activate_new_user()        #тест некорректной ссылки активации
# Test_custom_api.test_success_login_user()           #тест успешной аутентификации
# Test_custom_api.test_fail_login_user()              #тест не успешной аутентификации
# Test_custom_api.test_show_products_auth()      #тест отображения товаров
# Test_custom_api.test_show_products_no_auth()     #тест отображения с неудачной аутентификацией
# Test_custom_api.test_deposit_money()            #тест зачисления средств
# Test_custom_api.test_deposit_one_money()            #тест зачисления средств
# Test_custom_api.test_fail_deposit_money()           #тест зачисления средств c неудачной аутентификацией
# Test_custom_api.test_buy_products()                 #тест покупки
# Test_custom_api.test_fail_buy_products()                 #тест покупки с нехваткой денег
# Test_custom_api.test_fail_login_buy_products()      #тест покупки c неудачной аутентификацией
# Test_custom_api.test_bill_history()         #Тест отображения счетов пользователя и входящих транзакций
# Test_custom_api.test_fail_bill_history()         #Тест отображения счетов пользователя c неудачной аутентификацией
# Test_custom_api.test_admin_show_users()           # Тест отображения пользователей для администратора
# Test_custom_api.test_user_show_users()              # Тест отображения пользователей для пользователя
# Test_custom_api.test_disable_user_show_users()          # Тест отображения пользователей для отключенного пользователя
# Test_custom_api.test_admin_disable_users()       # Тест включения и отключения пользователя
# Test_custom_api.test_admin_enable_users()       # т.к. это одна и та же процедура, вызываем дважды
# Test_custom_api.test_admin_create_product()                # Тест создания продукта для администратора
# Test_custom_api.test_user_create_product()                  # Тест создания продукта для пользователя
# Test_custom_api.test_disable_user_create_product()               # Тест создания продукта для отключенного пользователя
# Test_custom_api.test_admin_update_product()                 #Тест изменения продукта администратором
# Test_custom_api.test_user_update_product()                      #Тест изменения продукта пользователем
# Test_custom_api.test_disable_user_update_product()                 #Тест изменения продукта отключенным пользователем
# Test_custom_api.test_admin_delete_product()                     #тест удаления продукта
# Test_custom_api.test_admin_alredy_delete_product()                   #тест удаления несуществующего продукта
# Test_custom_api.test_user_delete_product()                      #тест удаления продукта пользователем
# Test_custom_api.test_disable_user_delete_product()               #тест удаления продукта отключенным пользователем