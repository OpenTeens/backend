from MercurySQL import set_driver, DataBase
from MercurySQL.drivers.sqlite import Driver_SQLite

set_driver(Driver_SQLite)

db = DataBase("uniauth.db")
tb = db["login"]
tb.struct({"username": str, "password": str}, primaryKey="username")


def register(username, password):
    if not list(tb["username"] == username):
        tb.insert(username=username, password=password)
        return True
    return False


def login(username, password):
    if list((tb["username"] == username) & (tb["password"] == password)):
        return True
    return False


if __name__ == "__main__":
    print(register("bernie", "123456"))
    print(login("bernie", "123456"))
