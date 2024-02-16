# -*- coding: utf-8 -*-
# Date: 2024-02-16 18:16:52
# LastEditors: 宁静致远 468835121@qq.com
# LastEditTime: 2024-02-16 18:49:11


from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="OTENV",
    settings_files=['settings.toml', '.secrets.toml'],
    environments=True,
    
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
