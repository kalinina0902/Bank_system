from flask import Flask, render_template, request, redirect, url_for
from model.client import *
from services.add_service import AddService
from services.find_service import AuthorizationService

from datetime import date

app = Flask(__name__)


@app.route('/')
def start():
  return render_template('index.html')

@app.route('/main')
def exit():
    return render_template('index.html')


@app.route('/registration' )
def registration():
 return render_template('registration.html')

@app.route('/registration' , methods=['POST'])
def registration_people():
    name = request.args['first_name']
    surname = request.args['second_name']
    patronymic = request.args['patronymics']
    passport_id = request.args['number_passport']
    passport_seria = request.args['seria_passport']
    date_of_birth = request.args['date_of_birth']
    login = request.args['login']
    password = request.args['password']
    s = AddService.registration_client(name,surname,patronymic,passport_id,passport_seria,date_of_birth,login,password)
    return render_template('authorization.html')


@app.route('/authorization', methods=['GET'])
def authorization():
   return render_template('authorization.html')


@app.route('/authorization', methods=['POST'])
def authorization_people():
    login = request.args['login']
    password = request.args['password']
    client_id = AuthorizationService(login,password)
    if(client_id):
        return render_template('client.html',client_id)

if __name__ == '__main__':
 app.run(debug=True)