from model.client import Client
from model.account import Account
from model.offer import Offer

class FindService:

    @staticmethod
    def Log_in(login,password):

        my_client = Client.select().where((Client.login == login) & (Client.password == password)).get()
        if(my_client):
            return my_client.ID_client
        else:
            return 0

    @staticmethod
    def Get_debet(ID_client):

        id_debet =[]
        debet_account = Account.select().where(Account.ID_client == ID_client, Account.ID_offer == 1)
        for it in debet_account:
            id_debet.append(it.ID_account)
        return id_debet

    @staticmethod
    def Get_deposit_offer():
        return Offer.select().where(Offer.type == 'deposit')

    @staticmethod
    def Get_credit_offer():
        return Offer.select().where(Offer.type == 'credit')

    @staticmethod
    def Get_deposit(ID_client):

        id_deposit =[]
        account = Account.select().where((Account.ID_client == ID_client))
        for it in account:
           if Offer.get(Offer.ID_offer == it.ID_offer).type == ('deposit'):
                id_deposit.append(it.ID_account)
        return id_deposit

    @staticmethod
    def Get_credit(ID_client):

        id_credit = []
        account = Account.select().where((Account.ID_client == ID_client))
        for it in account:
            if Offer.get(Offer.ID_offer == it.ID_offer).type == ('credit'):
                id_credit.append(it.ID_account)
        return id_credit
