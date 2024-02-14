"""
[service] Verify Service

* this: 本服务
* s1: 调用本服务的服务
* client: 用户的客户端

1. [s1]      请求内网api "/newVerify" 来进行一个新的验证 (需提供一个回调地址、一个 session ID)
2. [client]  通过路由请求内部api "/verifyOutsideCode" 进行验证
3. [this]    将 [client] 重定向到 "<CALLBACK> ?s= <SUCCESS> &v= <INSIDE-CODE>" (`SUCCESS` 为 `0/1`, 代表验证失败/成功, `INSIDE-CODE` 为内部验证码)
4. [s1]      请求内网api "/verifyInsideCode" 验证 `INSIDE-CODE`
5. [s1]      根据返回字段 `ok` 判断验证是否成功, `sess` 来恢复会话

"""
import flask
from flask import request

import verify

app = flask.Flask(__name__)


@app.route("/newVerify", methods=["GET"])
def newVerify():
    """
    [内部] 进行一个新的验证

    [Request]
    method: str = [email]
    session: str
    callbackURI: str (建议使用绝对路径)

    [Response]
    {
        code: int
    }
    """
    method = request.args.get("method")
    session = request.args.get("session")
    callbackURI = request.args.get("callbackURI")

    code = verify.genOutsideCode(session, callbackURI)

    if method == "email":
        # [TODO]: Send Email
        print("Send Email:", code)
        pass

    return {"code": 0}


@app.route("/verifyOutsideCode", methods=["GET"])
def verifyOutsideCode():
    """
    [外部] 验证外部验证码

    [Request]
    code: str

    [Response]
    Redirect
    """
    code = request.args.get("code")

    result = verify.verifyOutsideCode(code)
    if result:
        sess = result["session"]
        callbackURI = result["callbackURI"]

        insideCode = verify.genInsideCode(sess)
        redirectURI = f"{callbackURI}?s=1&v={insideCode}"
    else:
        redirectURI = "ERROR: Invalid Verification Link"

    print("Redirect to", redirectURI)

    return redirectURI


@app.route("/verifyInsideCode", methods=["GET"])
def verifyInsideCode():
    """
    [内部] 验证内部验证码

    [Request]
    code: str

    [Response]
    {
        code: int,
        ok: bool,
        sess: str
    }
    """
    code = request.args.get("code")

    result = verify.verifyInsideCode(code)
    if result:
        return {"code": 0, "ok": True, "sess": result["session"]}
    else:
        return {"code": -1}



if __name__ == "__main__":
    app.run("localhost", 5003)
