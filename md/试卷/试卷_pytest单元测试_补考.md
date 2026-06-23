# 补考试卷：pytest 单元测试

- 日期：2026-06-23
- 对应章节：第 20 节 pytest 单元测试
- 对应初考：`试卷_pytest单元测试.md`
- 总分：10 分
- 通过线：8 分
- 答题方式：直接在每题“我的答案”下面作答
- 注意：本卷只补初考弱点，不附答案。答完后告诉我，我会把评分和最终阶段判断追加到本文件。

---

## 一、生命周期与边界（每题 2 分，共 4 分）

### 1. 请完整排列 fixture 的执行顺序

阅读代码：

```python
@pytest.fixture()
def client():
    Base.metadata.create_all(bind=test_engine)
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
```

请从 pytest 发现 `test_create_todo(client)` 开始，按顺序说明：

1. 测试前执行什么；
2. `yield` 做什么；
3. 测试函数什么时候执行；
4. 测试结束后如何关闭和清理。

**我的答案：**

如果测试函数有client就会先去找 带有fixture装饰器的client函数，找到之后先执行这个函数，创建测试数据库表，替换获取数据库的方法，with 打开 TestClinet（app）返回 testclient，测试函数在拿到client的时候执行，执行结束之后复原，原来的数据库会话实例获取方法，然后清空test.db里Base.metadata中相关的表

---

### 2. fixture、装饰器、中间件、Depends 分别是什么？

请分别用一句话说明下面四项的职责，并指出它们运行在“测试生命周期”还是“HTTP 请求生命周期”：

- `@pytest.fixture()`
- Python/TypeScript 装饰器
- HTTP Middleware
- FastAPI `Depends`

**我的答案：**

fixture 将函数登记为测试需要的依赖，运行在测试函数前后
装饰器函数执行前后添加行为，运行在导入定义或者框架等级时
http中间件负责拦截处理http请求和相应，运行在每次请求期间
Depends是fastapi的依赖注入，运行在fastapi请求函数的前后

---

## 二、依赖覆盖（2 分）

### 3. 为什么同名 `get_db` 仍可能导致覆盖失效？

场景：

```python
# database.py
def get_db():
    ...

# routers/todos_routers.py
def get_db():
    ...

# conftest.py
app.dependency_overrides[database.get_db] = override_get_db
```

请说明：

1. 为什么 Todo 路由仍可能访问正式数据库；
2. `dependency_overrides` 是按函数名字还是函数对象匹配；
3. 应该如何修正。

**我的答案：**

因为在文件里定义了一个本地的getdb，会覆盖在测试函数里覆盖的

---

## 三、SSE 与调试（每题 2 分，共 4 分）

### 4. SSE mock 测试的真实与模拟边界

测试通过 `monkeypatch` 将 `routers.ai_router.generate_stream` 替换为固定假流，然后请求 `/ai/chat`。

请把下面项目分成“真实执行”“被模拟”“完全没有调用”三类：

- FastAPI app
- `/ai/chat` 路由
- `ChatRequest` 参数解析
- `StreamingResponse`
- `generate_stream`
- 外部 AI 模型
- HTTP 状态码和 `Content-Type`

最后说明为什么 `Content-Type` 推荐使用：

```python
startswith("text/event-stream")
```

**我的答案：**

1. 真实执行
2. 真是执行
3. 完全没有调用
4. 真是执行
5. 被模拟
6. 完全没有调用
7. 真实执行

因为可以从返回的响应头content-type里的多个字段里准确的检查出开头是不是text/event-stream，防止有多个字段的变体，没必要完全相等

---

### 5. 识别“绿色空测试”

下面代码为什么可能显示 `PASSED`？请指出至少三个问题，并写出正确的缩进结构。

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

不要求写完整可运行代码，但必须说明：

- 哪些代码应该向左缩进；
- `message == ...` 应该如何处理；
- pytest 为什么会把原代码判定为通过。

**我的答案：**

因为不执行 if 条件里面的语句也可能是 

1. yield 后面的缩进有问题
2. 使用模拟数据 assert == 500 不可能成功
3. fake_generate_stream没必要加判断条件，因为测试写死了

```python
def test_ai_sse(client, monkeypatch):
    async def fake_generate_stream(message: str):
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

---

## 自评区

- [ ] 我能完整复述 fixture 的准备、暂停、恢复和清理
- [ ] 我能区分装饰器、fixture、Middleware 和 Depends
- [ ] 我知道 dependency override 按函数对象匹配
- [ ] 我能区分 SSE 测试里的真实、模拟和未调用部分
- [ ] 我能识别没有真正执行断言的绿色测试

---

## 批改区

> 等用户答完后追加补考得分、弱点和最终阶段判断。

---

## 补考批改结果（2026-06-24）

### 总分

- 得分：7.0 / 10
- 通过线：8 / 10
- 结果：暂未通过，但已从“概念整体不稳”缩小到两个明确缺口
- 阶段判断：`pytest` 继续保持 `in_progress`

这次比初考清楚很多：fixture 生命周期、装饰器/中间件边界、SSE 的大部分真/假分类已经可以使用。没有通过主要不是因为整章不会，而是第 3 题漏答函数对象匹配，第 5 题仍没说出空测试的准确执行链。

### 逐题评分

| 题号 | 得分 | 批改 |
|---|---:|---|
| 1 | 1.8 / 2 | 顺序基本完整：按参数找 fixture、建表、覆盖依赖、进入 TestClient、执行测试、恢复依赖、删表。再补一句“`yield` 暂停 fixture，测试结束后从 yield 后恢复，并退出 with 关闭 TestClient”即可满分。 |
| 2 | 1.7 / 2 | 四项边界基本正确。装饰器不只是在执行前后加行为，也可能只登记元数据；`Depends` 是在每次 HTTP 请求解析依赖时执行，而不是泛称“请求函数前后”。 |
| 3 | 0.6 / 2 | 知道问题来自路由本地 `get_db`，但没有回答核心：override 按函数对象匹配，不按名字；`database.get_db` 和路由本地 `get_db` 是 A/B 两个对象。修正方式是路由统一导入公共 `database.get_db`，或覆盖路由实际登记的那个对象。 |
| 4 | 1.6 / 2 | 其余分类正确，`startswith` 原因也正确；`ChatRequest` 参数解析是真实执行，不是完全没有调用。假流只替换 `generate_stream`，请求 JSON 仍由真实 Pydantic 模型解析。 |
| 5 | 1.3 / 2 | 已发现缩进问题，并把 monkeypatch 和请求左移到外层测试函数；但“if 条件”不存在。原代码通过的准确原因是：外层测试只定义 `fake_generate_stream` 后正常结束，假生成器没有被调用，所以内部 monkeypatch、请求和错误的 500 断言全部没有执行。修正后的代码仍写 `status_code == 500`，真正运行时会失败。 |

### 剩余两个缺口

#### 1. dependency override 按对象身份匹配

```text
database.get_db       → 函数对象 A
router 本地 get_db    → 函数对象 B

dependency_overrides[A] 不会替换 Depends(B)
```

正确规则：

```text
Depends() 登记哪个函数对象，dependency_overrides 的键就必须是哪个对象。
```

#### 2. 空测试通过的真实执行链

原代码的真实执行过程只有：

```text
进入 test_ai_sse
→ 定义 fake_generate_stream
→ 到达测试函数末尾
→ 没有异常、没有失败断言
→ PASSED
```

没有发生：

```text
没有 monkeypatch
没有请求 /ai/chat
没有执行 status_code == 500
```

### 最小补漏结论

不需要再复习整章。只需能独立回答：

1. 为什么两个同名函数仍是 A/B 两个对象，override 应该覆盖谁；
2. 为什么把请求和断言缩进进未调用的假函数后，pytest 会显示绿色。

这两个点确认后，再做一次极短的二次补考即可完成 pytest 阶段。
