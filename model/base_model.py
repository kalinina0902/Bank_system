import peewee

bank_db = peewee.SqliteDatabase('')


class BaseModel(peewee.Model):

    class Meta:
        database = bank_db