from model.account import Account
from model.client import Client
from model.offer import Offer
from model.transaction import Transaction
from model.operator import Operator
from datetime import *
import random


class AddService:
    @staticmethod
    def registration_client(name, surname, patronymic, passport_id, passport_seria, date_of_birth,login, password):
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
    def add_debet(id_client):
        Account.create(sum=0, ID_offer=Offer.get(Offer.ID_offer == 1), ID_client=id_client, date_open=date.today())

    @staticmethod
    def add_deposit(id_client, id_offer, id_debet, sum):
        dateall = date.today()
        day = dateall.day
        month = dateall.month
        year = dateall.year
        period = (Offer.get(Offer.ID_offer == id_offer)).period
        year_period = period // 12
        if (day == 31):
            day -= 1
        if year_period > 0:
            year += year_period
            period -= year_period * 12
        if month + period > 12:
            k = 12 - month
            period -= k
            year += 1
        month += period
        if month == 2 & day == 30:
            day = 28
        date_close = datetime(year, month, day)
        if ((Account.get(Account.ID_account == id_debet)).sum > sum):
            Account.create(sum=sum, ID_offer=id_offer, ID_client=id_client, date_open=dateall, date_close=date_close)
            acc = Account.get(Account.ID_account == id_debet)
            acc.sum -= sum
            acc.save()
            s = 1
            return s
        else:
            s = 2
            return s

    @staticmethod
    def add_credit(id_client, id_offer, id_debet, sum):
        dateall = date.today()
        day = dateall.day
        month = dateall.month
        year = dateall.year
        period = (Offer.get(Offer.ID_offer == id_offer)).period
        percent = (Offer.get(Offer.ID_offer == id_offer)).percent
        year_period = period // 12
        if day == 31:
            day -= 1
        if year_period > 0:
            year += year_period
            period -= year_period * 12
        if month + period > 12:
            k = 12 - month
            period -= k
            year += 1
        month += period
        if month == 2 & day == 30:
            day = 28
        date_close = datetime(year, month, day)
        summonth = ((sum*percent)/(100*12))/(1-(1/((1 + (percent/(100*12)))**(12*year_period))))
        sumcred = summonth * period
        Account.create(sum=(sumcred * -1), ID_offer=id_offer, ID_client=id_client, date_open=dateall, date_close=date_close)
        acc = Account.get(Account.ID_account == id_debet)
        acc.sum += sum
        acc.save()

    @staticmethod
    def add_transaction(sum, id_client, id_account_to, id_account_from):
        Transaction.create(sum=sum, ID_client=Client.get(Client.ID_client == id_client), ID_account_from=id_account_from,
                           ID_account_to=id_account_to, date=date.today())

    @staticmethod
    def delete_deposit(id_account):
        Account.get(Account.ID_account == id_account).delete_instance()

    @staticmethod
    def delete_offer(id_offer):
        Offer.get(Offer.ID_offer == id_offer).delete_instance()

    @staticmethod
    def add_offer(name, percent, type, period):
        if type == "1":
            Offer.create(name=name, type='credit', period=period, percent=percent)
        elif type == "2":
            Offer.create(name=name, type='deposit', period=period, percent=percent)

    @staticmethod
    def change_offer(id_offer, name, period, percent):
        offer = Offer.get(Offer.ID_offer == id_offer)
        offer.name = name
        offer.percent = percent
        offer.period = period
        offer.save()
