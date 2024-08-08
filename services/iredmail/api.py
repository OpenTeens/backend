from flask import request

from . import irm_restful


def activate(prev_process):
    if prev_process["authorized"] is False:
        return {"code": 1, "msg": "unauthorized"}

    uname = prev_process["username"]

    # create if not exist
    userprof = irm_restful.user_get(uname)
    if userprof is None:
        passwd = request.json["passwd"]
        success = irm_restful.user_create(uname, passwd, 1024)
        return success

    return True
