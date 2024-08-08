from MercurySQL import DataBase
from MercurySQL.drivers.sqlite import Driver_SQLite

db = DataBase("account.db", Driver_SQLite)
tb = db['account_info']
