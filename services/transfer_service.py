from model.account import Account
from model.transaction import Transaction


class TransferService:
    @staticmethod
    def transferfrom(sum, id_account_from):
        if (sum < Account.get(Account.ID_account == id_account_from).sum):
            acc = Account.get(Account.ID_account == id_account_from)
            acc.sum -= sum
            acc.save()
            return 1
        else:
            return 2

    @staticmethod
    def payment(sum, acc_from, acc_to):
        if (sum < Account.get(Account.ID_account == acc_from).sum):
            acc = Account.get(Account.ID_account == acc_from)
            acc.sum -= sum
            acc.save()
            acc2 = Account.get(Account.ID_account == acc_to)
            acc2.sum += sum
            acc2.save()
            return 1
        else:
            return 2


    @staticmethod
    def transferto(sum, id_account_to):
        acc = Account.get(Account.ID_account == id_account_to)
        acc.sum += sum
        acc.save()
