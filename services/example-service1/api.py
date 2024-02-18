"""
这个文件是必须的。

这个文件定义了对模块提供的API。

提供方式 **只能** 是对业务逻辑的 import, 不能进行其他处理。

----------------------------------------------
别的模块通过 

```py
from services.example_service1.api imoprt API1, API2, ...
```

来使用这个模块提供的API。
这些对模块暴露的api在这里被定义。
"""

from .func import add, hlwd
