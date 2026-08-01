# 试卷：pytest 单元测试

- 日期：2026-06-23
- 章节：第 20 节 pytest 单元测试
- 总分：20 分
- 通过线：16 分
- 答题方式：直接在每题“我的答案”下面作答
- 注意：本试卷不附答案。命令不要求逐字背诵，概念和调用链正确即可。答完后告诉我，我会把评分、错题和最小补漏计划追加到本文件。

---

## 一、核心理解题（每题 2 分，共 8 分）

### 1. pytest 解决了什么问题？

请说明自动化测试相比每次手动点击 Swagger 或 Hoppscotch 的主要价值，并写出 pytest 判断一个测试“通过”的最基本条件。

**我的答案：**

可以批量自动化的测试后期繁杂的功能，因为你不知道你动了一个地方其他地方会不会出错，而她可以节约你点各种swagger和api测试工具的时间

---

### 2. Arrange / Act / Assert 分别是什么？

请用测试 Todo 创建接口的场景，分别说明三段各自应该做什么。

**我的答案：**

输入参数/执行函数/检查结果


---

### 3. fixture 的完整生命周期是什么？

阅读下面的结构：

```python
@pytest.fixture()
def client():
    prepare()
    with TestClient(app) as test_client:
        yield test_client
    cleanup()
```

请按执行顺序解释：

1. 哪些代码在测试前运行；
2. `yield` 时发生什么；
3. 测试函数结束后发生什么；
4. 为什么 fixture 不是中间件。

**我的答案：**

client 代码在测试的时候注入到所有使用client的函数里，在函数执行的时候打开，yield是返回一个测试app实例，测试函数结束之后client也会关闭，中间件是经过了整个https请求周期，fixture装饰器没有，但是我记得我在project/study/note/后端课程文件整理 学习的时候讲的是装饰器就是中间件，你可以帮我扫描一下这里面的讲义为我在后面解惑

---

### 4. pytest fixture 和 FastAPI `Depends` 有什么关系？

请说明它们为什么都可以叫依赖注入，以及它们分别由谁执行、运行在哪个生命周期。

**我的答案：**

他们分别是fastapi和pytest的依赖注入，但是她们属于不同的框架，一个运行在生产开发环境，一个是测试环境

---

## 二、接口与数据库题（每题 2 分，共 6 分）

### 5. 为什么测试数据库必须隔离？

请解释下面四个对象各自负责什么：

- `test_engine`
- `TestingSessionLocal`
- `override_get_db`
- `app.dependency_overrides[get_db]`

并说明如果 Todo 路由自己又定义了一个同名 `get_db()`，为什么覆盖可能失效。

**我的答案：**

1. 测试数据库引擎
2. 测试数据库会话
3. 获取测试数据库操作对象的函数
4. 替换getdb为override_get_db

---

### 6. 测试中为什么可以使用 `create_all()`？

请说明：

1. `Base.metadata.create_all(bind=test_engine)` 做了什么；
2. `drop_all()` 做了什么；
3. 为什么测试临时库可以使用它们，而正式数据库结构仍推荐由 Alembic 管理。

**我的答案：**

1. 在测试数据库创建orm模型中的表
2. 清空测试数据库
3. 因为测试数据库是测试完接着清空的，而正式数据库不是，所以建议alembic进行版本管理



---

### 7. 认证闭环应该怎么测试？

请写出注册、登录、访问 `/auth/me` 的测试调用顺序，并说明 Bearer Token 应该放在请求的什么位置。代码可以写伪代码，不要求完整可运行。

**我的答案：**
```python
def test_auth_loop(client,get_db):
    # 注册
    response = client.post("/auth/register", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    #登陆
    login_response = client.post("/auth/login", json={"username": "testuser", "password": "testpassword"})
    
    token = login_response.json()["token"]    assert token is not None
    # 访问 /auth/me
    me_response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_response.status_code == 200
    assert me_response.json()["username"] == "testuser"
```

---

## 三、流式接口与调试题（每题 2 分，共 6 分）

### 8. WebSocket 测试为什么要使用 `with`？

请解释：

```python
with client.websocket_connect("/ws/message") as websocket:
    ...
```

进入和离开 `with` 时分别发生什么。如果完全不进入 `with`，测试会缺少什么步骤？

**我的答案：**

当使用with进行ws接口连接的时候 会触发返回对象里的self方法
不使用with 返回的只是一个对象，并没有出触发连接

---

### 9. SSE mock 测试中，哪些是真实的，哪些是假的？

场景：测试通过 `monkeypatch` 替换 `generate_stream`，然后请求真实 `/ai/chat`。

请分别说明下面这些部分是真实还是模拟：

- FastAPI 路由
- 请求参数解析
- `StreamingResponse`
- `generate_stream`
- 外部 AI 模型

再解释为什么下面的断言推荐使用 `startswith()`：

```python
assert response.headers["content-type"].startswith("text/event-stream")
```

**我的答案：**

因为content-type 返回的不只有text/stream 还有其他参数startswith可以检查返回的响应头里有没有text/stream 这个参数

---

### 10. 为什么这个测试会显示 PASSED？请修正思路。

```python
def test_ai_sse(client, monkeypatch):
    async def fake_generate_stream(message: str):
        message == "测试 SSE"
        yield 'data: {"type": "answer"}\n\n'

        monkeypatch.setattr(
            ai_router_module,
            "generate_stream",
            fake_generate_stream,
        )

        with client.stream(
            "POST",
            "/ai/chat",
            json={"message": "测试 SSE"},
        ) as response:
            assert response.status_code == 500
```

请指出至少三个问题，并说明 pytest 为什么可能把它判定为通过。不要求抄完整代码，但要说明正确缩进和断言应该放在哪里。

**我的答案：**

message 判定有问题？ 然后底下不应该等于500 而是要先进行decode转换utf8，验证status_code === 200

---

## 自评区

答完后先自己标记：

- [ ] 我能解释 pytest 的价值和 Arrange / Act / Assert
- [ ] 我能解释 fixture、`yield`、`with` 的生命周期
- [ ] 我能解释 fixture 与 `Depends` 的相同点和边界
- [ ] 我能解释测试数据库隔离和 dependency override
- [ ] 我能测试认证、WebSocket 和 SSE 的最小闭环
- [ ] 我能识别“pytest 绿色但断言没有执行”

---

## 批改区

> 等用户答完后追加评分、错题、弱点和最小补漏计划。

---

## 批改结果（2026-06-23）

### 总分

- 得分：12.3 / 20
- 通过线：16 / 20
- 结果：暂未通过，需要回炉关键关卡后补考

这次呈现出很清楚的特点：你已经能把 pytest、fixture、WebSocket 和 SSE 测试实际跑通，但文字回答容易只答一个方向，漏掉题目要求的生命周期、对象身份和真实/模拟边界。代码能力已经起步，概念表达还没有达到通关线。

### 逐题评分

| 题号 | 得分 | 批改 |
|---|---:|---|
| 1 | 1.5 / 2 | 自动化、回归检查和节约手测时间回答正确；漏了最基本通过条件：测试函数执行完且没有未处理异常或失败断言。 |
| 2 | 1.5 / 2 | “输入参数/执行函数/检查结果”方向正确；题目要求结合 Todo 场景，应具体写准备 JSON、POST `/todos/`、断言状态码和响应体。 |
| 3 | 1.4 / 2 | 知道 fixture 按需注入、TestClient 打开和关闭，也能区分中间件处理 HTTP 周期；`yield` 不是返回 app，而是暂停 fixture 并把 `test_client` 交给测试，测试后还会恢复执行 cleanup。 |
| 4 | 1.2 / 2 | 知道两者分别属于 pytest 和 FastAPI 的依赖注入；漏了 pytest fixture 围绕测试函数运行，`Depends` 由 FastAPI 在每次请求解析依赖时运行。 |
| 5 | 1.1 / 2 | 四个对象的方向基本正确；漏了隔离是为了防止测试污染正式数据，也漏了同名函数仍是不同对象，覆盖字典必须使用路由登记的同一个 `get_db`。 |
| 6 | 1.7 / 2 | `create_all` 和正式库/Alembic 的边界正确；`drop_all()` 是删除 metadata 中的表，不只是清空表内数据或删除数据库文件。 |
| 7 | 1.3 / 2 | 注册→登录→Bearer Token→`/auth/me` 的主流程正确；本项目字段是 `access_token`，不需要额外注入 `get_db`，代码里 token 赋值和 assert 也需要换行。 |
| 8 | 1.3 / 2 | 知道不进入 `with` 只得到会话对象、没有真正连接；应准确说进入调用 `__enter__` 完成握手，离开调用 `__exit__` 关闭连接和释放资源。 |
| 9 | 0.7 / 2 | 回答了响应头可能还有附加参数，因此使用 `startswith`；漏答主体：路由、参数解析、StreamingResponse 真实，`generate_stream` 和外部模型调用被模拟/跳过。准确媒体类型是 `text/event-stream`。 |
| 10 | 0.6 / 2 | 注意到比较和状态码有问题，但漏掉最核心原因：请求和断言缩进在未调用的假生成器中，外层测试只定义函数后正常结束，所以 pytest 判定通过；Python 应用 `==`，不是 `===`，`message == ...` 前还缺 `assert`。 |

### 三个关键弱点

#### 1. 生命周期调用链没有完全说清

```text
pytest 发现测试参数 client
→ 执行 fixture 到 yield
→ yield 把 TestClient 交给测试并暂停 fixture
→ 执行整个测试函数
→ 回到 yield 后继续
→ 离开 with，关闭 TestClient
→ cleanup / drop_all
```

fixture 不是中间件：fixture 包围测试函数；中间件包围每一次 HTTP 请求和响应。

#### 2. 同名依赖不等于同一对象

```text
database.get_db       → 函数 A
router 自己的 get_db  → 函数 B
```

即使名字和代码相同，`A is B` 仍然是 `False`。`dependency_overrides` 必须以路由登记的原函数对象为键。

#### 3. 流式测试的真实/模拟边界和空测试

SSE mock 测试中：

```text
真实：FastAPI app、/ai/chat、参数解析、StreamingResponse、状态码、响应头
模拟：generate_stream 返回内容
未调用：外部 AI 模型
```

pytest 的 `PASSED` 只说明测试函数没有抛异常。只有定义假函数却没有执行请求和断言，依然会绿色通过。

### 旧讲义扫描：装饰器是不是中间件？

扫描了 `/Users/enkidu/project/study/note/后端课程文件整理` 中的 Markdown，没有找到“装饰器就是中间件”或两者等同的原句。

旧讲义实际表达的是：

- NestJS 使用 `@Controller`、`@Get` 等装饰器登记路由和元数据；
- TypeScript 装饰器也可以用于 AOP、Guard、Interceptor 等机制的声明；
- Middleware 是请求处理链中的一个实际执行层，自动拦截流经系统的请求。

因此容易产生的误解是“框架用装饰器登记中间件/守卫，所以装饰器就是中间件”。准确关系是：

```text
装饰器 = 登记、包装或添加元数据的语法机制
中间件 = HTTP 请求/响应链中的运行组件
装饰器可以用于登记某个组件，但装饰器本身不是中间件
```

### 最小补漏计划

不重写整章，只回炉三组内容：

1. 用一条时间线复述 fixture、`yield`、`with`、cleanup。
2. 用函数 A/B 解释 `dependency_overrides` 为什么要求同一对象。
3. 重做 SSE 真/假分类和空测试改错题。

完成后进行 5 题补考，覆盖以上三组弱点；通过后再把 pytest 阶段标记为完成。
