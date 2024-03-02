'''
Date: 2024-02-18 15:57:15
LastEditors: 宁静致远 468835121@qq.com
LastEditTime: 2024-02-18 15:59:59
'''
def createAPIRouter():
    from fastapi import APIRouter
    router = APIRouter()
    from . import example_service2,example_service3
    router.include_router(example_service2.createAPIRouter())
    router.include_router(example_service3.createAPIRouter())
    return router