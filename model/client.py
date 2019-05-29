from peewee import *
from Bank_system.model.base_model import BaseModel


class Client(BaseModel):

    id = IntegerField(null=False, primary_key=True)
    name = CharField(max_length=100)
    surname = CharField(max_length=100)
    patronymic = CharField(max_length=100)
    passport_id = IntegerField(null=False)
    passport_number = IntegerField(null=False)
    date_of_birth = DateField(null=False)
    login = CharField(max_length=30, unique=True)
    password = CharField(max_length=100)