from Bank_system.model.client import Client

class AuthorizationService:

    @staticmethod
    def log_in(login,password):

        my_client = Client.select().where(Client.login == login, Client.password == password).get()
        if(my_client):
            return my_client.id
        else:
            return -1