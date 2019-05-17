from peewee import *
from Bank_system.model.base_model import BaseModel

class Card(BaseModel):
   number = IntegerField(null=False, primary_key=True)
