# 项目记忆 - PyCharmMiscProject

## 项目基本信息

- **项目名称**: PyCharmMiscProject
- **项目类型**: Python + FastAPI 学习项目
- **创建时间**: 2024年
- **主要用途**: Python 后端开发学习，从基础到 FastAPI + SQLAlchemy ORM

## 技术栈

- **语言**: Python 3.9
- **Web框架**: FastAPI
- **数据库**: SQLite (开发阶段)
- **ORM**: SQLAlchemy
- **服务器**: Uvicorn
- **IDE**: PyCharm

## 项目结构

```
PyCharmMiscProject/
├── .trae/
│   └── memory/           # 记忆存储文件夹
├── .venv/                # Python 虚拟环境
├── .idea/                # PyCharm 配置
├── md/                   # 学习文档 (8个Markdown文件)
│   ├── README.md
│   ├── 00_环境配置与PyCharm使用.md
│   ├── 01_Python基础.md
│   ├── 02_Python进阶.md
│   ├── 03_Python高级特性.md
│   ├── 04_FastAPI基础.md
│   ├── 05_FastAPI_CRUD.md
│   ├── 06_FastAPI_ORM_SQLAlchemy.md
│   └── 07_代码分层与模块化架构.md
├── main.py               # FastAPI 应用入口 (分层架构)
├── database.py           # 数据库配置
├── models.py             # ORM 模型
├── routers.py            # API 路由 (业务逻辑)
├── py学习.py             # Python 基础练习
├── py学习_进阶.py        # Python 进阶练习
├── py学习_进阶2.py       # Python 高级特性
├── python_接触fastapi之前的补充.py  # FastAPI 入门
├── py_CRUD.py            # FastAPI CRUD 练习
├── py_ORM.py             # FastAPI + SQLAlchemy 练习
├── script.py             # PyCharm 示例脚本
└── .my_database.db       # SQLite 数据库文件
```

## 学习进度

- [x] Python 基础 (变量、列表、字典、函数、类)
- [x] Python 进阶 (运算符、异常处理、文件操作、继承)
- [x] Python 高级特性 (列表推导式、生成器、装饰器)
- [x] FastAPI 基础 (JSON、路径参数、查询参数)
- [x] FastAPI CRUD (Pydantic、增删改查)
- [x] FastAPI ORM (SQLAlchemy、依赖注入)
- [x] 代码分层 (APIRouter、模块化架构)
- [ ] 前端对接 (待学习)

## 核心概念掌握情况

### 已掌握
- Python 基础语法和数据结构
- 函数和面向对象编程
- 列表推导式和生成器
- 装饰器原理
- FastAPI 路由和参数
- Pydantic 数据模型
- SQLAlchemy ORM 操作
- 依赖注入 (DI) 和控制反转 (IoC)
- yield 在资源管理中的应用
- APIRouter 模块化组织

### 待深入学习
- 异步编程 (async/await)
- 用户认证 (JWT/OAuth2)
- 数据库迁移 (Alembic)
- 测试 (pytest)
- Docker 部署
- 前端框架对接 (React/Vue)
