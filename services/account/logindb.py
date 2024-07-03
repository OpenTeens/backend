import datetime
import random
from hashlib import md5

from MercurySQL import set_driver, DataBase
from MercurySQL.drivers.sqlite import Driver_SQLite

set_driver(Driver_SQLite)
db = DataBase("accounts.db")

tb_login = db["login"]
tb_login.struct(
    {"uid": int, "username": str, "password": str}, primaryKey="uid", autoIncrement=True
)


def get_by_uname(username):
    result = tb_login.select(tb_login["username"] == username)

    return result[0] if result else None


def get_by_uid(uid):
    result = tb_login.select(tb_login["uid"] == uid)

    return result


def add(username, password):
    if get_by_uname(username) is not None:
        return False

    tb_login.insert(username=username, password=password)

    return get_by_uname(username).uid


def update(uid, username, password):
    tb_login.update(tb_login["uid"] == uid, username=username, password=password)


def delete(uid):
    target = tb_login["uid"] == uid
    del target


def login(username, password):
    user = get_by_uname(username)
    if user is None:
        return False

    return user.password == password


tb_token = db["token"]
tb_token.struct({"uid": int, "token": str, "validate": str}, primaryKey="token")


def add_token(uid, tokenreq):
    token = f"{uid}:{random.random()}"
    token = md5(token.encode("utf-8")).hexdigest()

    validate = datetime.datetime.now() + datetime.timedelta(days=30)

    tb_token.insert(
        uid=uid,
        token=token,
        validate=validate.strftime("%Y-%m-%d %H:%M:%S"),
    )

    return token
