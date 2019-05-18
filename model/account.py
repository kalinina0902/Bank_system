from peewee import *
from Bank_system.model.base_model import BaseModel
from Bank_system.model.client import Client
from Bank_system.model.card import Card


class Account(BaseModel):

    type = IntegerField()
    number = IntegerField(primary_key=True, unique=True)
    date_open = DateField()
    date_close = DateField()
    percent = DoubleField(null= False)
    count_money_now = DoubleField(null=False)
    id_client = ForeignKeyField(Client, backref="account")
    number_card = ForeignKeyField(Card,on_delete=None)