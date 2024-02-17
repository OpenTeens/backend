"""
Date: 2024-02-16 13:29:36
LastEditors: 宁静致远 468835121@qq.com
LastEditTime: 2024-02-16 22:44:57
"""

# -*- coding: utf-8 -*-
# Date: 2024-02-16 13:29:36
# LastEditors: 宁静致远 468835121@qq.com
# LastEditTime: 2024-02-16 22:15:40

from fastapi import APIRouter
from dynaconf import Dynaconf

from . import router

inter_router = APIRouter(prefix="/njzy")
exp_router = APIRouter(prefix="/test")


def entrypoint(settings: Dynaconf):
    """
        description: 这个是入口点, 会传入一个settings
        return {
            "Author":作者,
            "Version":版本号,
            "Describe":描述,
            "InterRouter":内部路由对象在这里,
            "ExposeRouter":暴露到外部的路由对象在这里,
            "Init":载入路由之后的初始（可以放其他线程启动啥的，别阻塞）,
        }
    """
    router.init(inter_router, exp_router)

    return {
        "Author": "宁静致远",
        "Version": "1.0.0",
        "Describe": "实例微服务，主要测试能不能用",
        "InterRouter": inter_router,
        "ExposeRouter": exp_router,
        "Init": lambda: init(settings),
    }


g_settings = None


def init(a: Dynaconf):
    print("原神~启动！")
    print(f'试着读配置{a.get("test")}')
    global g_settings
    g_settings = a

