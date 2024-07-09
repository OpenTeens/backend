from MercurySQL import set_driver, DataBase
from MercurySQL.drivers.sqlite import Driver_SQLite

import random
from hashlib import sha256
import datetime

set_driver(Driver_SQLite)

db = DataBase("uniauth.db")
tb = db["login_token"]
KEY = sha256(str(random.random())).hexdigest()

tb.struct({"token": str, "username": str, "validDate": str}, primaryKey="token")


def _gentoken(username: str, data: dict):
    return sha256(f"{KEY}{username}{str(data)}").hexdigest()


def _validate(validDate: str):
    return datetime.datetime.strptime(validDate, "%Y-%m-%d %H:%M:%S") > datetime.datetime.now()

def create_token(username: str, data: dict, expire: int = 60):
    """
    login_token: JWT-like
    valid for 60 days in default
    """
    token = _gentoken(username, data)
    validDate = (datetime.datetime.now() + datetime.timedelta(days=expire)).strftime("%Y-%m-%d %H:%M:%S")

    # already exists
    if list(tb["token"] == token):
        return None

    # one account can only have 5 tokens
    if len(list(tb["username"] == username)) < 5:
        tb.insert(username=username, token=token, validDate=validDate)
        return token
    else:
        # delete expired tokens
        for data in tb["username"] == username:
            if not _validate(data["validDate"]):
                data = tb["token"] == data["token"]
                del data

        # add token
        if len(list(tb["username"] == username)) < 5:
            tb.insert(username=username, token=token, validDate=validDate)
            return token

    return None


def check_token(username, data, token: str):
    # token is in the database
    if not list(tb["token"] == token):
        return False

    # token is valid
    if _gentoken(username, data) != token:
        return False
    
    # token is not expired
    validDate = list(tb["token"] == token)[0]["validDate"]
    if _validate(validDate):
        return True
    

def del_token(token: str):
    if list(tb["token"] == token):
        data = tb["token"] == token
        del data
        return True
    return False
