import todo_db

import flask
from hashlib import sha256, sha512


def _hash(s):
    return (
        "s"
        + sha256(s.encode("utf-8")).hexdigest()
        + sha512(s.encode("utf-8")).hexdigest()
    )


def createList(prev_process, listID):
    listID = _hash(listID)

    if todo_db.addTable(listID):
        return {"code": 0, "msg": "success", "listID": listID}
    else:
        return {"code": 1, "msg": "already exist", "listID": listID}


def addTask(prev_process, listID: str):
    listID = _hash(listID)

    data = flask.request.json
    # default
    default = {"title": "", "content": "", "ddl": "", "manager": "", "reviewer": ""}
    for key in default:
        if key not in data:
            data[key] = default[key]

    # add task
    tid = todo_db.addTask(
        listID,
        data["title"],
        data["content"],
        data["ddl"],
        data["manager"],
        data["reviewer"],
    )
    return {"code": 0, "msg": "success", "id": tid}


def updateTask(prev_process, listID: str):
    listID = _hash(listID)

    data = flask.request.json
    id = data["id"]
    todo_db.updateTask(listID, id, **data["update"])
    return {"code": 0, "msg": "success"}


def getTasks(prev_process, listID: str):
    listID = _hash(listID)

    if listID not in todo_db.db.tables:
        if todo_db.addTable(listID):
            return {"code": 0, "msg": "success", "listID": listID}
        else:
            return {"code": 1, "msg": "already exist", "listID": listID}

    tasks = todo_db.getTasks(listID)
    return {"code": 0, "msg": "success", "tasks": list(tasks)}
