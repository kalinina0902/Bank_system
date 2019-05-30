from peewee import *
from model.base_model import BaseModel

class Offer(BaseModel):
    ID_offer = IntegerField(null=False, primary_key=True)
    percent = DoubleField(null=True)
    name = CharField(max_length=100)
    type = CharField(max_length=100)
    period = IntegerField(null=True)