"""

"""

from fastapi import APIRouter
from dynaconf import Dynaconf

from . import router

router.init(APIRouter(prefix="/verify"))


def entrypoint(settings: Dynaconf):
    return {
        "Author": "Bernie H.",
        "Version": "1.0.0",
        "Describe": "验证微服务，主要用于验证用户的邮箱等。",
        "Router": router.router,
        "Init": lambda: init(settings),
    }


g_settings = None


def init(settings: Dynaconf):
    print("Verify service is starting...")
    global g_settings
    g_settings = settings

