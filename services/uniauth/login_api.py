from flask import request

from . import login_check

def login_pwd():
    username = request.form.get("username")
    pwd = request.form.get("password")

    return login_check.login(username, pwd)

def login_token():
    token = request.cookies.get("ot_login_token", None)
    if token is None:
        return {
            "code": 1,
            "msg": "No token"
        }

    return login_check.tlogin(token)

def register():
    username = request.form.get("username")
    pwd = request.form.get("password")

    return login_check.register(username, pwd)

def logout():
    token = request.form.get("token")

    return login_check.logout(token)

def pipe_auth(prev_data: dict):
    token = request.cookies.get("ot_login_token", None)
    if token is not None:
        tlogin = login_check.tlogin(token)
        if tlogin["code"] == 0:
            return {
                "reject": False,
                "result": {
                    "authorized": True,
                    "username": tlogin["username"]
                }
            }
    else:
        return {
            "reject": False,
            "result": {
                "authorized": False
            }
        }
