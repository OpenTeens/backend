'''
Date: 2024-02-18 15:41:17
LastEditors: 宁静致远 468835121@qq.com
LastEditTime: 2024-02-18 15:51:41
'''
'''
Date: 2024-02-18 15:41:17
LastEditors: 宁静致远 468835121@qq.com
LastEditTime: 2024-02-18 15:44:36
'''
"""
[该文件为必须文件]
router.py用于定义对外公开的api路由, 并提供一个router对象供__init__.py调用。

需要提供的东西:
  - router: fastapi.APIRouter

----------------------------------------------------------
这里的函数应当能直接处理fastapi的调用。

一般该函数的内容:
1. Get Parameter    从http请求中取获取参数
2. Type Check       进行类型校验
3. Type Convert     进行类型转化
4. Process          调用api.py内的api函数。(提供给外部的api显然也得提供给内部)
5. Return           处理业务函数的返回值, reformat为json或其他格式, 返回给用户。

【注意】：为了保证代码简洁，这里的函数 **只能** 调用提供给业务逻辑函数。
"""

import fastapi

from . import api


router = fastapi.APIRouter(prefix="/example")

@router.get("/add")
def add(a:int,b:int):
    """
    对func.add进行简单封装。

    从参数中获取a和b, 做类型转化, 然后调用api.add。
    **(为了代码整齐, 只能做这些)**

    :param a: int
    :param b: int

    :return: int
    """
    # Get parameter
    # request = fastapi.Request()
    # a = request.args.get("a")
    # b = request.args.get("b")

    # Type Check
    if not isinstance(a, int) or not isinstance(b, int):
        return {
            "code": 1,
            "msg": "Parameter Error",
            "data": None
        }
    
    # Type Convert
    a = int(a)
    b = int(b)

    # Process
    ret = api.add(a, b)

    # Return
    return {
        "code": 0,
        "msg": "Success",
        "data": ret
    }

@router.get("/wrong")
def wrong_example(a:int,b:int,c:int):
    """
    一个 **错误** 的例子。

    这个函数调用了两个业务逻辑函数, 这是不允许的。

    :return: int
    """
    # Get parameter
    # request = fastapi.Request()
    # a = request.args.get("a")
    # b = request.args.get("b")
    # c = request.args.get("c")

    # [Warning!] Call two business logic function
    ret = api.add(a, b) + api.add(b, c)
    # or
    ret = api.add(api.add(a, b), c)

    # Return
    return {
        "code": 0,
        "msg": "Success",
        "data": ret
    }
