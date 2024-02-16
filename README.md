# OpenTeens 社区后端开发文档 📖

## 项目介绍 🚀

OpenTeens社区后端项目是由OpenTeensCore团队开发的，旨在为前端提供必要的API接口和技术支持。

## 开始之前 🛠️

确保您的开发环境中安装了以下软件：

- Python 环境
- Pip环境

## 如何下载项目 📦

1. 打开终端或命令提示符。
2. 运行以下命令来克隆项目仓库：

```bash
git clone https://github.com/OpenTeens/backend.git
```

3. 进入项目目录：

```bash
cd backend
```

## 启动项目 🚀

在项目根目录下，执行以下命令来启动项目：

```bash
pip install -U -r requirement.txt
uvicorn app:application --reload --host localhost --port 80
```

这将启动服务器，默认监听在`localhost`。您可以通过访问`http://localhost`来测试是否成功运行。

## 进行开发 👨‍💻👩‍💻

### 设置开发环境

建议使用Visual Studio Code或PyCharm作为开发IDE，它们提供了良好的Python语言支持和便捷的调试工具。

### 目录结构

- `/` - 根目录，项目启动目录
- `/services` - 微服务目录，暂时存放微服务

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

版本号按照（算了我明天写）