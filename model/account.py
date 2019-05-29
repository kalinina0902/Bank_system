from peewee import *
from Bank_system.model.base_model import BaseModel
from Bank_system.model.client import Client
from Bank_system.model.offer import Offer


class Account(BaseModel):


    ID_account = IntegerField(primary_key=True, unique=True)
    sum = DoubleField(null=False)
    ID_client = ForeignKeyField(Client, backref="account")
    ID_offer = ForeignKeyField(Offer, on_delete=None)
    date_open = DateField()
    date_close = DateField()
    percent = DoubleField(null= False)
    type = IntegerField(null= False)