from MercurySQL import set_driver, DataBase
from MercurySQL.drivers.sqlite import Driver_SQLite

set_driver(Driver_SQLite)
db = DataBase("todo.db")


def addTable(tbname):
    tb = db.createTable(tbname)
    tb.struct(
        {
            "id": int,
            "title": str,
            "content": str,
            "status": int,  # 0: 未开始, 1: 正在进行, 2: 已完成
            "ddl": str,
            "manager": str,
            "reviewer": str,
        },
        primaryKey="id",
        autoIncrement=True,
    )


def addTask(tbname, title, content, ddl, manager, reviewer):
    tb = db[tbname]
    tb.insert(
        title=title,
        content=content,
        status=0,
        ddl=ddl,
        manager=manager,
        reviewer=reviewer
    )


def getTasks(tbname):
    tb = db[tbname]
    return tb.select()


def getTask(tbname, id):
    tb = db[tbname]
    return tb.select(where={"id": id})


def updateTask(tbname, id, **kwargs):
    tb = db[tbname]
    tb.update(tb["id"] == id, **kwargs)
