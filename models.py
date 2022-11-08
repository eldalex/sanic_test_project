from peewee import *

pg_db = PostgresqlDatabase('test', user='postgres', password='QWErty123',
                           host='localhost', port=5432)


class BaseModel(Model):
    class Meta:
        database = pg_db


class Users(BaseModel):
    user_id = IntegerField(column_name='User_ID', null=False, unique=True, primary_key=True, sequence='user_id_seq')
    user_hash = CharField(column_name='User_hash', null=False, unique=True)
    user_name = CharField(column_name='User_name', null=False, unique=True)
    user_pass = CharField(column_name='User_pass', null=False)
    user_role = CharField(column_name='User_role', null=False)
    user_enable = BooleanField(column_name='User_enable', null=False)

    class Meta:
        table_name = 'Users'


class Products(BaseModel):
    product_id = IntegerField(column_name='Product_ID', null=False, unique=True, primary_key=True,
                              sequence='product_id_seq')
    product_header = CharField(column_name='Product_header', null=False)
    product_description = CharField(column_name='Product_description', null=False)
    product_price = IntegerField(column_name='Product_price', null=False)

    class Meta:
        table_name = 'Products'


class Bills(BaseModel):
    bill_id = IntegerField(column_name='Bill_ID', null=False, unique=True)
    user_id = ForeignKeyField(Users, related_name='User_Bills', column_name='User_ID', null=False)
    bill_balance = IntegerField(column_name='Bill_balance', null=False)

    class Meta:
        table_name = 'Bills'


class Transactions(BaseModel):
    transaction_id = IntegerField(column_name='Transaction_ID', null=False, unique=True, primary_key=True,
                                  sequence='transaction_id_seq')
    incoming_transaction = IntegerField(column_name='Incoming_transaction', null=False)
    bill_id = ForeignKeyField(Bills, to_field='bill_id', related_name='Bill_Transactions', column_name='Bill_ID',
                              null=False)
    amount = IntegerField(column_name='Amount', null=False)
    signature = CharField(column_name='Signature', null=False)

    class Meta:
        table_name = 'Transactions'


class Test(BaseModel):
    test = CharField()

    class Meta:
        table_name = 'test'
