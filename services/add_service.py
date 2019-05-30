from model.account import Account
from model.client import Client

from datetime import *

class AddService:

    @staticmethod
    def registration_client(name, surname, patronymic, passport_id, passport_seria, date_of_birth, login, password):
        s = "Ошибка: "
        if (Client.select().where(Client.passport_id==passport_id, Client.passport_seria==passport_seria).get()):

            s += "Серия и номер паспорта не валидны"

        elif (Client.select().where(Client.login == login, Client.password == password).get()):

            s += "Такой логин существует"

        else:

            my_client = Client(name,surname,patronymic, passport_id,passport_seria, date_of_birth)
            my_client.save()
            s = "Успешная регистрация"

        return s

    def add_debet(self, id_client):

        Account.create(type=1,date_open=datetime.today(),percent=0,count_money_now=0,id_client=id_client, num_card= CardService.add_card())


    def add_credit(self,id_client,Offer,num_deb,sum):
        Account.create(type=2, date_open=datetime.today(), percent=Offer.percent, count_money_now=sum, id_client=id_client)
        Account.update(count_money_now=Account.count_money_now-sum).where(Account.number == num_deb)


    def add_deposite(self,id_client,offer,num_deb,sum):
        Account.create(type=3, date_open=datetime.today(), percent=offer.percent, count_money_now=sum, id_client=id_client)
        Account.update(count_money_now=Account.count_money_now-sum).where(Account.number == num_deb)