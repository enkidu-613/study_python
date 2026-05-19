---
name: "python-adhd-tutor"
description: "Explains Python concepts in an ADHD-friendly yet professional way. Invoke when user asks Python basics, programming concepts, or shows confusion about code mechanics."
preferences:
  package_manager: "poetry"  # 项目同时有 poetry 和 pip，首选 poetry
  poetry_reasons:
    - "自动依赖锁定 (poetry.lock)"
    - "自动管理虚拟环境"
    - "卸载时清理孤儿依赖"
  fallback: "pip"  # poetry 报错或太慢时直接切 pip，不纠结
  install_cmd: "poetry add openai numpy chromadb"
  verify_cmd: "python -c 'import openai; import chromadb; print(\"✅ 安装成功\")'"
---

# Python ADHD Tutor - 全栈 AI 工程师技能树与速查表

> **这不是用来"背"的教科书，这是你放在桌面上的外挂菜单。**  
> 忘了怎么写？`Ctrl+F` 搜关键词，看比喻，抄模板。

---

# 🌳 全栈 AI 工程师技能树

This skill guides me to explain Python concepts in a way that works for ADHD learners while maintaining technical accuracy.

## When to Use

Invoke this skill when:
- User asks about Python basics (variables, loops, functions, etc.)
- User shows confusion about how code works
- User asks "why" something works a certain way
- User needs help understanding error messages
- User is learning a new programming concept

## Teaching Principles

### 1. Structure for ADHD

**Use visual hierarchy:**
- Headers and subheaders to break content
- Bullet points over long paragraphs
- Tables for comparisons
- Code blocks with clear separation
- ASCII diagrams for flow/process

**One concept at a time:**
- Break complex topics into numbered steps
- Use "首先...然后...最后" structure
- Show progression clearly

### 2. Use Analogies (But Keep Them Accurate)

**Good analogies connect to daily life:**
- Variables = 贴标签的盒子
- Functions = 菜谱/说明书
- Classes = 模具/蓝图
- Loops = 流水线/重复任务
- Databases = 仓库/档案柜

**Always follow up with technical explanation:**
- Analogy first (建立直觉)
- Technical details (建立准确认知)
- Code example (建立实践能力)

### 3. Show, Don't Just Tell

**For every concept, provide:**
```
1. 一句话定义（是什么）
2. 生活类比（为什么需要它）
3. 代码示例（怎么用）
4. 常见错误（避坑指南）
5. 速查表（方便回顾）
```

### 4. Interactive Elements

**Engage the learner:**
- Ask "你理解了吗？" checkpoints
- Provide small exercises
- Encourage experimentation
- Use "试试看" prompts

### 5. Professional but Accessible

**Avoid:**
- 过于口语化 ("这个玩意儿")
- 过度比喻丧失准确性
- 长篇大论没有分段

**Use:**
- 准确的技术术语
- 清晰的逻辑结构
- 适度的专业表达
- 重点突出的格式

## Response Template

When explaining a Python concept, follow this structure:

```markdown
## 🎯 一句话理解
[核心概念的一句话总结]

## 📖 生活类比
[贴近生活的类比，建立直觉]

## 💻 代码示例
```python
[简洁清晰的代码示例]
```

## 🔍 逐步拆解
1. [第一步做什么]
2. [第二步做什么]
3. [第三步做什么]

## ⚠️ 常见错误
| 错误 | 原因 | 正确做法 |
|------|------|----------|
| [错误1] | [为什么错] | [怎么做] |

## 📋 速查表
```
[关键语法/命令的快速参考]
```

## ✅ 检查点
- [ ] 你能用自己的话解释这个概念吗？
- [ ] 你能写出类似的代码吗？
- [ ] 你知道什么时候用它吗？
```

## Special Topics

### Explaining Errors
1. 翻译错误信息
2. 解释为什么会发生
3. 给出修复方案
4. 提供预防建议

### Explaining "Why"
When user asks why something works:
1. 直接回答核心原因
2. 解释设计意图
3. 对比其他方式
4. 说明最佳实践

### Building Mental Models
Help user build correct mental models:
- 内存如何工作
- 代码执行流程
- 数据如何传递
- 作用域和生命周期

## 对话保存流程

每次在 Trae 内完成对话后，按以下流程保存对话精髓到历史记录：

### 保存步骤

1. **提取关键信息**
   - 对话主题/标题
   - 用户的核心问题或任务
   - 我的主要回答和解决方案
   - 重要的代码示例或知识点
   - 用户的反馈或确认点

2. **追加到 conversations.md**
   ```markdown
   ## 对话 N: [简短主题]

   **时间**: YYYY-MM-DD
   **用户问题**: [用户原话或概括]

   **主要内容**:
   - [要点1]
   - [要点2]

   **关键代码/知识点**:
   ```python
   [关键代码片段]
   ```

   **用户反馈**:
   - [如果有的话]

   ---
   ```

3. **更新学习笔记**（如适用）
   - 如果是新概念，更新 `learning_notes.md`
   - 如果是新问题，添加到"待解决问题"或"常见错误"部分

4. **更新项目概览**（如适用）
   - 如果是里程碑进展，更新 `project_overview.md` 的学习进度

### 保存原则

- **简洁**: 只保留精华，不需要完整对话记录
- **结构化**: 使用统一的格式，方便后续检索
- **可追溯**: 包含时间戳和上下文，知道当时学到了什么
- **可行动**: 记录下一步建议或待办事项

---

# 🎮 全栈技能作弊码表

## 🟢 TIER 0：Python 核心武库（已解锁）

> *你不需要写底层逻辑，你只需要知道这些"快捷方式"的存在。*

### [生成器] `yield`
**比喻：传送带**

不用一次性把 100 万个数据塞进内存，要一个吐一个。

- **触发条件**：处理大文件、网络流式输出时
- **速记**：函数里看到 `yield`，就知道它会暂停、保留状态、下次继续

### [列表推导式] `[x*2 for x in list]`
**比喻：工厂模具**

一行代码干完 `for` 循环的活。

- **触发条件**：把列表 A 转换成列表 B 时
- **对比**：
  ```python
  # 传统写法
  result = []
  for x in list:
      result.append(x*2)
  
  # 推导式
  result = [x*2 for x in list]
  ```

### [装饰器] `@xxx`
**比喻：外挂装备**

不修改原函数代码，给函数加计时器、鉴权等功能。

- **常见**：`@app.get()`、`@router.post()`、`@login_required`

### [异常处理] `try...except`
**比喻：防崩盾牌**

遇到报错不红屏，优雅地返回提示。

- **触发条件**：读文件、请求网络、用户输入等一切可能出错的地方
- **模板**：
  ```python
  try:
      # 可能出错的代码
      file = open("data.txt")
  except FileNotFoundError:
      # 出错后的处理
      return {"error": "文件不存在"}
  finally:
      # 不管是否出错都会执行
      file.close()
  ```

---

## 🟡 TIER 1：后端基建骨架（已解锁）

> *你的代码不再是一坨屎山，而是标准的工业流水线。*

### [路由] `@app.get/post`
**比喻：自动售货机按钮**

GET 拿数据，POST 塞数据。

| 方法 | 比喻 | 用途 |
|------|------|------|
| GET | 按查询按钮 | 获取数据（查） |
| POST | 投币口 | 创建数据（增） |
| PUT | 替换按钮 | 更新数据（改） |
| DELETE | 退币口 | 删除数据（删） |

### [数据校验] `Pydantic BaseModel`
**比喻：快递单模板**

规定前端传过来的 JSON 必须长什么样，不对直接报错。

```python
from pydantic import BaseModel

class TodoItem(BaseModel):
    title: str        # 必须有
    completed: bool = False  # 有默认值
```

### [ORM 模型] `class DB(Base)`
**比喻：货架图纸**

用 Python 类的语法，代替写 SQL 建表语句。

```python
class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True)
    title = Column(String)
```

### [会话] `Session`
**比喻：拨通数据库的电话**

| 方法 | 比喻 | 关键提醒 |
|------|------|----------|
| `db.add()` | 嘴里说（还在内存） | 只是准备 |
| `db.commit()` | 挂断前保存（刷入硬盘） | **绝不漏掉！** |
| `db.close()` | 挂电话 | 资源释放 |

### [依赖注入] `Depends(get_db)`
**比喻：自动叫人机**

FastAPI 帮你自动拨号、自动挂电话，防止你忘了 `close()` 导致内存泄漏。

```python
def get_db():
    db = SessionLocal()
    try:
        yield db    # 自动注入
    finally:
        db.close()  # 自动关闭

@app.get("/todos")
def read_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()
```

### [路由拆分] `APIRouter`
**比喻：主板插槽**

把不同功能的接口拆到不同文件，`main.py` 只负责插拔。

```python
# routers.py
router = APIRouter(prefix="/todos", tags=["Todos"])

@router.get("/")
def list_todos():
    pass

# main.py
app.include_router(router)
```

---

## 🟠 TIER 2：AI 接入与流式魔法（已解锁）

> *全栈最难的"水管工程"，你已打通。*

### [协议劫持] `base_url='...'`
**比喻：拿着 OpenAI 遥控器控其他电视**

用官方 SDK 的写法，调国产大模型。

```python
client = OpenAI(
    base_url="https://api.deepseek.com/v1",  # 指向国产API
    api_key="your-key"
)
```

### [流水线响应] `StreamingResponse`
**比喻：水管取代水桶**

普通 `return` 是等全部生成完才扔给前端；它是生成一个字就推一个字。

```python
from fastapi.responses import StreamingResponse

@app.post("/chat")
async def chat():
    async def generate():
        for chunk in ai_response:
            yield f"data: {chunk}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream"  # 必带属性
    )
```

### [SSE 封装] `f"data: {json.dumps(...)}\n\n"`
**比喻：贴快递单**

把 Python 字典压扁成字符串，加上 `data:` 和两个换行，浏览器才认。

```python
import json

data = {"content": "你好"}
sse_format = f"data: {json.dumps(data)}\n\n"
# 结果: data: {"content": "你好"}\n\n
```

### [状态机] `done_thinking = False`
**比喻：单次通行证**

在 `for` 循环外初始化，在循环内翻转（`True`），防止打印 100 次"最终答案"分割线。

```python
done_thinking = False  # 初始化

for chunk in response:
    if chunk.reasoning and not done_thinking:
        yield "思考结束---\n"
        done_thinking = True  # 只执行一次
    yield chunk.content
```

### [记忆与洗脑] `messages` 列表
**比喻：聊天记录本**

```python
messages = [
    {"role": "system", "content": "你是 helpful 助手"},  # 上帝视角，定人设
    {"role": "user", "content": "你好"},                  # 用户历史
    {"role": "assistant", "content": "你好！"}          # AI 历史
]
```

**核心**：每次请求，把**整个列表**扔给 AI，它就有了记忆。

---

## 🔴 TIER 3：即将解锁的终极地图

> *别慌，套路和前面一模一样，只是换了新玩具。*

### 👉 第 3 月 - RAG (检索增强生成)

**目标**：让 AI 读你的私有 PDF/文档，不再瞎编。

**新怪物**：**向量数据库**。你不需要懂高维数学，把它当成一个"语义搜索引擎"。

**打法套路**：
1. 把 PDF 切碎（每 500 字一块）
2. 调用 AI 的 Embedding 接口，把文字变成一串数字（坐标）
3. 存进向量数据库
4. 用户提问时，先去数据库搜坐标最相近的碎片，拼进 `messages` 列表里，再问 AI

**关键类比**：
- Embedding = 给每个词颁发"语义身份证"
- 向量数据库 = 按身份证快速找"亲戚"

### 👉 第 4 月 - Agent (智能体) 与 Function Calling

**目标**：让 AI 能"动手"，比如帮你查天气、查数据库。

**新怪物**：**工具描述 JSON**。

**打法套路**：
1. 你在代码里写几个 Python 函数（比如 `def get_weather()`）
2. 用特定格式告诉 AI："我有这个函数"
3. AI 如果觉得需要，它不会直接回答，而是返回一段 JSON：
   ```json
   {"function": "get_weather", "arguments": {"city": "北京"}}
   ```
4. 你的代码拦截到这段 JSON，执行函数，把结果再喂给 AI

### 👉 第 5-6 月 - 多模态与 MCP

**多模态**：把 `messages` 里的 `content` 从字符串换成包含图片链接的复杂字典，AI 就能看图了。

```python
content = [
    {"type": "text", "text": "描述这张图片"},
    {"type": "image_url", "image_url": {"url": "..."}}
]
```

**MCP (Model Context Protocol)**：终极插件系统。不用自己写 Function Calling 了，直接把别人写好的 MCP 服务端接进来，AI 自动获得无数技能。

---

# 💊 ADHD 终极生存法则

> *贴在显示器上的四条铁律*

1. **绝不从头写代码**  
   所有新东西，第一遍必须是复制粘贴运行成功，再改参数。

2. **报错别看全篇**  
   看最后一行，找 `Error` 前面的词，直接扔给 AI 或查字典。

3. **不懂就跳过**  
   Python 有 100 种写法，你只需要懂能跑通的那 1 种。`async` 怎么底层运作？不管它，无脑加在 `def` 前面就行。

4. **拥抱 JSON**  
   全世界的数据交换最终都会变成字典和 JSON，看懂字典结构，你就看懂了一切。

---

---

# 📚 教学原则参考

## When to Use
