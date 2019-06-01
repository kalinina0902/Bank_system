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
    def add_debet(id_client):
        Account.create(sum=0, ID_offer=Offer.get(Offer.ID_offer == 1), ID_client=id_client, date_open=date.today())

    @staticmethod
    def add_credit(id_client, id_offer, num_deb, sum):
        Account.create(sum=(sum * -1), ID_offer=id_offer, ID_client=id_client, date_open=date.today(),
                       date_close=date.today() + Offer.get(Offer.ID_offer == id_offer).period)
        Account.update(sum=Account.sum + sum).where(Account.number == num_deb)

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
        Account.create(sum=(sum * -1), ID_offer=id_offer, ID_client=id_client, date_open=dateall, date_close=date_close)
        acc = Account.get(Account.ID_account == id_debet)
        acc.sum += sum
        acc.save()