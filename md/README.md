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
第9步: 09_RAG向量数据库入门.md      →  Embedding、余弦相似度、向量概念
    ↓
第10步: 10_RAG_ChromaDB向量数据库实战.md → ChromaDB、Collection、语义检索
    ↓
第11步: 11_双存储架构SQLite_ChromaDB.md → 双存储协作、ChunkVector、RAG 存储层
    ↓
第12步: 12_FastAPI_Chroma_最小原型.md → API封装、持久化存储、依赖注入
    ↓
第13步: 13_RAG_闭环_检索到回答.md → 检索→拼Prompt→流式LLM调用完整闭环
    ↓
第14步: 14_上下文窗口管理.md → Token截断策略、超长Prompt处理、防幻觉
    ↓
第15步: 15_LangChain核心概念.md → LCEL链式语法、六大核心组件
    ↓
第16步: 16_异步编程深入.md → async/await原理、三种协程对象、Semaphore
    ↓
第17步: 17_JWT用户认证.md → JWT令牌、bcrypt、Depends守卫、角色授权
    ↓
第18步: 18_WebSocket实时通信.md → WebSocket升级、房间广播、AI流式打断
    ↓
第19步: 19_Alembic数据库迁移.md → revision、upgrade/downgrade、autogenerate
    ↓
第20步: 20_pytest单元测试.md → FastAPI TestClient、依赖覆盖、fixture
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
**对应代码**: `app/main.py` + `app/database.py` + `app/models.py` + `app/routers/`

- **为什么要分层**: 单体文件的问题、分层的好处
- **分层架构详解**: 表现层、业务层、模型层、数据层
- **各层代码解析**:
  - `app/database.py`: 数据库连接、会话工厂
  - `app/models.py`: ORM 模型、建表
  - `app/routers/`: APIRouter、业务逻辑（按功能拆分为多个文件）
  - `app/main.py`: 应用组装、路由注册、CORS/中间件配置
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
**对应代码**: `app/routers/chat_memory.py`

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
**对应代码**: `rag_demo.py`

- **为什么需要向量数据库**: SQL LIKE 的语义盲区
- **Embedding 核心概念**:
  - 文本 → 向量的转换
  - 语义指纹、高维空间
  - 余弦相似度计算
- **向量数据库 vs 关系型数据库**: 概念映射对比表
- **余弦相似度数学原理**: 点积、范数、归一化
- **RAG 最小原型概念**: 切片 → Embedding → 存储 → 检索

---

### [10_RAG_ChromaDB向量数据库实战.md](./10_RAG_ChromaDB向量数据库实战.md)
**对应代码**: `playground/chroma_demo.py`、`playground/chroma_real.py`、`playground/embedding_playground.py`、`app/embedding.py`

- **ChromaDB 核心概念**:
  - Client（客户端）与 Collection（集合）
  - 内存模式 vs 持久化模式
- **Collection 四大操作**:
  - `create_collection()` 创建集合
  - `add()` 存入数据（ids + embeddings + documents + metadatas）
  - `query()` 语义检索
  - `get()` / `delete()` 管理数据
- **简化向量 vs 真实 Embedding**:
  - 简化向量（4维，手工设计，教学用）
  - 真实 Embedding（本地bge-small-zh-v1.5，512维）
- **关键澄清**: `metadatas` 不参与相似度计算，只是标签
- **Embedding Playground 实验**: 语义相近、多义词、跨语言验证
- **本地 Embedding 部署**: sentence-transformers + MPS加速

---

### [11_双存储架构SQLite_ChromaDB.md](./11_双存储架构SQLite_ChromaDB.md)
**对应代码**: `playground/dual_storage_demo.py`、`app/models.py`

- **为什么需要双存储**: ChromaDB 碎片太小 + SQLite 不能语义搜索 → 互补
- **图书馆类比**: ChromaDB = 索引卡片柜，SQLite = 藏书仓库
- **ORM 模型设计**:
  - `Document` 模型：完整文档（title, content, source）
  - `DocumentChunk` 模型：切片信息（content, embedding_id, 外键）
- **两条"绳子"连接机制**:
  - 绳子① `embedding_id`: 同名字符串双向索引
  - 绳子② `metadatas`: 查询返回时直接带 document_id
- **存入流程**: SQLite 存全文+切片 → ChromaDB 存向量 → 用 embedding_id 关联
- **查询流程**: ChromaDB 快速检索 → 返回 metadatas → SQLite 回查完整上下文
- **关键澄清**: `metadatas` 标签是手动构造的，不是查库获取的
- **文本切片**: `split_text()` 函数（chunk_size + overlap 防止断句）

---

### [12_FastAPI_Chroma_最小原型.md](./12_FastAPI_Chroma_最小原型.md)
**对应代码**: `app/routers/rag.py`（早期版本）

- **从演示到 API**: demo脚本 vs 生产API的区别
- **依赖注入重构**:
  - ChromaDB 客户端作为依赖
  - Embedding 函数复用
  - 数据库会话管理
- **文档上传接口设计**:
  - 文件接收与文本提取
  - 自动切片与向量化
  - 双存储事务一致性
- **查询接口设计**:
  - 查询参数解析
  - 检索结果格式化
  - ApiResponse 统一响应格式
- **持久化配置**:
  - chroma_db/ 目录配置
  - 启动时预加载 Embedding 模型
- **lifespan 上下文管理器**: 启动/关闭钩子

---

### [13_RAG_闭环_检索到回答.md](./13_RAG_闭环_检索到回答.md)
**对应代码**: `app/routers/rag.py`

- **RAG 完整闭环流程**:
  1. 用户提问
  2. 问题向量化
  3. ChromaDB 语义检索（Top-K）
  4. 上下文拼接（带来源引用）
  5. Prompt 组装（System + Context + Question）
  6. LLM 流式调用
  7. SSE 逐字返回
- **来源引用机制**: `enumerate(start=1)` 生成 `[1]` `[2]` 引用标记
- **流式输出实现**:
  - `yield` vs `return` 的区别
  - SSE (Server-Sent Events) 格式
  - StreamingResponse 使用
- **Prompt 模板设计**:
  - 只使用提供的上下文回答
  - 不知道就说不知道
  - 标注引用来源
- **curl 测试与调试**: 流式响应验证方法

---

### [14_上下文窗口管理.md](./14_上下文窗口管理.md)
**对应代码**: `app/routers/rag.py`

- **为什么需要窗口管理**: Token 超限 = 报错/截断/幻觉
- **Token 估算方法**: tiktoken 库使用
- **三层防御策略**:
  - **第一层**: Top-K 动态调整（文档多就减少返回数量）
  - **第二层**: 相关性阈值过滤（相似度低于阈值的丢弃）
  - **第三层**: 硬截断兜底（超过 Token 限制直接截断）
- **上下文拼装优化**:
  - 按相关度排序
  - 摘要前置策略
  - 历史对话窗口裁剪
- **防幻觉设计**:
  - 明确告知"根据以下资料回答"
  - 资料不足时的拒答提示
  - 引用来源的可追溯性
- **常见坑点**: Token 计算偏差、中英文 Token 比例差异

---

### [15_LangChain核心概念.md](./15_LangChain核心概念.md)
**对应代码**: `app/routers/langchain_rag.py`

- **为什么用 LangChain**: 手搓 RAG 的痛点 vs 框架化优势
- **六大核心概念**:
  1. **Document**: 统一文档抽象（page_content + metadata）
  2. **Embeddings**: 向量化模型接口（本地/API统一抽象）
  3. **VectorStore**: 向量数据库统一接口（Chroma/Pinecone/FAISS等）
  4. **Retriever**: 检索器（相似度检索/MMR/上下文压缩）
  5. **PromptTemplate**: 提示词模板（变量注入）
  6. **LLM/ChatModel**: 大语言模型统一接口
- **LCEL 链式语法 (LangChain Expression Language)**:
  - `|` 管道符：组件像 Linux 管道一样串联
  - `RunnablePassthrough`：数据透传
  - `RunnableParallel`：并行执行
  - `StrOutputParser`：输出解析
- **ChatDeepSeek 集成**:
  - langchain-deepseek 包使用
  - reasoning_content（思维链）流式获取
  - 深度思考内容的独立展示
- **文档删除同步**: 删除Document时同步清理ChromaDB向量
- **统一API响应**: 框架化后仍保持 code/status/content 格式

---

### [16_异步编程深入.md](./16_异步编程深入.md)
**对应代码**: async 相关练习、`routers/` 中的异步路由

- **为什么需要异步**: 同步阻塞 vs 异步非阻塞（餐厅服务员类比）
- **async/await 基础语法**:
  - `async def` 定义协程函数
  - `await` 挂起等待结果
  - 协程对象 vs 实际执行
- **三种核心对象**:
  - **Coroutine**: 协程对象（待执行的菜谱）
  - **Task**: 任务（已在Event Loop中调度的协程）
  - **Future**: 未来结果占位符（Task的父类）
- **Event Loop 调度原理**:
  - 单线程并发模型
  - IO等待时切换任务
  - Future 唤醒回调机制
- **并发模式**:
  - `asyncio.gather()`: 并发执行，收集所有结果
  - `asyncio.create_task()`: 后台创建任务
  - `asyncio.as_completed()`: 按完成顺序迭代
  - `gather(return_exceptions=True)`: 异常作为值返回
- **Semaphore 限流**: 控制并发数量（防止API限流打爆）
- **常见坑点**:
  - `create_task` 不 await 会隐藏异常（"Task exception was never retrieved"）
  - 同步阻塞代码会卡住整个Event Loop
  - `run_in_executor` 是同步转异步的桥梁

---

### [17_JWT用户认证.md](./17_JWT用户认证.md)
**对应代码**: `app/routers/auth.py`、`app/models.py` (User/RevokedToken)

- **认证 vs 授权**: 你是谁 vs 你能做什么
- **密码哈希 bcrypt**:
  - 为什么不能存明文密码
  - bcrypt 哈希结构：`$2b$` + cost因子 + 22字符盐 + 31字符哈希
  - 加盐原理：相同密码不同哈希
  - bcrypt 慢哈希防暴力破解
- **JWT 令牌结构**: Header.Payload.Signature
  - Header: 算法+类型
  - Payload: 用户数据（username/role/exp）
  - Signature: HMAC-SHA256 签名防篡改
- **JWT 工作流**:
  1. 用户登录 → 验证密码 → 签发 Token
  2. 客户端请求带 `Authorization: Bearer <token>`
  3. 服务端验证签名+过期时间 → 获取用户信息
- **Depends 守卫实现**:
  - `get_current_user` 依赖：统一验票逻辑
  - 从请求头提取Token
  - 黑名单检查（RevokedToken表）
  - 用户查询与注入
- **角色守卫**: `require_admin` 依赖实现权限控制
- **登出黑名单机制**:
  - Token 无状态问题 → 黑名单补刀
  - 存 token_hash（SHA256）而非完整Token
  - expires_at 字段用于定时清理
- **Swagger 集成**: FastAPI OAuth2PasswordBearer 自动加 Authorize 按钮
- **CORS 配置**: 前端跨域访问支持
- **全局异常处理**: 兜底异常处理器防止500裸奔
- **算法白名单**: `algorithms=["HS256"]` 防算法混淆攻击（含"none"算法攻击）

---

### [18_WebSocket实时通信.md](./18_WebSocket实时通信.md)
**对应代码**: `app/routers/websocket.py`

- **HTTP vs WebSocket**:
  - HTTP: 单向、请求-响应、无状态
  - WebSocket: 双向、长连接、全双工
  - 协议升级：HTTP 101 Switching Protocols
- **FastAPI WebSocket 基础**:
  - `@app.websocket()` 装饰器
  - `await websocket.accept()` 握手
  - `await websocket.receive_text()` / `send_text()`
  - `await websocket.close()` 关闭
- **认证方案**: Query参数传递token（ws协议不方便带header）
- **ConnectionManager 连接管理**:
  - 活跃连接列表维护
  - 连接/断开事件处理
  - 广播 vs 单发
- **房间分组实现**: `dict[str, list[WebSocket]]` 真正的房间模式
- **AI 流式打断**:
  - 客户端发送"停止"消息
  - 服务端任务取消（asyncio.Task.cancel()）
  - 资源清理与状态重置
- **SSE vs WebSocket 对比**:
  - SSE: 单向（服务端→客户端）、HTTP协议、自动重连
  - WebSocket: 双向、独立协议、需要自己管理重连
  - 选型建议：AI流式输出用SSE，实时聊天/协作才用WS
- **语法坑点**: Python用`!=`而非JavaScript的`!==`

---

### [19_Alembic数据库迁移.md](./19_Alembic数据库迁移.md)
**对应代码**: `alembic/` 目录、`alembic.ini`

- **为什么需要迁移**: 改模型不会自动改表结构，开发环境与生产环境同步问题
- **迁移 vs 备份**:
  - ❌ 迁移 ≠ 备份！迁移是schema变更脚本
  - ✅ 备份是完整数据拷贝
  - 迁移表结构前先备份数据！
- **Alembic 核心概念**:
  - **revision**: 迁移版本（像Git commit）
  - **upgrade**: 升级到新版本（应用变更）
  - **downgrade**: 回滚到旧版本（撤销变更）
  - **autogenerate**: 自动对比模型生成迁移脚本
  - **head**: 最新版本
- **工作流程**:
  1. 修改 models.py
  2. `alembic revision --autogenerate -m "描述"` 生成迁移脚本
  3. 检查自动生成的脚本（autogenerate不是100%准确！）
  4. `alembic upgrade head` 应用到数据库
  5. `alembic downgrade -1` 回滚上一个版本
- **target_metadata 关键配置**: `target_metadata = Base.metadata` 必须正确指向
- **常见问题**:
  - 空迁移脚本：说明Alembic没检测到变化（检查metadata导入）
  - 空库upgrade报错：需要初始迁移包含create_table，不能只建alembic_version表
  - SQLite 限制：SQLite 不支持 ALTER TABLE 某些操作（如DROP COLUMN）
  - `server_default`: 服务端默认值（如`func.now()`），区别于Python端default
- **stamp 命令**: 标记版本号不实际执行（用于已有数据库基线）
- **迁移脚本结构**: upgrade()/downgrade() 函数对称编写

---

### [20_pytest单元测试.md](./20_pytest单元测试.md)
**对应代码**: `tests/` 目录、`tests/conftest.py`

- **为什么需要测试**: 改代码不心慌、重构有保障、bug早发现
- **Arrange/Act/Assert 三段式**:
  - Arrange: 准备测试数据和环境
  - Act: 执行要测试的操作
  - Assert: 断言结果符合预期
- **FastAPI TestClient**:
  - `TestClient(app)` 创建测试客户端
  - 与requests库相同API（get/post/put/delete）
  - 自动处理ASGI调用，不需要真的启动服务器
- **测试数据库隔离**:
  - 内存SQLite（`:memory:`）或临时文件
  - 每个测试用例新建表 → 测试完删除
  - 不污染开发数据库
- **fixture 核心概念**:
  - `@pytest.fixture` 装饰器
  - 测试用函数参数名自动注入
  - `conftest.py` 全局共享fixture
  - yield 实现setup/teardown（前置+后置清理）
- **依赖覆盖**:
  - `app.dependency_overrides[get_db] = override_get_db`
  - 替换真实数据库依赖为测试数据库
  - 注意覆盖的是同一个对象引用！
- **认证测试**:
  - 先注册/登录获取token
  - 请求头带`Authorization: Bearer <token>`
  - 未认证/权限不足的401/403测试
- **SSE 流式测试**:
  - `with client.stream(...) as response:` 上下文管理器
  - 迭代`response.iter_lines()`获取流式块
  - 判断停止条件
- **WebSocket 测试**:
  - `with client.websocket_connect(...) as websocket:`
  - `websocket.send_text()` / `receive_text()`
- **常见坑点**:
  - 空测试函数会假阳性通过（一定要有assert）
  - 异步生成器fixture的依赖覆盖对象身份问题
  - 测试顺序依赖（测试之间不该互相影响）
- **测试运行**: `pytest -v` 详细输出，`pytest test_file.py::test_func` 指定测试

---

### 额外学习资源

| 文档 | 内容 |
|------|------|
| [向量与余弦相似度](./ai学习应用数学/01_向量与余弦相似度.md) | 数学基础复习 |
| [错题本.md](./错题本.md) | 练习中记录的错题与易错点 |
| [试卷/](./试卷/) | 各章节测试卷（含补考卷） |
| [答题/](./答题/) | 答题记录与复习资料 |

---

## 🎯 学习建议

### 对于 ADHD 学习者

1. **番茄工作法**: 每学习 25 分钟休息 5 分钟
2. **动手实践**: 看完一个知识点立即写代码验证
3. **视觉化**: 利用文档中的流程图、表格帮助理解
4. **循序渐进**: 按顺序学习，不要跳步
5. **做笔记**: 用自己的话总结每个概念
6. **做习题**: 每章学完用「试卷/」里的题目自测
7. **错题复习**: 记录到「错题本.md」并定期回顾

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
- [ ] 理解双存储架构（关系库+向量库）的分工与协作
- [ ] 能说出 `collection.add()` 四个参数的作用
- [ ] 理解两条"绳子"（embedding_id + metadatas）的连接机制
- [ ] 能独立搭建完整的RAG闭环（检索→生成）
- [ ] 理解上下文窗口管理的三层防御策略
- [ ] 能用LangChain LCEL语法写出链式RAG
- [ ] 理解async/await和三种协程对象的区别
- [ ] 能实现JWT认证+角色守卫+黑名单
- [ ] 能用WebSocket实现房间广播和流式打断
- [ ] 能用Alembic进行数据库迁移和回滚
- [ ] 能用pytest写单元测试，理解fixture和依赖覆盖

---

## 🔗 代码文件对应关系

| 学习文档 | 对应代码文件 | 难度 |
|----------|-------------|------|
| 00_环境配置与PyCharm使用.md | `playground/script.py` | ⭐ |
| 01_Python基础.md | `archive/month1-python-basics/00_python_basics.py` | ⭐ |
| 02_Python进阶.md | `archive/month1-python-basics/01_python_advanced.py` | ⭐⭐ |
| 03_Python高级特性.md | `archive/month1-python-basics/02_python_advanced2.py` | ⭐⭐⭐ |
| 04_FastAPI基础.md | `archive/month1-python-basics/05_before_fastapi.py` | ⭐⭐ |
| 05_FastAPI_CRUD.md | `archive/month1-python-basics/03_crud.py` | ⭐⭐⭐ |
| 06_FastAPI_ORM_SQLAlchemy.md | `archive/month1-python-basics/04_orm.py` | ⭐⭐⭐⭐ |
| 07_代码分层与模块化架构.md | `app/main.py` + `app/models.py` + `app/database.py` + `app/routers/` | ⭐⭐⭐⭐ |
| 08_提示词工程与聊天记忆.md | `app/routers/chat_memory.py` | ⭐⭐⭐ |
| 09_RAG向量数据库入门.md | `playground/rag_demo.py` + `playground/rag_test.py` | ⭐⭐⭐⭐ |
| 10_RAG_ChromaDB向量数据库实战.md | `playground/chroma_demo.py` + `playground/chroma_real.py` + `playground/embedding_playground.py` + `app/embedding.py` | ⭐⭐⭐ |
| 11_双存储架构SQLite_ChromaDB.md | `playground/dual_storage_demo.py` + `app/models.py` | ⭐⭐⭐⭐ |
| 12_FastAPI_Chroma最小原型.md | `app/routers/rag.py` | ⭐⭐⭐⭐ |
| 13_RAG闭环_检索到回答.md | `app/routers/rag.py` | ⭐⭐⭐⭐ |
| 14_上下文窗口管理.md | `app/routers/rag.py` | ⭐⭐⭐⭐ |
| 15_LangChain核心概念.md | `app/routers/langchain_rag.py` | ⭐⭐⭐⭐ |
| 16_异步编程深入.md | `md/答题/async.md` + `app/routers/` 中的异步路由 | ⭐⭐⭐⭐ |
| 17_JWT用户认证.md | `app/routers/auth.py` + `app/models.py` (User/RevokedToken) | ⭐⭐⭐⭐ |
| 18_WebSocket实时通信.md | `app/routers/websocket.py` | ⭐⭐⭐⭐ |
| 19_Alembic数据库迁移.md | `alembic/` + `alembic.ini` | ⭐⭐⭐⭐ |
| 20_pytest单元测试.md | `tests/` + `tests/conftest.py` | ⭐⭐⭐⭐ |
| 21_Prompt_Engineering进阶.md | `app/routers/prompt.py` | ⭐⭐⭐⭐ |

> **📂 目录说明**：
> - `app/` - 核心代码区（日常开发在这里）
> - `archive/month1-python-basics/` - 第1个月Python基础练习归档
> - `playground/` - 实验/demo/试错区（随便改，不影响主线）
> - `tests/` - 单元测试

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
        result = func(*args, **kwargs)
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

### JWT 认证核心

```python
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def create_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(hours=24)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
```

---

## 🚀 下一步学习方向

完成本系列（0-20章）学习后，接下来的学习路径（已根据roadmap.sh重新规划）：

### AI 核心深入（当前优先级）
1. **prompt-advanced**: 高级提示词工程（结构化输出、采样参数、Prompt Injection边界）
2. **rag-chunking**: RAG分块策略优化、混合检索、重排序
3. **rag-evaluation**: RAG评估指标（RAGAS、Faithfulness）
4. **ai-agents**: AI Agents基础（ReAct模式、Function Calling，手动实现优先）
5. **langchain-memory & agents**: LangChain对话记忆、工具调用
6. **langgraph**: LangGraph工作流
7. **dify**: Dify平台实战（可视化对比）
8. **llm-evaluation & observability**: LLM评估、LangSmith/Langfuse可观测性

### 全栈补全（暂缓，AI核心后再做）
9. **docker-deploy**: Docker部署、CI/CD
10. **frontend-basics**: React/Vue前端基础
11. **frontend-backend**: 前后端对接

### 选修课
- 多向量数据库对比（Pinecone、Weaviate、Qdrant、FAISS）
- MCP (Model Context Protocol)
- n8n工作流自动化
- Hugging Face生态
- LlamaIndex
- Fine-tuning基础（LoRA、QLoRA）
- 多模态AI（图片理解、TTS、STT）
- AI安全与伦理

---

## 💡 遇到问题？

1. **重新阅读对应文档**: 每个文档都有详细解释和示例
2. **查看代码注释**: 源代码中有丰富的注释说明
3. **动手实验**: 修改代码，观察结果变化
4. **画流程图**: 把执行流程画出来帮助理解
5. **做章节测试**: 在「试卷/」目录下有对应测试卷
6. **查看错题本**:「错题本.md」记录了常见易错点

---

**祝你学习愉快！记住：理解 > 记忆，实践 > 阅读。**
