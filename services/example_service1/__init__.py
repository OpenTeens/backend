"""
每一个模块必须的文件:
  - __init__.py
  - router.py       
  - api.py


__init__.py必须提供的东西:
  - entrypoint(settings: dict) -> dict
  - init_router(settings: dict) -> fastapi.APIRouter
"""
from . import router
from . import api

def entrypoint(settings: dict):
    return {
        "Author": "Example <xxx@example.com>",
        "Version": "0.0.1",
        "Description": "Example Service 1",
        "PublicRouter": router.router,
        "API": api,
    }
