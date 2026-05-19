# Python + FastAPI 学习路线图

> 🎯 适合 ADHD 学习者的 Python 与 FastAPI 完整学习资料
> 
> 📁 所有文档位于 `/md` 目录下

---

## 📚 文档目录

### 学习顺序建议

```
第0步: 00_环境配置与PyCharm使用.md  →  开发环境准备
    ↓
第1步: 01_Python基础.md              →  变量、列表、字典、函数、类
    ↓
第2步: 02_Python进阶.md              →  运算符、异常处理、文件操作、继承
    ↓
第3步: 03_Python高级特性.md          →  列表推导式、生成器、装饰器
    ↓
第4步: 04_FastAPI基础.md             →  JSON、路径参数、查询参数
    ↓
第5步: 05_FastAPI_CRUD.md            →  Pydantic、增删改查
    ↓
第6步: 06_FastAPI_ORM_SQLAlchemy.md  →  数据库、ORM、IoC/DI
    ↓
第7步: 07_代码分层与模块化架构.md    →  APIRouter、分层架构、UPDATE操作
    ↓
第8步: 08_提示词工程与聊天记忆.md    →  System Prompt、多轮对话、上下文记忆
    ↓
第9步: 09_RAG_向量数据库入门.md      →  Embedding、ChromaDB、语义检索、双存储架构
```

---

## 📖 各文档内容速览

### [00_环境配置与PyCharm使用.md](./00_环境配置与PyCharm使用.md)
**对应代码**: `script.py`

- PyCharm 简介与版本选择
- Python 脚本基本结构
- `if __name__ == '__main__'` 详解
- PyCharm 常用快捷键（Mac/Windows）
- 调试技巧与断点使用
- 虚拟环境配置与管理

---

### [01_Python基础.md](./01_Python基础.md)
**对应代码**: `py学习.py`

- **变量与基础类型**: `int`, `float`, `str`, `bool`
- **列表 List**: 创建、索引、修改、常用方法
- **元组 Tuple**: 不可变序列、与列表的区别
- **循环结构**: `for`, `range()`, 循环求和
- **条件判断**: `if-elif-else`, 比较运算符
- **字典 Dict**: 键值对、遍历、方法
- **函数定义**: 参数、返回值、f-string
- **面向对象基础**: 类、`__init__`、`self`

---

### [02_Python进阶.md](./02_Python进阶.md)
**对应代码**: `py学习_进阶.py`

- **运算符详解**: 比较、逻辑(`and/or/not`)、成员(`in/not in`)
- **循环控制**: `while`, `break`, `continue`
- **字符串操作**: 切片、方法、格式化
- **集合 Set**: 去重、数学运算
- **列表进阶**: `remove()`, `pop()`, 合并
- **函数进阶**: 默认参数、`*args`、lambda
- **异常处理**: `try-except-finally`, 常见异常类型
- **文件操作**: 读写、上下文管理器(`with`)
- **模块导入**: `import`, `from...import`
- **面向对象继承**: 父类/子类、方法重写、`super()`

---

### [03_Python高级特性.md](./03_Python高级特性.md)
**对应代码**: `py学习_进阶2.py`

- **列表推导式**: `[x for x in range(10)]`, 带条件筛选
- **生成器 Generator**: 惰性计算、节省内存、`next()`
- **yield 详解**: 
  - 函数暂停与恢复机制
  - 为什么 `get_db()` 使用 `yield` 而不是 `return`
  - 上下文管理器模式
- **装饰器 Decorator**: 
  - 原理与语法糖 `@`
  - 带参数的装饰器
  - 多个装饰器叠加

---

### [04_FastAPI基础.md](./04_FastAPI基础.md)
**对应代码**: `python_接触fastapi之前的补充.py`

- **JSON 数据处理**: `json.dumps()`, `json.loads()`
- **FastAPI 简介**: 特点、安装
- **创建第一个 API**: `FastAPI()` 实例、路由
- **路径参数**: `/items/{id}`, 类型声明
- **查询参数**: `?key=value`, 默认值、可选参数
- **启动服务器**: `uvicorn.run()`, 参数详解

---

### [05_FastAPI_CRUD.md](./05_FastAPI_CRUD.md)
**对应代码**: `py_CRUD.py`

- **CRUD 概念**: Create, Read, Update, Delete
- **Pydantic 数据模型**: `BaseModel`, 字段类型、校验
- **模拟数据库**: 内存存储、列表操作
- **Create (增)**: POST, 请求体解析
- **Read (查)**: GET, 返回列表/单个
- **Delete (删)**: DELETE, 索引检查
- **HTTP 状态码**: 200, 201, 404, 422
- **HTTPException**: 错误处理

---

### [06_FastAPI_ORM_SQLAlchemy.md](./06_FastAPI_ORM_SQLAlchemy.md)
**对应代码**: `py_ORM.py`

- **架构概览**: 分层结构图
- **数据库连接配置**: 
  - `create_engine()` 引擎
  - `sessionmaker()` 会话工厂
  - `declarative_base()` 基类
- **ORM 模型定义**: 
  - 类与表的映射
  - `Column`, `primary_key`, `index`
- **核心概念深度解析**:
  - **IoC (控制反转)**: 什么是控制、为什么反转
  - **DI (依赖注入)**: 提供者、消费者、容器
  - 类比理解（餐厅、出租车、电力公司）
- **yield 在依赖注入中的作用**:
  - 完整执行流程图解
  - 资源管理保证
- **CRUD 操作详解**: 
  - `db.add()`, `db.commit()`, `db.refresh()`
  - `db.query()`, `db.filter()`, `db.delete()`
- **完整请求生命周期追踪**: 7 个阶段详解

---

### [07_代码分层与模块化架构.md](./07_代码分层与模块化架构.md)
**对应代码**: `main.py` + `database.py` + `models.py` + `routers.py`

- **为什么要分层**: 单体文件的问题、分层的好处
- **分层架构详解**: 表现层、业务层、模型层、数据层
- **各层代码解析**:
  - `database.py`: 数据库连接、会话工厂
  - `models.py`: ORM 模型、建表
  - `routers.py`: APIRouter、业务逻辑
  - `main.py`: 应用组装、路由注册
- **APIRouter 深度解析**:
  - 什么是子路由器
  - `prefix` 和 `tags` 参数
  - 多 Router 组织
  - `app.include_router()` 高级用法
- **UPDATE 操作详解**:
  - PUT vs PATCH
  - ORM 脏数据追踪机制
  - 完整执行流程
- **模块导入关系图**: 导入链、循环导入问题
- **从单体到分层的演变**: 项目结构演进

---

### [08_提示词工程与聊天记忆.md](./08_提示词工程与聊天记忆.md)
**对应代码**: `routers/chat_memory.py`

- **为什么需要记忆**: 无状态 vs 有状态对话
- **核心数据结构**: `chat_history` 列表、`role` 字段含义
- **System Prompt 详解**:
  - 什么是系统指令
  - 如何给 AI "洗脑"
  - 提示词工程技巧
- **多轮对话实现**: 五步记忆法
  - 洗脑 → 记录 → 发请求 → 拿结果 → 存档
- **为什么发送完整历史**: AI 无状态特性
- **辅助路由**: 查看记录、清空记录
- **局限性与改进**: 内存存储、用户隔离、会话管理

---

### [09_RAG_向量数据库入门.md](./09_RAG_向量数据库入门.md)
**对应代码**: `rag_demo.py`（本章新建）

- **为什么需要向量数据库**: SQL LIKE 的语义盲区
- **Embedding 核心概念**:
  - 文本 → 向量的转换
  - 语义指纹、高维空间
  - 余弦相似度计算
- **向量数据库 vs 关系型数据库**: 概念映射对比表
- **ChromaDB 实战**:
  - 安装与配置
  - Collection 创建与管理
  - `add()` 数据入库（自动 Embedding）
  - `query()` 语义检索
- **生产级设计**: ChunkVector 结构、双存储架构（CQRS）
- **RAG 最小原型**: FastAPI + Chroma 实现 /ingest + /search
- **Embedding API 调用**: OpenAI / ModelScope 获取文本向量

---

## 🎯 学习建议

### 对于 ADHD 学习者

1. **番茄工作法**: 每学习 25 分钟休息 5 分钟
2. **动手实践**: 看完一个知识点立即写代码验证
3. **视觉化**: 利用文档中的流程图、表格帮助理解
4. **循序渐进**: 按顺序学习，不要跳步
5. **做笔记**: 用自己的话总结每个概念

### 学习检查清单

- [ ] 能独立写出 Python 基础数据类型操作
- [ ] 理解 `for` 循环和列表推导式的区别
- [ ] 能解释 `yield` 和 `return` 的区别
- [ ] 能说出 IoC 和 DI 的核心思想
- [ ] 能独立创建一个 FastAPI 应用
- [ ] 能使用 SQLAlchemy 完成增删改查
- [ ] 理解代码分层架构，能解释每层职责
- [ ] 能使用 APIRouter 组织多模块路由
- [ ] 理解 System Prompt 的作用，能设计简单的人设
- [ ] 能解释多轮对话的实现原理（chat_history 机制）
- [ ] 理解 Embedding 和语义相似度的概念
- [ ] 能使用 ChromaDB 完成数据的存与取
- [ ] 理解双存储架构（关系库+向量库）的分工

---

## 🔗 代码文件对应关系

| 学习文档 | 对应代码文件 | 难度 |
|----------|-------------|------|
| 00_环境配置与PyCharm使用.md | `script.py` | ⭐ |
| 01_Python基础.md | `py学习.py` | ⭐ |
| 02_Python进阶.md | `py学习_进阶.py` | ⭐⭐ |
| 03_Python高级特性.md | `py学习_进阶2.py` | ⭐⭐⭐ |
| 04_FastAPI基础.md | `python_接触fastapi之前的补充.py` | ⭐⭐ |
| 05_FastAPI_CRUD.md | `py_CRUD.py` | ⭐⭐⭐ |
| 06_FastAPI_ORM_SQLAlchemy.md | `py_ORM.py` | ⭐⭐⭐⭐ |
| 07_代码分层与模块化架构.md | `main.py` + `routers.py` + `models.py` + `database.py` | ⭐⭐⭐⭐ |
| 08_提示词工程与聊天记忆.md | `routers/chat_memory.py` | ⭐⭐⭐ |
| 09_RAG_向量数据库入门.md | `rag_demo.py` | ⭐⭐⭐⭐ |

---

## 📌 重点知识速查

### Python 核心

```python
# 列表推导式
[x*2 for x in range(10) if x % 2 == 0]

# 生成器表达式
(x**2 for x in range(1000000))

# 装饰器
def decorator(func):
    def wrapper(*args, **kwargs):
        # 前置操作
        result = func(*args, **kwargs)
        # 后置操作
        return result
    return wrapper

@decorator
def my_func():
    pass
```

### FastAPI 核心

```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

app = FastAPI()

# Pydantic 模型
class Item(BaseModel):
    name: str
    price: float = 0.0

# 依赖注入
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 路由
@app.post("/items")
def create_item(item: Item, db: Session = Depends(get_db)):
    db_item = DBItem(**item.dict())
    db.add(db_item)
    db.commit()
    return db_item
```

---

## 🚀 下一步学习方向

完成本系列学习后，可以探索：

1. **数据库迁移**: Alembic
2. **用户认证**: JWT、OAuth2
3. **异步编程**: async/await
4. **测试**: pytest、TestClient
5. **部署**: Docker、云服务器
6. **前端对接**: React/Vue + FastAPI

---

## 💡 遇到问题？

1. **重新阅读对应文档**: 每个文档都有详细解释和示例
2. **查看代码注释**: 源代码中有丰富的注释说明
3. **动手实验**: 修改代码，观察结果变化
4. **画流程图**: 把执行流程画出来帮助理解

---

**祝你学习愉快！记住：理解 > 记忆，实践 > 阅读。**
