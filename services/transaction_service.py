from model.account import Account
from model.transaction import Transaction

class Transactionservice:


    def transfer_money_another(self, id_from_ac, id_into_ac, sum):

        from_ac = Account.select().where(Account.number == id_from_ac).get()
        from_ac.count_money_now -= sum
        from_ac.save()
        Transaction.create(from_ac=from_ac.number, into_ac=id_into_ac, sum=sum)


    def transfer_money_account(self, id_from_ac, id_into_ac, sum):

        from_ac = Account.select().where(Account.number == id_from_ac).get()
        into_ac = Account.select().where(Account.number == id_into_ac).get()
        from_ac.count_money_now -= sum
        from_ac.save()
        if (into_ac.type == 2):
            into_ac.count_money_now -= (sum + into_ac.count_money_now*(into_ac.percent/100 +1))
            if(into_ac.count_money_now):
                into_ac.save()
            else:
                into_ac.delete()
        elif(into_ac.type == 3):
            into_ac.count_money_now += sum
            into_ac.save()
        Transaction.create(from_ac=from_ac.number, into_ac=into_ac.number, sum=sum)


    def close_deposite(self, id_from_ac,id_into_ac):

        from_ac = Account.select().where(Account.number == id_from_ac).get()
        into_ac = Account.select().where(Account.number == id_into_ac).get()
        from_ac.count_money_now += into_ac.count_money_now
        from_ac.save()
        into_ac.delete()

    def show_transaction(self):
        return Transaction.select()