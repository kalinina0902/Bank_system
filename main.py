from flask import Flask, render_template, request, redirect, url_for
from model.client import *
from services.add_service import AddService
from services.find_service import FindService
from datetime import date

app = Flask(__name__)


@app.route('/')
def start():
  return render_template('main_page.html')


@app.route('/main_page', methods=['GET'])
def menu_action():
    if request.args['button'] == 'Регистрация':
        return render_template('registration.html', message="")
    elif request.args['button'] == 'Вход':
        return render_template('authorization.html', message="")


@app.route('/addClient', methods=['GET'])
def addClient():
    if request.args['button'] == 'Зарегистрироваться':
        name = request.args['first_name']
        surname = request.args['second_name']
        patronymic = request.args['patronymic']
        passport_id = int(request.args['passport_id'])
        passport_seria = int(request.args['passport_seria'])
        login = request.args['login']
        password = request.args['password']
        date_of_birth = request.args['date_of_birth']
        ans = AddService.registration_client(name,surname,patronymic,passport_id,passport_seria,date_of_birth,login,password)
        if ans == 1:
            return render_template('authorization.html', message="Регистрация прошла успешно")
        elif ans == 2:
            return render_template('registration.html', message="Данные паспорта не валидны")
    elif request.args['button'] == 'Регистрация':
        return render_template('registration.html')
    elif request.args['button'] == 'Вход':
        return render_template('authorization.html')


@app.route('/client',methods=['GET'])
def action_client():
    client_id = request.args['id_client']
    debet_account = FindService.Get_debet(client_id)
    deposit_account = FindService.Get_deposit(client_id)
    credit_account = FindService.Get_credit(client_id)
    offers_deposit = FindService.Get_deposit_offer()
    offers_credit = FindService.Get_credit_offer()
    if request.args['button'] == 'Открыть счёт':
        AddService.add_debet(client_id);
        debet_account = FindService.Get_debet(client_id)
        return render_template('client.html', message="Открыт дебетовый счёт", id_client=client_id, debet_accounts= debet_account, deposit_accounts=deposit_account,
                               credit_accounts=credit_account)
    elif request.args['button'] == 'Открыть вклад':
        return render_template('add_deposit.html', id_client=client_id, accounts=debet_account, offers=offers_deposit)
    elif request.args['button'] == 'Взять кредит':
        return render_template('add_credit.html',id_client=client_id, accounts=debet_account, offers=offers_credit)
    elif request.args['button'] == 'Перейти в дебет':
        id_debet = request.args['debet']
        sum = FindService.Get_sum(id_debet)
        return render_template('debet.html', id_client=client_id, ID_account=id_debet, sum=sum)
    elif request.args['button'] == 'Перейти во вклад':
        id_deposit = request.args['deposit']
        sum = FindService.Get_sum(id_deposit)
        percent = FindService.Get_persent(id_deposit)
        offer_name = FindService.Get_offer_name(id_deposit)
        return render_template('deposit.html', id_client=client_id, ID_account=id_deposit, sum=sum, offer_name=offer_name,
                               percent=percent)
    elif request.args['button'] == 'Перейти в кредит':
        id_credit = request.args['credit']
        sum = FindService.Get_sum(id_credit)
        percent = FindService.Get_persent(id_credit)
        offer_name = FindService.Get_offer_name(id_credit)
        return render_template('credit.html', id_client=client_id, ID_account=id_credit, sum=sum, offer_name=offer_name,
                               percent=percent)
    elif request.args['button'] == 'Личная информация':
        client = FindService.Get_client(client_id)
        return render_template('information.html', id_client=client_id, surname=client[0], name=client[1], patronymic=client[2],
                               passport_num=client[3], passport_ser=client[4], date_of_birth=client[5])
    elif request.args['button'] == 'Выход':
        return render_template('main_page.html')

@app.route('/add_deposit', methods=['GET'])
def add_deposite():

    client_id = request.args['id_client']
    debet_account = FindService.Get_debet(client_id)
    credit_account = FindService.Get_credit(client_id)
    offer_id = request.args['chooseoffer']
    debet_id = request.args['accountfrom']
    sum = float(request.args['sum'])
    if request.args['button'] == 'Открыть':
        s = AddService.add_deposit(id_client=client_id, id_offer=offer_id, id_debet=debet_id, sum=sum)
        deposit_account = FindService.Get_deposit(client_id)
        if s == 1:
           return render_template('client.html',message="Вклад открыт", id_client=client_id, debet_accounts=debet_account,
                                  deposit_accounts=deposit_account, credit_accounts=credit_account)
        if s == 2:
            return render_template('client.html',message="Недостаточно средств на дебетовом счёте", id_client=client_id,
                                   debet_accounts=debet_account,deposit_accounts=deposit_account, credit_accounts=credit_account)
    elif request.args['button'] == 'Выход':
        return render_template('main_page.html')


@app.route('/add_credit', methods=['GET'])
def add_credit():
    client_id = request.args['id_client']
    debet_account = FindService.Get_debet(client_id)
    deposit_account = FindService.Get_deposit(client_id)
    offer_id = request.args['chooseoffer']
    debet_id = request.args['accountto']
    sum = float(request.args['sum'])
    if request.args['button'] == 'Взять кредит':
        AddService.add_credit(id_client=client_id, id_offer=offer_id, id_debet=debet_id, sum=sum)
        credit_account = FindService.Get_credit(client_id)
        return render_template('client.html', message="Кредит открыт", id_client=client_id, debet_accounts=debet_account,
                                   deposit_accounts=deposit_account, credit_accounts=credit_account)
    elif request.args['button'] == 'Выход':
        return render_template('main_page.html')

@app.route('/authorization',methods=['GET'])
def authorization():
    if request.args['button'] == 'Войти':
        login = request.args['login']
        password = request.args['password']
        client_id = FindService.Log_in(login,password)
        if(client_id):
            debet_account = FindService.Get_debet(client_id)
            deposite_account = FindService.Get_deposit(client_id)
            credit_account = FindService.Get_credit(client_id)
            return render_template('client.html', id_client=client_id, debet_accounts=debet_account,
                                   deposite_accounts=deposite_account, credit_accounts=credit_account)
    elif request.args['button'] == 'Регистрация':
        return render_template('registration.html')
    elif request.args['button'] == 'Вход':
        return render_template('authorization.html')

@app.route("/information",methods=['GET'])
def information():
    client_id = request.args['id_client']
    if request.args["button"] == 'Посмотреть транзакции':
        transaction = FindService.Get_all_transaction(client_id)
        return render_template("my_transaction.html",id_client=client_id, table=transaction)
    elif request.args['button'] == 'Личный кабинет':
        debet_account = FindService.Get_debet(client_id)
        deposite_account = FindService.Get_deposit(client_id)
        credit_account = FindService.Get_credit(client_id)
        return render_template('client.html', id_client=client_id, debet_accounts=debet_account,
                               deposite_accounts=deposite_account, credit_accounts=credit_account)
    elif request.args['button'] == 'Выход':
        return render_template('main_page.html')


@app.route("/my_transaction", methods=['GET'])
def transaction():
    client_id = request.args['id_client']
    if request.args['button'] == 'Личный кабинет':
        debet_account = FindService.Get_debet(client_id)
        deposite_account = FindService.Get_deposit(client_id)
        credit_account = FindService.Get_credit(client_id)
        return render_template('client.html', id_client=client_id, debet_accounts=debet_account,
                               deposite_accounts=deposite_account, credit_accounts=credit_account)
    elif request.args['button'] == 'Выход':
        return render_template('main_page.html')


if __name__ == '__main__':
 app.run(debug=True)