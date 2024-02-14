# OpenTeens 社区后端开发文档 📖

## 项目介绍 🚀

OpenTeens社区后端项目是由OpenTeensCore团队开发的，旨在为前端提供必要的API接口和技术支持。

## 开始之前 🛠️

(待完善)

## 如何下载项目 📦

(待完善)

## 进行开发 👨‍💻👩‍💻

### 设置开发环境

建议使用Visual Studio Code或PyCharm作为开发IDE，它们提供了良好的Python语言支持和便捷的调试工具。

### 目录结构

经过一定的讨论，我们决定使用FastAPI重构这个后端项目。
我们首先尝试使用模块化编程，下面的文件目录是我和GPT对话后得到的结果。
其中`user/`目录和`post/`目录是一个组件的示例

```
OpenTeens_Backend/
│
├── app/                  # 应用主目录
│   ├── __init__.py       # 初始化应用和全局配置
│   ├── main.py           # FastAPI应用实例和应用入口
│   │
│   ├── api/              # 所有API组件的根目录
│   │   ├── __init__.py   # 初始化API模块
│   │   ├── deps.py       # 依赖项（数据库连接、权限校验等）
│   │   │
│   │   ├── user/         # 用户系统模块
│   │   │   ├── __init__.py
│   │   │   ├── models.py # 用户模型定义
│   │   │   ├── schemas.py # 请求和响应的模式
│   │   │   └── routes.py  # 用户系统相关路由
│   │   │
│   │   └── post/         # 发帖系统模块
│   │       ├── __init__.py
│   │       ├── models.py # 帖子模型定义
│   │       ├── schemas.py # 请求和响应的模式
│   │       └── routes.py  # 发帖系统相关路由
│   │
│   └── core/             # 核心配置和实用程序
│       ├── config.py     # 配置文件
│       └── security.py   # 安全和认证工具
│
└── tests/                # 测试目录
│   ├── __init__.py
│   ├── test_user.py
│   └── test_post.py
│
├── README.md
└── "Other files"
```

### 添加新的API

1. 编写一份微服务，写入services文件夹内部
2. 在（未来的）启动文件内加入该微服务并设置

### 编写代码

遵循开发标准，代码格式尽量保持一致，写一定量的注释，熟悉使用Pylint进行代码检查。

## Git提交规范 📝

创建分支的时候请遵循分支分类+名称的命名规则，如`feat-sqlite`。如果有很多修改可以用名字/分类-名称的方式，如`lanbinshiji-sqlite`。这些分支名经过测试都是合法的。

为了提高项目的可维护性，请遵循以下Git提交信息规范：

- 功能添加：`[feat] 添加了新的登录功能`
- 问题修复：`[fix] 修复了用户认证bug`
- 文档更新：`[docs] 更新了README文件`
- 性能优化：`[perf] 优化了数据库查询效率`
- 代码重构：`[refactor] 重构了用户服务模块`
- 测试代码：`[test] 添加了新的API测试用例`

## 贡献指南 🤝

欢迎通过Pull Requests或Issue来贡献您的智慧。在提交PR之前，请确保您的代码符合上述开发和Git提交规范。

## 开发周期

@lanbinshijie 明天写

---

我的一些设计想法，可以尝试修改？—— Lanbin 2024-2-15 02:09:54

**以下内容和GPT共同生成**

## 项目架构说明

本项目采用Python的FastAPI框架，并结合模块化编程的理念进行开发，旨在将不同的服务功能（如用户系统、发帖系统等）分别封装成独立的组件。每个组件内部包含了该服务相关的所有业务逻辑处理。

### 服务组件化

我们将每个服务（例如用户系统包括注册、登录、鉴权等功能；发帖系统等）设计为一个独立的组件。这样做的目的是为了提高代码的可维护性和可扩展性，同时也便于团队成员并行开发和维护。

### API路由设计

每个组件都定义了一个“API根”，以及一系列暴露给外部使用的API接口。这些接口通过FastAPI的主函数（main）暴露到公网。例如，用户系统组件的API根为`/user`，在此基础上，注册功能的路由为`/reg`，因此该功能对应的全局API路径就是`/user/reg`。这种设计使得API的结构清晰、易于管理，同时也方便了前端与其他服务的对接。

### 实现思想

1. **模块化**: 每个服务（用户系统、发帖系统等）作为独立模块存在，在其自身目录下维护相关的路由、模型、模式等。
2. **路由分发**: 在每个模块的`routes.py`中定义该模块的路由，并在应用的主文件`main.py`中导入和挂载这些路由。
3. **依赖管理**: 使用`deps.py`来定义全局依赖（如数据库会话、权限校验函数等），这些依赖可以在各个路由中重用。
4. **配置管理**: 在`core/config.py`中集中管理配置，例如数据库连接信息、秘钥等，可以使用环境变量来灵活管理不同环境下的配置。

### 代码示例

#### `app/main.py`

```python
from fastapi import FastAPI
from app.api.user.routes import router as user_router
from app.api.post.routes import router as post_router

app = FastAPI()

# 挂载路由
app.include_router(user_router, prefix="/user")
app.include_router(post_router, prefix="/post")
```

#### `app/api/user/routes.py`

```python
from fastapi import APIRouter

router = APIRouter()

@router.post("/reg")
def register_user():
    # 用户注册逻辑
    return {"message": "User registered successfully."}
```

#### `app/api/post/routes.py`

```python
from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def create_post():
    # 创建帖子逻辑
    return {"message": "Post created successfully."}
```

