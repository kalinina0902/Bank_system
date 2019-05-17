from peewee import *
from Bank_system.model.base_model import BaseModel

class Offer(BaseModel):
    id = IntegerField(null=False, primary_key=True)
    percent = DoubleField(null=False)
    description = CharField(max_length=100)
    type = CharField(max_length=100)
