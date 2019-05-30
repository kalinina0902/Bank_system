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


if __name__ == '__main__':
 app.run(debug=True)