from Bank_system.model.client import Client

class RegistrationService:


    def registration_client (name, surname, patronymic, passport_id, passport_number, date_of_birth,login, password):
        s = "Ошибка: "
        if (Client.select().where(Client.passport_id==passport_id, Client.passport_number==passport_number).get()):

            s += "Серия и номер паспорта не валидны"

        elif (Client.select().where(Client.login == login, Client.password == password).get()):

            s += "Такой логин существует"

        else:

            my_client = Client(name,surname,patronymic, passport_id,passport_number, date_of_birth)
            my_client.save()
            s = "Успешная регистрация"

        return s
