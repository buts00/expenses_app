from peewee import *

db = SqliteDatabase('database.db')


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db


class Expense(BaseModel):
    name = CharField()

    class Meta:
        db_table = 'expenses'
        order_by = 'id'


class Payment(BaseModel):
    amount = FloatField()
    payment_date = DateField()
    payment_id = ForeignKeyField(Expense)

    class Meta:
        db_table = 'payments'
