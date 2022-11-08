import peewee
from models import *
import hashlib


class Control_database():
    '''класс управления бд через ОРМ'''

    @staticmethod
    def create_tables():
        Users.create_table()
        Bills.create_table()
        Transactions.create_table()
        Products.create_table()

    @staticmethod
    def create_user(user_name, user_pass):
        with pg_db.atomic() as transaction:
            try:
                user = Users()
                user.user_name = user_name
                user.user_pass = user_pass
                user.user_role = 'user'
                user.user_hash = hashlib.md5(bytes(user_name, 'utf-8')).hexdigest()
                user.user_enable = False
                user.save()
                return {"status_code": 200, "result": user.user_hash}
            except peewee.IntegrityError as e:
                transaction.rollback()
                if e.args[0].find('ограничение уникальности') != -1:
                    return {"status_code": 501, "result": "Такой пользователь уже существует"}
                else:
                    return {"status_code": 502, "result": f"Произошла ошибка добавления:\n{e.args}"}

    @staticmethod
    def activate_user(user_hash):
        with pg_db.atomic() as transaction:
            try:
                user = Users().get(Users.user_hash == user_hash)
                user.user_enable = True
                user.save()
                return {"status_code": 200, "result": f"Пользователь активирован!"}
            except peewee.IntegrityError as e:
                transaction.rollback()
                error_saving = True
                return {"status_code": 502, "result": f"Ошибка записи:\n{e.args}"}

    @staticmethod
    def check_user_password(username, password):
        user = Users().get(Users.user_name == username)
        if user.user_pass == password:
            return {"id": user.user_id, "user_name": user.user_name, "user_pas": user.user_pass}
        else:
            return 'fail'

    @staticmethod
    def get_all_products():
        products = Products.select()
        all_products_json = {}
        for product in products:
            all_products_json.update({product.product_id: {"Product_header": product.product_header,
                                                           "Product_description": product.product_description,
                                                           "Product_price": product.product_price}})
        return all_products_json

    @staticmethod
    def check_user_id(user_id):
        try:
            if Users.get(Users.user_id == user_id):
                return True
            else:
                return False
        except:
            return False

    @staticmethod
    def add_new_bill(user_id, bill_id):
        with pg_db.atomic() as transaction:
            try:
                if Control_database.check_user_id(user_id):
                    bill = Bills()
                    bill.bill_id = bill_id
                    bill.user_id = user_id
                    bill.bill_balance = 0
                    bill.save()
                    return {"status_code": 200, "result": "Счет создан!"}
                else:
                    return {"status_code": 502, "result": "Пользователь отсутствует."}
            except peewee.IntegrityError as e:
                transaction.rollback()
                error_saving = True
                return {"status_code": 501, "result": "Ошибка записи."}

    @staticmethod
    def get_user_id(username):
        user = Users.get(Users.user_name == username)
        return user.user_id

    @staticmethod
    def check_bill_id(bill_id):
        try:
            bills = Bills.get(Bills.bill_id == bill_id)
            exists = True
        except:
            exists = False
        return exists

    @staticmethod
    def check_product_id(product_id):
        try:
            product = Products.get(Products.product_id == product_id)
            exists = True
        except:
            exists = False
        return exists

    @staticmethod
    def deposit_money(bill_id, amount, signature, transaction_id):
        with pg_db.atomic() as transaction:
            try:
                trans = Transactions()
                trans.bill_id = bill_id
                trans.incoming_transaction = transaction_id
                trans.amount = amount
                trans.signature = signature
                bill = Bills.get(Bills.bill_id == bill_id)
                bill.bill_balance += amount
                bill.save()
                trans.save()
                return {"status_code": 200,
                        "result": f"Деньги зачислены. баланс:{bill.bill_balance}. Транзакция сохранена"}
            except peewee.IntegrityError as e:
                transaction.rollback()
                return {"status_code": 501, "result": f"Ошибка записи:\n{e.args}"}

    @staticmethod
    def pay_for_a_purchase(bill_id, product_id):
        with pg_db.atomic() as transaction:
            try:
                bill = Bills.get(Bills.bill_id == bill_id)
                product = Products.get(Products.product_id == product_id)
                if bill.bill_balance >= product.product_price:
                    bill.bill_balance -= product.product_price
                    print('1')
                    bill.save()
                    print('2')
                    return {"status_code": 200,
                            "result": f"Покупка завершена. баланс:{bill.bill_balance}. Транзакция сохранена"}
                else:
                    return {"status_code": 400,
                            "result": f"Покупка невозможна, недостаточно средств. баланс:{bill.bill_balance}."}
            except peewee.IntegrityError as e:
                transaction.rollback()
                return {"status_code": 501, "result": f"Ошибка записи:\n{e.args}"}

    @staticmethod
    def get_bill_history(username):
        history = {}
        user_id = Users.get(Users.user_name == username).user_id
        for bill in Bills.select().where(Bills.user_id == user_id):
            trans = Transactions.select().where(Transactions.bill_id == bill.bill_id)
            hist_bill = {}
            for trn in trans:
                hist_bill.update({
                    trn.transaction_id: {
                        "incoming_transaction": trn.incoming_transaction,
                        "bill_id": trn.Bill_ID,
                        "amount": trn.amount,
                        "signature": trn.signature,
                    }})
            history.update({bill.bill_id: {"balance": bill.bill_balance, "history": hist_bill}})
        return {"status_code": 200,
                "result": history}

    @staticmethod
    def check_is_admin(username):
        user = Users.get(Users.user_name == username)
        if user.user_role == 'admin':
            return True
        else:
            return False

    @staticmethod
    def check_is_enable(username):
        user = Users.get(Users.user_name == username)
        if user.user_enable == True:
            return True
        else:
            return False

    @staticmethod
    def get_users():
        users = Users.select()
        users_bills = {}
        for user in users:
            bills = Bills.select().where(Bills.user_id == user.user_id)
            user_bill = {}
            for bill in bills:
                user_bill.update({bill.bill_id: {"balanse": bill.bill_balance}})
            if user_bill == {}:
                user_bill = 'Нет ни одного счета'
            users_bills.update({user.user_id: {"Name": user.user_name, "Role": user.user_role, "Bills": user_bill}})
        return {"status_code": 200, "result": users_bills}

    @staticmethod
    def enable_disable_user(username):
        user = Users.get(Users.user_name == username)
        with pg_db.atomic() as transaction:
            try:
                if user.user_enable == True:
                    user.user_enable = False
                    user.save()
                    result = {"status_code": 200, "result": "Пользователь деактивирован!"}
                else:
                    user.user_enable = True
                    user.save()
                    result = {"status_code": 200, "result": "Пользователь активирован!"}
                return result
            except peewee.IntegrityError as e:
                transaction.rollback()
                return {"status_code": 501, "result": f"Ошибка записи:\n{e.args}"}

    @staticmethod
    def create_product(header, description, price):
        with pg_db.atomic() as transaction:
            try:
                product = Products()
                product.product_header = header
                product.product_description = description
                product.product_price = price
                product.save()
                return {"status_code": 200, "result": f"Товар {product.product_header} создан!"}
            except peewee.IntegrityError as e:
                transaction.rollback()
                return {"status_code": 501, "result": f"Ошибка записи:\n{e.args}"}

    @staticmethod
    def update_product(id, header=None, description=None, price=None):
        with pg_db.atomic() as transaction:
            try:
                product = Products.get(Products.product_id == id)
                if header:
                    product.product_header = header
                if description:
                    product.product_description = description
                if price:
                    product.product_price = price
                product.save()
                return {"status_code": 200, "result": f"Товар {product.product_header} Изменён!"}
            except peewee.IntegrityError as e:
                transaction.rollback()
                return {"status_code": 501, "result": f"Ошибка записи:\n{e.args}"}

    @staticmethod
    def delete_product(id):
        with pg_db.atomic() as transaction:
            try:
                try:
                    product = Products.get(Products.product_id == id)
                except:
                    product = None
                if product != None:
                    name = product.product_header
                    product.delete_instance()
                    return {"status_code": 200, "result": f"Товар {name} Удалён!"}
                else:
                    return {"status_code": 500, "result": f"Такого товара не существует!"}
            except peewee.IntegrityError as e:
                transaction.rollback()
                return {"status_code": 501, "result": f"Ошибка записи:\n{e.args}"}
