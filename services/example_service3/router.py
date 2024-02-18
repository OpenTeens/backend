'''
Date: 2024-02-18 15:41:17
LastEditors: 宁静致远 468835121@qq.com
LastEditTime: 2024-02-18 16:10:28
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

# 模块间调用
from ..example_service2.api import me


router = fastapi.APIRouter(prefix="/example3")

@router.get("/say")
def say(a:str):
    return me(a)
