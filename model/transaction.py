from peewee import *
from Bank_system.model.base_model import BaseModel

class Transaction(BaseModel):


    id = IntegerField(primary_key=True)
    sum = DoubleField (null=False)
    account_from = IntegerField(null=False)
    account_to = IntegerField(null=False)
    date = DateField(null= False)

