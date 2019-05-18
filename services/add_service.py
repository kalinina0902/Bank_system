from Bank_system.model.account import Account
from Bank_system.model.card import Card
from Bank_system.services.card_service import CardService
from datetime import *

class AddService:


    def add_debet(self, id_client):

        Account.create(type=1,date_open=datetime.today(),percent=0,count_money_now=0,id_client=id_client, num_card= CardService.add_card())


    def add_credit(self,id_client,Offer,num_deb,sum):
        Account.create(type=2, date_open=datetime.today(), percent=Offer.percent, count_money_now=sum, id_client=id_client)
        Account.update(count_money_now=Account.count_money_now-sum).where(Account.number == num_deb)


    def add_deposite(self,id_client,offer,num_deb,sum):
        Account.create(type=3, date_open=datetime.today(), percent=offer.percent, count_money_now=sum, id_client=id_client)
        Account.update(count_money_now=Account.count_money_now-sum).where(Account.number == num_deb)