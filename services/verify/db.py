from pony.orm import Database, Required, PrimaryKey

""" Create Database """
db = Database()


class OutsideVerifyCode(db.Entity):
    code = PrimaryKey(str)
    session = Required(str)
    expired = Required(int)
    callbackURI = Required(str)


class InsideVerifyCode(db.Entity):
    code = PrimaryKey(str)
    session = Required(str)
    expired = Required(int)


db.bind(provider="sqlite", filename="verify.db")

db.generate_mapping(create_tables=True)

from pony.orm import db_session
