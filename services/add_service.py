from model.account import Account
from model.client import Client
from model.offer import Offer
from datetime import *
import random


class AddService:
    @staticmethod
    def registration_client (name, surname, patronymic, passport_id, passport_seria, date_of_birth,login, password):
        dateall = date_of_birth.split('-')
        day = int(dateall[2])
        month = int(dateall[1])
        year = int(dateall[0])
        if ((passport_id > 1970) & (passport_id < 2030) & (passport_seria > 100000) & (passport_seria < 999999)):
            Client.create(name=name,surname=surname,patronymic=patronymic, passport_id=passport_id,
                          passport_seria=passport_seria, date_of_birth=date(year,month,day), login=login, password=password)
            sumR = random.randint(500, 5000)
            Account.create(sum=sumR, ID_offer=Offer.get(Offer.ID_offer == 1), ID_client=Client.get((Client.passport_seria
                             == passport_seria) & (Client.passport_id == passport_id)), date_open=date.today())
            s = 1
            return s
        else:
            s = 2
            return s

    @staticmethod
    def add_debet(self, id_client):
        Account.create(type=1,date_open=datetime.today(),percent=0,count_money_now=0,id_client=id_client)

    @staticmethod
    def add_credit(self,id_client,Offer,num_deb,sum):
        Account.create(type=2, date_open=datetime.today(), percent=Offer.percent, count_money_now=sum, id_client=id_client)
        Account.update(count_money_now=Account.count_money_now-sum).where(Account.number == num_deb)

    @staticmethod
    def add_deposite(self,id_client,offer,num_deb,sum):
        Account.create(type=3, date_open=datetime.today(), percent=offer.percent, count_money_now=sum, id_client=id_client)
        Account.update(count_money_now=Account.count_money_now-sum).where(Account.number == num_deb)