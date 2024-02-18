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

import fastapi
from fastapi import Request, Response
from starlette.responses import RedirectResponse

import verify
import send


inter_router = None
public_router = None


def init(ri: fastapi.APIRouter, rp: fastapi.APIRouter):
    global inter_router
    global public_router
    inter_router = ri
    public_router = rp

    inter_router.add_route("/newVerifyCode", newVerifyCode, methods=["GET"])
    inter_router.add_route("/verifyOutsideCode", verifyOutsideCode, methods=["GET"])
    inter_router.add_route("/verifyInsideCode", verifyInsideCode, methods=["GET"])

    public_router.add_route("/verify", verifyOutsideCode, methods=["GET"])


def _getVerifyUri(code: str):
    """
    [Tool] 从验证码生成验证链接
    """
    return f"https://openteens.org/verify/verify?code={code}"

def newVerify():
    """
    [内部] 进行一个新的验证

    Request: 
        method: str (one of [email])
        target: str (e.g. "test@openteens.org")
        session: str
        callbackURI: str (建议使用带https的绝对路径)

    Response:
        ..codeblock:: json
        {
            code: int
        }
    """
    request = Request()
    
    method = request.args.get("method")
    target = request.args.get("target")
    session = request.args.get("session")
    callbackURI = request.args.get("callbackURI")

    code = verify.genOutsideCode(session, callbackURI)

    if method == "email":
        send.sendEmail(target, _getVerifyUri(code))
    else:
        return {"code": -1}

    return {"code": 0}


def newVerifyCode():
    """
    [内部] 进行一个新的验证（返回验证链接）

    Request: 
        session: str
        callbackURI: str (建议使用带https的绝对路径)
    
    Response:
        ..codeblock:: json
        {
            code: int,
            verifyUri: str
        }
    """
    request = Request()
    
    session = request.args.get("session")
    callbackURI = request.args.get("callbackURI")

    code = verify.genOutsideCode(session, callbackURI)

    return {"code": 0, "verifyUri": _getVerifyUri(code)}


def verifyOutsideCode():
    """
    [外部] 验证外部验证码

    Request:
        code: str (外部验证码)

    Response:
        <Redirect> (重定向到回调地址)
    """
    request = Request()

    code = request.args.get("code")

    result = verify.verifyOutsideCode(code)
    if result:
        sess = result["session"]
        callbackURI = result["callbackURI"]

        insideCode = verify.genInsideCode(sess)
        redirectURI = f"{callbackURI}?s=1&v={insideCode}"
    else:
        redirectURI = "ERROR: Invalid Verification Link"

    return RedirectResponse(redirectURI)


def verifyInsideCode():
    """
    [内部] 验证内部验证码

    Request:
        code: str (内部验证码)

    Response:
        ..codeblock:: json
        {
            code: int,
            ok: bool,
            sess: str
        }
    """
    request = Request()

    code = request.args.get("code")

    result = verify.verifyInsideCode(code)
    if result:
        return {"code": 0, "ok": True, "sess": result["session"]}
    else:
        return {"code": -1}


if __name__ == "__main__":
    init(fastapi.APIRouter())
    router.run("localhost", 5003)
