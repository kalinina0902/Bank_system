from flask import Flask, render_template, request, redirect, url_for
from model.client import *
from services.add_service import AddService
from services.find_service import FindService
from services.transfer_service import TransferService
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
    name = request.args['first_name']
    surname = request.args['second_name']
    patronymic = request.args['patronymic']
    passport_id = int(request.args['passport_id'])
    passport_seria = int(request.args['passport_seria'])
    login = request.args['login']
    password = request.args['password']
    date_of_birth = request.args['date_of_birth']
    if ((request.args['button'] == 'Зарегистрироваться')&(name!='')&(surname!='')&(patronymic!='')&(request.args['passport_id']!='')&
            (request.args['passport_seria']!='')&(login!='')&(passport_id!='')):
        ans = AddService.registration_client(name,surname,patronymic,passport_id,passport_seria,date_of_birth,login,password)
        if ans == 1:
            return render_template('authorization.html', message="Регистрация прошла успешно")
        elif ans == 2:
            return render_template('registration.html', message="Данные паспорта не валидны")
    elif request.args['button'] == 'Регистрация':
        return render_template('registration.html',message="")
    elif request.args['button'] == 'Вход':
        return render_template('authorization.html',message="")
    else:
        return render_template('registration.html', message="Не все поля заполнены!")


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
        sum_deb = FindService.Get_sum(id_debet)
        return render_template('debet.html', id_client=client_id, ID_account=id_debet, sum=sum_deb)
    elif request.args['button'] == 'Перейти во вклад':
        id_deposit = request.args['deposit']
        sum_dep = FindService.Get_sum(id_deposit)
        percent_dep = FindService.Get_percent(id_deposit)
        offer_name = FindService.Get_offer_name(id_deposit)
        return render_template('deposit.html', id_client=client_id, ID_account=id_deposit, sum=sum_dep, offer_name=offer_name,
                               percent=percent_dep)
    elif request.args['button'] == 'Перейти в кредит':
        id_credit = request.args['credit']
        sum_cr = FindService.Get_sum(id_credit)
        percent_cr = FindService.Get_percent(id_credit)
        offer_name = FindService.Get_offer_name(id_credit)
        return render_template('credit.html', id_client=client_id, ID_account=id_credit, sum=sum_cr, offer_name=offer_name,
                               percent=percent_cr)
    elif request.args['button'] == 'Личная информация':
        client = FindService.Get_client(client_id)
        return render_template('information.html', id_client=client_id, surname=client[0], name=client[1], patronymic=client[2],
                               passport_num=client[3], passport_ser=client[4], date_of_birth=client[5])
    elif request.args['button'] == 'Выход':
        return render_template('main_page.html')


@app.route('/debet', methods=['GET'])
def action_debet():
    client_id = request.args['id_client']
    account_id = request.args['id_account']
    if request.args['button'] == 'Перевод':
        return render_template('transfer.html', ID_account=account_id, id_client=client_id, message="")
    elif request.args['button'] == 'Выход':
        return render_template('main_page.html')


@app.route('/transfer', methods=['GET'])
def transfer():
    client_id = request.args['id_client']
    account_id = request.args['id_account']
    sum = float(request.args['sum'])
    accountto = request.args['accountto']
    if request.args['button'] == 'Осуществить перевод':
        ans = TransferService.transferfrom(sum=sum,id_account_from=account_id)
        if ans == 1:
            debet_account = FindService.Get_debet(client_id)
            deposit_account = FindService.Get_deposit(client_id)
            credit_account = FindService.Get_credit(client_id)
            AddService.add_transaction(sum=sum, id_client=client_id, id_account_to=accountto, id_account_from=account_id)
            return render_template('client.html', message="Перевод осуществлён", id_client=client_id,
                                   debet_accounts=debet_account, deposit_accounts=deposit_account,
                                    credit_accounts=credit_account)
        if ans == 2:
            return render_template('transfer.html',message="На счету недостаточно средств для перевода",ID_account=account_id, id_client=client_id)
    elif request.args['button'] == 'Выход':
        return render_template('main_page.html')


@app.route('/credit', methods=['GET'])
def action_credit():
    client_id = request.args['id_client']
    account_id = request.args['id_account']
    sumAll = float(request.args['sum'])
    date_close = FindService.Get_date_close_credit(account_id)
    date_today = date.today()
    years = date_close.year - date_today.year
    month = date_close.month - date_today.month
    rem_period = years*12 + month
    payment=sumAll/rem_period
    pp = round(payment, 3) * (-1)
    debet_account = FindService.Get_debet(client_id)
    if request.args['button'] == 'Ежемесячный платёж':
        return render_template('every_month_payment.html', ID_account=account_id, id_client=client_id,
                               debet_accounts=debet_account, payment=pp,message="")
    elif request.args['button'] == 'Выход':
        return render_template('main_page.html')


@app.route('/every_month_payment', methods=['GET'])
def every_month_payment():
    client_id = request.args['id_client']
    account_id = request.args['id_account']
    sum = float(request.args['payment'])
    accountfrom = request.args['accountfrom']
    if ((request.args['button'] == 'Списать')&(request.args['accountfrom']!='null')):
        ans = TransferService.payment(sum=sum, acc_from=accountfrom, acc_to=account_id)
        if ans == 1:
            debet_account = FindService.Get_debet(client_id)
            deposit_account = FindService.Get_deposit(client_id)
            credit_account = FindService.Get_credit(client_id)
            AddService.add_transaction(sum=sum, id_client=client_id, id_account_to=account_id, id_account_from=accountfrom)
            return render_template('client.html', message="Платёж осуществлён", id_client=client_id,
                                   debet_accounts=debet_account, deposit_accounts=deposit_account,
                                    credit_accounts=credit_account)
        if ans == 2:
            return render_template('every_month_payment.html',message="На счету недостаточно средств для платежа",ID_account=account_id, id_client=client_id)
    elif request.args['button'] == 'Выход':
        return render_template('main_page.html')
    else:
        return render_template('every_month_payment.html',message="Не выбран счёт!")


@app.route('/deposit', methods=['GET'])
def action_deposit():
    client_id = request.args['id_client']
    account_id = request.args['id_account']
    sumAll = float(request.args['sum'])
    debet_account = FindService.Get_debet(client_id)
    if request.args['button'] == 'Пополнить баланс':
        return render_template('replenish.html', ID_account=account_id, id_client=client_id,
                               debet_accounts=debet_account, message="")
    elif request.args['button'] == 'Закрыть вклад':
        return render_template('close_deposite.html', ID_account=account_id, id_client=client_id, sum=sumAll,
                               debet_accounts=debet_account, message="")
    elif request.args['button'] == 'Выход':
        return render_template('main_page.html')


@app.route('/replenish', methods=['GET'])
def replenish():
    client_id = request.args['id_client']
    account_id = request.args['id_account']
    sum = float(request.args['sum'])
    accountfrom = request.args['accountfrom']
    if ((request.args['button'] == 'Пополнить')&(request.args['accountfrom']!='null')):
        ans = TransferService.payment(sum=sum, acc_from=accountfrom, acc_to=account_id)
        if ans == 1:
            debet_account = FindService.Get_debet(client_id)
            deposit_account = FindService.Get_deposit(client_id)
            credit_account = FindService.Get_credit(client_id)
            AddService.add_transaction(sum=sum, id_client=client_id, id_account_to=account_id, id_account_from=accountfrom)
            return render_template('client.html', message="Пополнение осуществлено", id_client=client_id,
                                   debet_accounts=debet_account, deposit_accounts=deposit_account,
                                    credit_accounts=credit_account)
        if ans == 2:
            return render_template('replenish.html',message="На счету недостаточно средств для пополнения",ID_account=account_id, id_client=client_id)
    elif request.args['button'] == 'Выход':
        return render_template('main_page.html')
    else:
        return render_template('replenish.html',message="Не выбран счёт!")


@app.route('/close_deposit', methods=['GET'])
def close_deposit():
    client_id = request.args['id_client']
    account_id = request.args['id_account']
    sum = float(request.args['sum'])
    accountto = request.args['accountto']
    if ((request.args['button'] == 'Закрыть вклад')&(request.args['accountto']!='null')):
        ans = TransferService.transferto(sum=sum, id_account_to=accountto)
        debet_account = FindService.Get_debet(client_id)
        credit_account = FindService.Get_credit(client_id)
        AddService.add_transaction(sum=sum, id_client=client_id, id_account_to=accountto,
                                   id_account_from=account_id)
        AddService.delete_deposit(account_id)
        deposit_account = FindService.Get_deposit(client_id)
        return render_template('client.html', message="Вклад закрыт", id_client=client_id,
                               debet_accounts=debet_account, deposit_accounts=deposit_account,
                               credit_accounts=credit_account)
    elif request.args['button'] == 'Выход':
        return render_template('main_page.html')
    else:
        return render_template('close_deposite.html',message="Не выбран счёт!")


@app.route('/add_deposit', methods=['GET'])
def add_deposite():
    client_id = request.args['id_client']
    debet_account = FindService.Get_debet(client_id)
    credit_account = FindService.Get_credit(client_id)
    offer_id = request.args['chooseoffer']
    debet_id = request.args['accountfrom']
    sum = float(request.args['sum'])
    if ((request.args['button'] == 'Открыть')&(request.args['accountfrom']!='null')&(request.args['choseoffer']!='null')&(request.args['sum']!='')):
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
    else:
        return render_template('add_deposite.html',message="Не все поля заполнены(выбраны)!")


@app.route('/add_credit', methods=['GET'])
def add_credit():
    client_id = request.args['id_client']
    debet_account = FindService.Get_debet(client_id)
    deposit_account = FindService.Get_deposit(client_id)
    offer_id = request.args['chooseoffer']
    debet_id = request.args['accountto']
    sum = float(request.args['sum'])
    if ((request.args['button'] == 'Взять кредит')&(request.args['accountfrom']!='null')&(request.args['choseoffer']!='null')&(request.args['sum']!='')):
        AddService.add_credit(id_client=client_id, id_offer=offer_id, id_debet=debet_id, sum=sum)
        credit_account = FindService.Get_credit(client_id)
        return render_template('client.html', message="Кредит открыт", id_client=client_id, debet_accounts=debet_account,
                                   deposit_accounts=deposit_account, credit_accounts=credit_account)
    elif request.args['button'] == 'Выход':
        return render_template('main_page.html')
    else:
        return render_template('add_credit.html',message="Не все поля заполнены(выбраны)!")


@app.route('/authorization',methods=['GET'])
def authorization():
    if ((request.args['button'] == 'Войти')&(request.args['login']!='')&(request.args['password']!='')):
        login = request.args['login']
        password = request.args['password']
        auth = []
        auth = FindService.Log_in(login,password)
        if(auth[0]==1):
            debet_account = FindService.Get_debet(auth[1])
            deposit_account = FindService.Get_deposit(auth[1])
            credit_account = FindService.Get_credit(auth[1])
            return render_template('client.html', id_client=auth[1], debet_accounts=debet_account,
                                   deposit_accounts=deposit_account, credit_accounts=credit_account,message="")
        elif auth[0] == 2:
            return render_template('operator.html',message="")
        else:
            return render_template('authrization.html', message="Неверные данные")
    elif request.args['button'] == 'Регистрация':
        return render_template('registration.html',message="")
    elif request.args['button'] == 'Вход':
        return render_template('authorization.html',message="")
    else:
        return render_template('authorization.html',message="Не все поля заполнены!")


@app.route("/operator", methods=['GET'])
def operator_action():
    if request.args["button"] == 'Добавить предложение':
        return render_template("add_offer.html")
    elif request.args['button'] == 'Редактировать предложение':
        offers = FindService.Get_offer()
        return render_template("edit_offer.html", offers=offers)
    elif request.args['button'] == 'Удалить предложение':
        offers = FindService.Get_offer()
        return render_template("delete_offer.html", offers=offers)
    elif request.args['button'] == 'Выход':
        return render_template('main_page.html')


@app.route("/add_offer", methods=['CET'])
def add_offer():
    period = int(request.args['period'])
    percent = float(request.args['percent'])
    name = request.args['nameoffer']
    type = request.args['type']
    if request.args["button"] == 'Добавить предложение':
        AddService.add_offer(name=name, period=period, percent=percent, type=type)
        return render_template("operator.html",message="Предложение добавлено")
    elif request.args['button'] == 'Выход':
        return render_template('main_page.html')


@app.route("/edit_offer", methods=['GET'])
def edit_offer():
    period = int(request.args['period'])
    percent = float(request.args['percent'])
    name = request.args['nameoffer']
    offer_id = request.args['chooseoffer']
    if request.args["button"] == 'Изменить информацию':
        AddService.change_offer(id_offer=offer_id, name=name, period=period, percent=percent)
        return render_template("operator.html",message="Предложение изменено")
    elif request.args['button'] == 'Выход':
        return render_template('main_page.html')


@app.route("/delete_offer", methods=['GET'])
def delete_offer():
    offer_id = request.args['chooseoffer']
    if request.args["button"] == 'Удалить':
        AddService.delete_offer(id_offer=offer_id)
        return render_template("operator.html",message="Предложение удалено")
    elif request.args['button'] == 'Выход':
        return render_template('main_page.html')


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
                               deposit_accounts=deposite_account, credit_accounts=credit_account)
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
                               deposit_accounts=deposite_account, credit_accounts=credit_account)
    elif request.args['button'] == 'Выход':
        return render_template('main_page.html')


if __name__ == '__main__':
 app.run(debug=True)