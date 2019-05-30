from peewee import *
from model.base_model import BaseModel
from model.client import Client
from model.offer import Offer


class Account(BaseModel):
    ID_account = IntegerField(primary_key=True, unique=True)
    sum = DoubleField(null=False)
    ID_client = ForeignKeyField(Client, backref="account")
    ID_offer = ForeignKeyField(Offer, on_delete=None)
    date_open = DateField()
    date_close = DateField(null=True)