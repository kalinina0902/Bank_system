from Bank_system.model.client import Client

class AuthorizationService:

    def log_in(self, login,password):

        my_client = Client.select().where(Client.login == login, Client.password == password).get()
        if(my_client):
            return my_client.id
        else:
            return -1
