# -*- coding: utf-8 -*-
# Date: 2024-02-16 14:45:49
# LastEditors: 宁静致远 468835121@qq.com
# LastEditTime: 2024-02-16 22:15:25

"""
这里做一下重写，
"""

import fastapi
import logging
from config import settings

logger = logging.getLogger(settings.get('logger',default='OpenTeens'))
logger.setLevel(logging.INFO)
application = fastapi.FastAPI(
    title='OpenTeens',
    debug=settings.get('debug',default=False),
    )

# include services

from services import createAPIRouter
application.include_router(createAPIRouter())