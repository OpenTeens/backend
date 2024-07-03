import flask

import logindb

app = flask.Flask(__name__)


@app.route("/login", methods=["POST"])
def login():
    username = flask.request.form["username"]
    password = flask.request.form["password"]
    tokenreq = flask.request.form["tokenreq"]

    if logindb.login(username, password):
        uid = logindb.get_by_uname(username).uid
        return {
            "code": 200,
            "msg": "Login successful",
            "token": logindb.add_token(uid, tokenreq),
        }
    else:
        return {"code": 401, "msg": "Login failed"}


@app.route("/register", methods=["POST"])
def register():
    username = flask.request.form["username"]
    password = flask.request.form["password"]
    tokenreq = flask.request.form["tokenreq"]

    if logindb.get_by_uname(username) is not None:
        return {"code": 409, "msg": "Username already exists"}
    else:
        uid = logindb.add(username, password)
        return {
            "code": 200,
            "msg": "Registration successful",
            "token": logindb.add_token(uid, tokenreq),
        }


if __name__ == "__main__":
    app.run(debug=True)
