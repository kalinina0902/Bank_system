from peewee import *
from model.base_model import BaseModel

class Operator(BaseModel):

   ID_operator = IntegerField(primary_key=True, unique=True)
   login = CharField(max_length=30, unique=True)
   password = CharField(max_length=20)
   name = CharField(max_length=100)