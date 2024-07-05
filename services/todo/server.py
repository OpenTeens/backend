import todo_db

import flask

app = flask.Flask(__name__)

@app.route("/create/<listID>", methods=["PUT"])
def createList(listID):
    if todo_db.addTable(listID):
        return {"code": 0, "status": "success", "listID": listID}
    else:
        return {"code": 1, "status": "failed", "listID": listID}

@app.route("/<listID>/addTask", methods=["POST"])
def addTask(listID: str):
    data = flask.request.json
    # default
    default = {
        "title": "",
        "content": "",
        "ddl": "",
        "manager": "",
        "reviewer": ""
    }
    for key in default:
        if key not in data:
            data[key] = default[key]
    
    # add task
    todo_db.addTask(listID, data["title"], data["content"], data["ddl"], data["manager"], data["reviewer"])
    return {"code": 0, "status": "success"}

@app.route("/<listID>/updateTask", methods=["POST"])
def updateTask(listID: str):
    data = flask.request.json
    id = data["id"]
    todo_db.updateTask(listID, id, **data["update"])
    return {"code": 0, "status": "success"}

@app.route("/<listID>/getTasks", methods=["GET"])
def getTasks(listID: str):
    tasks = todo_db.getTasks(listID)
    return {"code": 0, "status": "success", "tasks": [list(res) for res in tasks]}

@app.route("/<listID>/getTask", methods=["GET"])
def getTask(listID: str):
    id = flask.request.args.get("id")
    task = todo_db.getTask(listID, id)
    return {"code": 0, "status": "success", "task": list(task)}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
