from peewee import *
from model.base_model import BaseModel
from model.client import Client
from model.account import Account

class Transaction(BaseModel):
    ID_transaction = IntegerField(primary_key=True)
    sum = DoubleField (null=False)
    ID_client= ForeignKeyField(Client, backref="transaction")
    ID_account_from = ForeignKeyField(Account, backref="account_from")
    ID_account_to = IntegerField(null=False)
    date = DateField(null= False)

