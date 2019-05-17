from peewee import *
from Bank_system.model.base_model import BaseModel


class Account(BaseModel):
    type = IntegerField()
    number = IntegerField(null=False, primary_key=True)
    date_open = DateField()
    date_close = DateField()
    percent = DoubleField(null= False)
    count_money_now = DoubleField(null=False)