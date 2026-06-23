# 二次补考试卷：pytest 单元测试

- 日期：2026-06-24
- 对应章节：第 20 节 pytest 单元测试
- 总分：5 分
- 通过线：4 分
- 答题方式：直接在每题“我的答案”下面作答
- 注意：本卷只考最后两个缺口，不附答案。通过后即可判定 pytest 阶段完成。

---

## 1. dependency override 与函数对象（2 分）

项目中有两个同名函数：

```python
# database.py
def get_db():       # 函数对象 A
    ...

# routers/todos_routers.py
def get_db():       # 函数对象 B
    ...

@router.post("/")
def create_todo(db=Depends(get_db)):
    ...
```

测试配置为：

```python
app.dependency_overrides[database.get_db] = override_get_db
```

请完整回答：

1. `Depends(get_db)` 在这里登记的是函数 A 还是函数 B？
2. `dependency_overrides` 按函数名字还是函数对象匹配？
3. 为什么测试仍可能连接正式数据库？
4. 写出一种正确修正方式。

**我的答案：**

1. 函数b
2. 是按照函数对象匹配
3. 因为名字一样，但是函数a ！= 函数b，覆盖的只是函数a的对象没有覆盖函数b的
4. 删除 路由本地的getdb，换成从database导入的

---

## 2. async generator 与绿色空测试（3 分）

阅读代码：

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

请完整回答：

1. pytest 调用外层 `test_ai_sse()` 后，实际执行了哪些代码？
2. 为什么错误的 `assert response.status_code == 500` 没有让测试失败？
3. 调用 `fake_generate_stream(...)` 后，为什么函数体还不一定开始执行？还需要什么操作？
4. `yield` 后面的代码什么时候才可能继续执行？
5. `monkeypatch` 和 `client.stream()` 正确的缩进位置在哪里？

**我的答案：**

1. 定义了fake，然后什么没有执行
2. 因为缩进错误在fake里面，fake没有被anext 或者async for 执行
3. 因为fake是一个生成器函数 需要anext 或者 async for才能让他执行下一步，这样只会返回一个生成器对象
4. 在调用第二次anext 或者使用async for的时候
5. 和async def fake 同级

---

## 自评区

- [ ] 我知道 override 按函数对象身份匹配
- [ ] 我能说清空测试真实执行了什么、没有执行什么
- [ ] 我知道调用异步生成器只创建对象，迭代才执行
- [ ] 我知道下一次 `anext()` 才会从 `yield` 后继续

---

## 批改区

> 等用户答完后追加得分和 pytest 阶段最终判断。

---

## 二次补考批改结果（2026-06-24）

### 总分

- 得分：5 / 5
- 通过线：4 / 5
- 结果：通过
- 阶段判断：pytest 单元测试阶段完成

### 逐题评分

| 题号 | 得分 | 批改 |
|---|---:|---|
| 1 | 2 / 2 | 完整指出 `Depends` 登记函数 B、override 按函数对象匹配、A/B 不同导致覆盖失效，并给出路由统一导入公共 `database.get_db` 的正确修正。 |
| 2 | 3 / 3 | 完整说明外层测试只定义 fake 后结束；错误断言因位于未执行的 fake 内而没有运行；调用异步生成器只返回对象，需 `anext`/`async for` 才执行；下一次 `anext` 从 `yield` 后继续；monkeypatch 和请求应与 `async def fake` 同级。 |

### 最终掌握结论

以下两个初考弱点已经补齐：

```text
Depends 登记谁，dependency_overrides 就必须以同一个函数对象为键。
```

```text
调用异步生成器只创建对象；迭代才执行，下一次迭代从 yield 后继续。
```

你已经能够识别 pytest 的“绿色空测试”，并能解释它为什么没有执行请求和断言。结合此前项目测试 `8 passed`，本章达到可用和可继续推进的标准。
