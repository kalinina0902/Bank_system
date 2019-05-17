from Bank_system.model.client import Client

def registration_client (name, surname, patronymic, passport_id, passport_number, date_of_birth):
   client = Client(name,surname,patronymic, passport_id,passport_number, date_of_birth)
   client.save()
