import peewee

bank_db = peewee.SqliteDatabase('BD.db')


class BaseModel(peewee.Model):

    class Meta:
        database = bank_db