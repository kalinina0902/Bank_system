from model.client import Client
from model.account import Account
from model.offer import Offer
from model.transaction import Transaction
from model.operator import Operator

class FindService:

    @staticmethod
    def Log_in(login, password):

        try:
            my_client = Client.select().where((Client.login == login) & (Client.password == password)).get()
            return [1, my_client.ID_client]
        except:
            my_operator = Operator.select().where((Operator.login == login) & (Operator.password == password)).get()
            return [2, my_operator.ID_operator]
        else:
            return [0,0]


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

    @staticmethod
    def Get_sum(id_acc):
        return Account.get(Account.ID_account==id_acc)

    @staticmethod
    def Get_offer_name(id_acc):
        return Offer.get(Offer.ID_offer==(Account.get(Account.ID_account==id_acc)).ID_offer).name

    @staticmethod
    def Get_percent(id_acc):
        return Offer.get(Offer.ID_offer == (Account.get(Account.ID_account==id_acc)).ID_offer).percent

    @staticmethod
    def Get_client(id_client):
        result = []
        client = Client.get(Client.ID_client == id_client)
        result.append(client.surname)
        result.append(client.name)
        result.append(client.patronymic)
        result.append(client.passport_id)
        result.append(client.passport_seria)
        result.append(client.date_of_birth)
        return result

    @staticmethod
    def Get_all_transaction(id_client):
        return Transaction.select().where(Transaction.ID_client == id_client)