# -*- coding: utf-8 -*-
# Date: 2024-02-16 14:45:49
# LastEditors: 宁静致远 468835121@qq.com
# LastEditTime: 2024-02-16 22:15:25

import fastapi
import os
import importlib
import logging
from config import settings

logger = logging.getLogger(settings.get('logger',default='OpenTeens'))
logger.setLevel(logging.INFO)
application = fastapi.FastAPI(
    title='OpenTeens',
    debug=settings.get('debug',default=False),
    )

# include services

services_path='services'
if not os.path.exists(services_path):
    logger.critical(f"{os.path.join(os.getcwd(),services_path)} 不存在")
    raise OSError(f"{os.path.join(os.getcwd(),services_path)} 不存在")

services = os.listdir(services_path)
for service in services:
    try:
        entrypoint = importlib.import_module(f"{services_path}.{service}").entrypoint
        metadata = entrypoint(settings)
        logger.warn("#"*50+f"""
加载{service}
\t作者{metadata['Author']}
\t版本{metadata['Version']}
\t描述{metadata['Describe']}
"""+"#"*50)
        application.include_router(metadata['Router'])
        metadata['Init']()
    except Exception as e:
        logger.warn(f"加载{service}出错")
        logger.warn(e)
        if settings.get('debug',default=False):raise e
