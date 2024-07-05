import todo_db

import flask
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app, origins="*")


@app.route("/create/<listID>", methods=["GET"])
def createList(listID):
    if todo_db.addTable(listID):
        return {"code": 0, "msg": "success", "listID": listID}
    else:
        return {"code": 1, "msg": "already exist", "listID": listID}


@app.route("/<listID>/addTask", methods=["POST"])
def addTask(listID: str):
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


@app.route("/<listID>/updateTask", methods=["POST"])
def updateTask(listID: str):
    data = flask.request.json
    id = data["id"]
    todo_db.updateTask(listID, id, **data["update"])
    return {"code": 0, "msg": "success"}


@app.route("/<listID>/getTasks", methods=["GET"])
def getTasks(listID: str):
    if listID not in todo_db.db.tables:
        createList(listID)
    
    tasks = todo_db.getTasks(listID)
    return {"code": 0, "msg": "success", "tasks": list(tasks)}


@app.route("/<listID>/getTask", methods=["GET"])
def getTask(listID: str):
    id = flask.request.args.get("id")
    task = todo_db.getTask(listID, id)
    return {"code": 0, "msg": "success", "task": list(task)}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
