# 09 · Flask 与 Web 应用：把请求接到 Python 和数据库

> David J. Malan / CS50 团队，Harvard University
>
> 非官方中文改编，依据 Harvard CS50x 当前课程资料编写；原课程资料许可为 CC BY-NC-SA 4.0。本文件不是 Harvard 官方翻译或课程材料。使用与改编说明见[本目录来源与许可](来源与许可.md)。

上一章的浏览器只过滤自己那张静态页面里的三行文档。现在让浏览器把请求送到 Python 服务器，服务器读取/写入一份隔离的 SQLite 演示数据库，再返回 HTML。业务背景仍是知识文档目录，不碰用户真实应用和数据库。

## 本章学什么

- Flask 应用实例、route 装饰器、请求上下文及 GET/POST 表单数据的真实调用方式。
- Jinja 模板、状态码、重定向与 `url_for` 的职责。
- SQLite 参数化查询、每请求一个连接及连接关闭的生命周期。
- Cookie、Flask session、签名与授权之间的边界，以及 CSRF 风险。
- 不启动监听服务，用 Flask `test_client` 离线验证 GET、POST、400、404 和 session。

本章不做真实密码认证、多用户注册、生产部署、迁移系统、后台任务或异步应用。登录选项是明确标记的演示身份切换，不是安全登录。官方课还讲 HTTP server、Frosh IMs、购物车、Shows、API、JSON 与 AJAX；本章讲清服务器请求/响应和 SQL 模型，末尾补充 API/JSON/AJAX 的接口边界，不实现对外网络调用。

## 依赖隔离与文件

Flask 是 Python 第三方 Web 微框架，PyPI 依赖名为 `Flask`。它提供请求路由、请求/响应对象和模板渲染；它不替你设计数据库 schema、验证用户权限或保证部署安全。适合小型 Python Web 服务；只需静态网页时不需要 Flask，重型异步/大型系统可按需求评估其他框架。

本章只使用练习目录里的独立 `.venv-flask`，不改 Poetry 项目依赖或全局 Python：

```bash
cd examples/cs50x
poetry run python -m venv .venv-flask
.venv-flask/bin/python -m pip install 'Flask>=3.1,<4'
```

Windows 上请使用该虚拟环境中对应的 `Scripts/python.exe`。安装只进入当前练习目录的虚拟环境，不改项目 `pyproject.toml` 或 lockfile。`unittest` 是 Python 标准库测试框架：`TestCase` 用来组织测试，`setUp` 在每个测试前准备独立状态，`tearDown` 在测试结束后清理，`assertEqual` 等断言在结果不符时让测试失败，`unittest.main()` 是命令行测试运行器。运行测试时注入仅供测试的临时密钥：

```bash
FLASK_SECRET_KEY=test-only-temporary-key .venv-flask/bin/python -m unittest -v test_app.py
```

运行本地服务器（仅本机 loopback 地址，不开放局域网/公网）：

```bash
export FLASK_SECRET_KEY="$(.venv-flask/bin/python -c 'import secrets; print(secrets.token_hex(32))')"
.venv-flask/bin/python -m flask --app app run --host 127.0.0.1
```

Windows PowerShell 可用 `.venv-flask/Scripts/python.exe -c "import secrets; print(secrets.token_hex(32))"` 生成值并赋给 `$env:FLASK_SECRET_KEY`。服务只绑定 `127.0.0.1` 且关闭 debug，不使用 `0.0.0.0`。

## 完整应用：`app.py`

保存为 `examples/cs50x/app.py`。为了不依赖缺失的模板文件，最小演示把模板字符串内嵌；下一节会说明真实项目应如何拆到 `templates/`。

```python
import os
import sqlite3
from flask import Flask, abort, g, jsonify, redirect, render_template_string, request, session, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY")
if not app.config["SECRET_KEY"]:
    raise RuntimeError("请先设置随机的 FLASK_SECRET_KEY 环境变量")
app.config["DATABASE"] = os.path.join(app.instance_path, "cs50x-notes-demo.sqlite3")

INDEX_TEMPLATE = """
<!doctype html>
<html lang="zh-CN">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>知识文档目录</title></head>
<body>
  <h1>知识文档目录</h1>
  {% if user_id %}
    <p>当前演示身份：owner {{ user_id }}</p>
    <form action="{{ url_for('logout') }}" method="post">
      <button type="submit">退出</button>
    </form>
    <form action="{{ url_for('add_document') }}" method="post">
      <label for="title">新增文档标题</label>
      <input id="title" name="title" required maxlength="80">
      <button type="submit">新增</button>
    </form>
    <p>待读文档 ID：{{ session.get('reading_list', [])|join(', ') }}</p>
  {% else %}
    <p>先选择一个演示身份。此切换不验证真实身份。</p>
    <form action="{{ url_for('login') }}" method="post">
      <label for="user_id">演示 owner ID（7 或 9）</label>
      <input id="user_id" name="user_id" inputmode="numeric" required>
      <button type="submit">切换身份</button>
    </form>
  {% endif %}
  <form action="{{ url_for('index') }}" method="get">
    <label for="q">按标题筛选</label>
    <input id="q" name="q" value="{{ query }}">
    <button type="submit">搜索</button>
  </form>
  <p>匹配 {{ documents|length }} 条。</p>
  <ul>
    {% for document in documents %}
      <li>
        {{ document['id'] }} · {{ document['title'] }} · owner {{ document['owner_id'] }}
        {% if user_id %}
          <form action="{{ url_for('add_to_reading_list') }}" method="post">
            <input type="hidden" name="document_id" value="{{ document['id'] }}">
            <button type="submit">加入待读</button>
          </form>
        {% endif %}
      </li>
    {% else %}
      <li>没有匹配的文档。</li>
    {% endfor %}
  </ul>
  <section aria-labelledby="api-heading">
    <h2 id="api-heading">JSON 接口预览</h2>
    <button id="load-api" type="button">读取文档 JSON</button>
    <p id="api-status" aria-live="polite"></p>
    <pre id="api-result"></pre>
  </section>
  <script>
    const apiUrl = {{ url_for('api_documents')|tojson }};
    const apiButton = document.querySelector('#load-api');
    const apiStatus = document.querySelector('#api-status');
    const apiResult = document.querySelector('#api-result');

    async function loadDocuments() {
      apiStatus.textContent = '正在读取…';
      try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error('HTTP ' + response.status);
        }
        const documents = await response.json();
        apiResult.textContent = JSON.stringify(documents, null, 2);
        apiStatus.textContent = '读取 ' + documents.length + ' 条';
      } catch (error) {
        apiStatus.textContent = '读取失败：' + error.message;
      }
    }

    apiButton.addEventListener('click', loadDocuments);
  </script>
</body>
</html>
"""


def get_db():
    """Return this request's SQLite connection, creating it on first use."""
    if "db" not in g:
        os.makedirs(os.path.dirname(app.config["DATABASE"]), exist_ok=True)
        connection = sqlite3.connect(app.config["DATABASE"])
        g.db = connection
        connection.row_factory = sqlite3.Row
        connection.execute(
            "CREATE TABLE IF NOT EXISTS documents "
            "(id INTEGER PRIMARY KEY, title TEXT NOT NULL, owner_id INTEGER NOT NULL)"
        )
        count = connection.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
        if count == 0:
            connection.executemany(
                "INSERT INTO documents (id, title, owner_id) VALUES (?, ?, ?)",
                [(1, "Python 入门", 7), (2, "HTTP 请求", 7), (3, "SQL 查询", 9)],
            )
            connection.commit()
    return g.db


@app.teardown_appcontext
def close_db(error=None):
    """Close the request's connection when Flask tears down its context."""
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()


@app.get("/")
def index():
    query = request.args.get("q", "").strip()
    db = get_db()
    if query:
        documents = db.execute(
            "SELECT id, title, owner_id FROM documents WHERE title LIKE ? ORDER BY id",
            (f"%{query}%",),
        ).fetchall()
    else:
        documents = db.execute(
            "SELECT id, title, owner_id FROM documents ORDER BY id"
        ).fetchall()
    return render_template_string(
        INDEX_TEMPLATE,
        documents=documents,
        query=query,
        user_id=session.get("user_id"),
    ), 200


@app.get("/api/documents")
def api_documents():
    query = request.args.get("q", "").strip()
    db = get_db()
    if query:
        documents = db.execute(
            "SELECT id, title, owner_id FROM documents WHERE title LIKE ? ORDER BY id",
            (f"%{query}%",),
        ).fetchall()
    else:
        documents = db.execute(
            "SELECT id, title, owner_id FROM documents ORDER BY id"
        ).fetchall()
    return jsonify([dict(document) for document in documents]), 200


@app.post("/login")
def login():
    raw_user_id = request.form.get("user_id", "").strip()
    if raw_user_id not in {"7", "9"}:
        abort(400, description="演示身份只接受 7 或 9")
    session.clear()
    session["user_id"] = int(raw_user_id)
    return redirect(url_for("index"), code=303)


@app.post("/documents")
def add_document():
    user_id = session.get("user_id")
    if user_id not in {7, 9}:
        abort(400, description="请先选择演示身份")
    title = request.form.get("title", "").strip()
    if not title or len(title) > 80:
        abort(400, description="标题必须是 1 到 80 个字符")
    db = get_db()
    db.execute(
        "INSERT INTO documents (title, owner_id) VALUES (?, ?)",
        (title, user_id),
    )
    db.commit()
    return redirect(url_for("index"), code=303)


@app.post("/reading-list")
def add_to_reading_list():
    if session.get("user_id") not in {7, 9}:
        abort(400, description="请先选择演示身份")
    raw_document_id = request.form.get("document_id", "")
    try:
        document_id = int(raw_document_id)
    except ValueError:
        abort(400, description="文档 ID 无效")
    db = get_db()
    exists = db.execute(
        "SELECT 1 FROM documents WHERE id = ?", (document_id,)
    ).fetchone()
    if exists is None:
        abort(400, description="文档不存在")

    reading_list = session.get("reading_list", [])
    if not isinstance(reading_list, list):
        reading_list = []
    if document_id not in reading_list:
        reading_list.append(document_id)
    session["reading_list"] = reading_list
    return redirect(url_for("index"), code=303)


@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"), code=303)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
```

正常首页是 `200 OK`，无查询时返回三个种子文档。`/?q=HTTP` 仍为 200，只列 HTTP 请求；无结果也是 200，因为路径有效，只是集合为空。`POST /login` 的合法值回 `303 See Other`，浏览器随后 GET `/`；非法值回 400。不存在的路由由 Flask 返回 404。

## 从请求追到响应

### Flask 实例与 route 装饰器

`from flask import Flask` 导入 Flask 类；`app = Flask(__name__)` 创建本应用的实例。它保存配置、路由表和扩展状态。`@app.get("/")` / `@app.post(...)` 是 Python 装饰器语法：定义函数时，Flask 将 URL 规则、HTTP 方法和函数关联起来。用户请求到达时，Flask 根据方法与路径找到视图函数并调用；不是我们手动调用 `index()`。

`request`、`session`、`g` 是 Flask 在当前请求/应用上下文中提供的代理对象。它们不是全局共享的一个 HTTP 请求。请求结束后上下文被拆除；不要把 request 内容保存到跨请求全局变量。`g` 适合保存此请求生命周期内的连接。

### Query、表单与 HTTP 方法

浏览器访问 `/?q=HTTP` 发 GET。`request.args` 是 URL 查询参数集合，`.get("q", "")` 读一个值；如果没有 `q`，就用空字符串。GET 便于分享/收藏搜索结果，不能放密码或秘密。

浏览器提交 `method="post"` 的表单时，Flask 用 `request.form` 读取表单字段。`.get("title", "")` 返回字段或默认值。客户端的 `required`、`maxlength` 是体验提示，服务端仍主动检查空白和长度；用户可绕过 HTML 控件直接发请求。

GET 适合读取；POST 用于提交会改变状态的数据。POST 数据通常位于正文而不是 URL，但并非因此获得加密。必须用 HTTPS 保护网络传输；仍需授权、输入校验、CSRF 防护和错误处理。

### 返回值、状态与重定向

视图函数返回字符串时 Flask 可把它作为响应正文；返回 `render_template_string(...), 200` 是 `(body, status)` 形式。`abort(400)` 立即产生对应错误响应。`redirect(url_for("index"), code=303)` 先让 `url_for` 根据视图函数名生成路径，再告诉浏览器去 GET 目标。303 的意图是 POST/处理后转 GET，避免刷新页面重复提交；这仍不保证任意业务动作天然去重。

### SQLite 连接和数据所有权

`sqlite3` 是 Python 标准库，不是 Flask 的一部分。`get_db` 第一次在当前请求中被调用时才创建连接，并放入 `g.db`；同一请求后续调用复用它。`@app.teardown_appcontext` 在该上下文收尾时取出并关闭连接。下一请求会有自己的 `g` 和连接。不要把一个连接塞进模块级变量让多个请求/线程共享。

连接一创建就放进 `g`，而不是等建表和种子数据全部成功后才登记；这样初始化中途报错，收尾函数仍能找到并关闭连接。

`?` 是 SQLite 参数占位符；值作为第二个参数绑定。这样标题中的引号按数据处理，而不是拼成 SQL 语法。永远不要用 `f"... {user_input} ..."` 把不可信输入拼进 SQL。表名、列名一般不能像值一样用 `?` 参数化，动态标识符必须通过白名单选择。

种子行是仅供课堂使用的样例。数据库路径放在 Flask `instance_path` 下，并使用独立文件名 `cs50x-notes-demo.sqlite3`。这不是仓库里真实应用的数据源；练习的所有权范围只到该 demo 文件。

## 模板的职责与输出转义

Jinja 是 Flask 常用的模板语言。`render_template_string(INDEX_TEMPLATE, documents=...)` 把变量交给 Jinja；`{{ document['title'] }}` 输出模板变量，`{% for ... %}` 做模板控制流程。默认 HTML 模板会自动转义普通变量，`<script>` 等字符作为文字呈现，而不是浏览器执行的标记。不要对不可信内容使用 `|safe`：它会跳过转义并可能引入 XSS。

内嵌模板适合这里的一文件演示，不适合多人维护的实际项目。真实 Flask 项目通常这样拆分：

```text
examples/cs50x/
├── app.py
└── templates/
    ├── layout.html
    └── index.html
```

在 `app.py` 用 `from flask import render_template`，然后 `return render_template("index.html", documents=documents)`。模板文件放在 Flask 应用默认查找的 `templates/` 相对目录；CSS、图片和浏览器 JavaScript 通常放 `static/`，用 `url_for('static', filename='style.css')` 生成 URL。模板继承（template inheritance）把共同 HTML 外壳放进 `layout.html`：它用 `{% block body %}{% endblock %}` 留出命名位置；`index.html` 以 `{% extends "layout.html" %}` 声明父模板，再提供同名 `{% block body %}` 内容。Jinja 渲染子模板时把内容填入父模板的 block，最终响应仍是一份完整 HTML；导航或页脚只需改父模板一次。不要把模板放 `static/`：静态文件不会由 Jinja 执行。

## Cookie、session 与登录边界

HTTP 请求彼此独立，服务器默认不会自动记得上次请求者是谁。浏览器 Cookie 是服务器要求浏览器在后续请求携带的一小段数据；Flask `session` 是以字典形式使用的接口。本例 `session["user_id"] = 7` 会被序列化并放进 Flask 默认的客户端 Cookie，再由 `SECRET_KEY` 签名校验。

Flask 默认 session Cookie 是签名而非加密：用户不能在不知道密钥时任意修改并通过签名校验，但内容原则上可被读取。因此不要放密码、访问令牌或机密数据。应用从 `FLASK_SECRET_KEY` 环境变量读取密钥；未设置时立即报错退出，不提供硬编码默认值。真实项目必须用高熵随机 secret，存放在环境变量或 secret manager，不提交代码库；轮换密钥会使旧签名 Cookie 失效。测试客户端另外注入仅用于测试的临时值。

Cookie 中存在一个 `user_id` 不等于完成了真实身份认证。当前页面让用户自行选 7 或 9，任何人都能切换，这是“演示身份”，绝不保护真实用户记录。真实应用需验证凭证、处理密码安全存储、基于当前身份检查每项资源的授权，并在改数据的路由上做 CSRF 防护。即便一个请求已登录，也不能仅靠表单隐藏按钮来授权。

CSRF（Cross-Site Request Forgery，跨站请求伪造）是诱使已登录浏览器向目标站点发起非预期请求；浏览器可能自动带上 Cookie。生产表单通常需要不可预测的 CSRF token 与适当 Cookie 策略（例如 SameSite），并结合 Origin/Referer 等防护。此示例故意没有 token，因此仅本机课堂演示，不能作为公开部署模板。

## 离线测试：`test_app.py`

Flask 的 `app.test_client()` 提供测试客户端，在进程内构造 HTTP 请求，不开启 socket、不联系外网。测试会把 SQLite 路径改到临时目录，因此不会接触贯穿项目文件或用户数据库。保存为同目录的 `examples/cs50x/test_app.py`。

```python
import os
import tempfile
import unittest
from app import app


class NotesAppTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        app.config.update(
            TESTING=True,
            SECRET_KEY="test-only-signing-key",
            DATABASE=os.path.join(self.temp_dir.name, "test.sqlite3"),
        )
        self.client = app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_get_search_and_not_found(self):
        response = self.client.get("/?q=HTTP")
        self.assertEqual(response.status_code, 200)
        self.assertIn("HTTP 请求".encode(), response.data)
        self.assertNotIn("SQL 查询".encode(), response.data)
        self.assertEqual(self.client.get("/missing").status_code, 404)

    def test_api_json_and_response_parsing(self):
        response = self.client.get("/api/documents?q=SQL")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")
        self.assertEqual(
            response.get_json(),
            [{"id": 3, "title": "SQL 查询", "owner_id": 9}],
        )
        empty_response = self.client.get("/api/documents?q=missing")
        self.assertEqual(empty_response.get_json(), [])

    def test_invalid_demo_identity_is_rejected(self):
        response = self.client.post("/login", data={"user_id": "99"})
        self.assertEqual(response.status_code, 400)

    def test_login_session_and_create(self):
        login_response = self.client.post(
            "/login", data={"user_id": "7"}, follow_redirects=True
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertIn(b"owner 7", login_response.data)

        reading_response = self.client.post(
            "/reading-list", data={"document_id": "1"}, follow_redirects=True
        )
        self.assertEqual(reading_response.status_code, 200)
        self.assertIn("待读文档 ID：1".encode(), reading_response.data)

        create_response = self.client.post(
            "/documents", data={"title": "C 指针"}, follow_redirects=True
        )
        self.assertEqual(create_response.status_code, 200)
        self.assertIn("C 指针".encode(), create_response.data)
        self.assertIn(b"owner 7", create_response.data)

        self.client.post("/logout")
        self.assertEqual(
            self.client.post("/documents", data={"title": "未授权"}).status_code,
            400,
        )

    def test_invalid_title_is_rejected(self):
        self.client.post("/login", data={"user_id": "9"})
        response = self.client.post("/documents", data={"title": "   "})
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main(verbosity=2)
```

预期五个测试通过：HTML 搜索包含/排除对应标题，JSON 接口返回 application/json 且可解析为预期列表，非法路径是 404，非法身份与空标题是 400，登录后待读列表与新增标题都能显示在后续请求中，退出后再提交被拒绝。这里的登录测试只验证演示 session 流程，不证明认证或授权安全。

## 逐步验证与改动

1. 先不运行服务，运行 `python -m unittest -v test_app.py`。它在临时文件中创建 SQLite 表，不需要联网。
2. 将测试中的 `q=HTTP` 改为 `q=Python`：应包含 Python、排除 SQL。这检验路由读取 `request.args` 和绑定查询参数。
3. 将 `title` 改成 `引号 ' 和问号 ?`：它应作为普通标题写入/呈现；不要通过修改为 SQL 字符串拼接来“简化”。
4. 删除 `follow_redirects=True` 并打印登录响应：应看到 303 和 `Location` 头。再 GET 目标路径，浏览器/测试客户端才会跟随重定向。
5. 将 `SECRET_KEY` 测试值改动后新建客户端 Cookie：旧 Cookie 签名不再匹配，session 不会被信任。测试密钥固定只为可重复测试；线上密钥必须秘密且随机。
6. 如果出现 `ModuleNotFoundError: flask`，确认运行命令使用 `examples/cs50x/.venv-flask/bin/python`，并只在该环境安装 Flask；不要改项目依赖文件。

## API、JSON 与 AJAX 在哪里

API（Application Programming Interface，应用程序编程接口）是供另一个程序调用的契约，不限定是否返回网页。HTML 页面路由通常返回 HTML；数据 API 可以返回 JSON（JavaScript Object Notation，一种常见文本数据格式），例如 `{"id": 1, "title": "Python 入门"}`。HTTP 状态码和响应标头仍然适用。

AJAX 是浏览器页面加载后用 JavaScript 异步请求服务器、局部更新界面的传统统称；今天常见实现使用 `fetch`，不必使用旧的 XMLHttpRequest。上面页面按钮的实际数据流是：点击事件调用 `loadDocuments` → 浏览器 `fetch(apiUrl)` 发同源 GET → Flask `api_documents` 查 SQLite 并用 `jsonify` 返回 JSON → `response.ok` 检查 HTTP 状态 → `response.json()` 把响应文本解析成 JavaScript 数组 → `JSON.stringify` 格式化后写入 `textContent`。`await` 暂停当前 async 函数直到 Promise 完成，不阻塞整个浏览器界面。测试里的 `response.get_json()` 执行对应的 JSON 解码并断言字段和值。

Promise 是 JavaScript 用来表示“异步操作最终成功或失败”的对象，`async` 函数会返回 Promise；`await` 等待其结果，失败可以由 `try/catch` 处理。模板中的 `|tojson` 将 Python 值编码成适合嵌入脚本的 JSON 表示，不是把任意字符串直接拼进 JavaScript。`jsonify` 则负责生成 JSON HTTP 响应，这与模板编码是不同位置的操作。

待读列表示例把一组整数 ID 存在 Flask session 中。POST `/reading-list` 先校验演示身份和数据库里确有该文档，再取出 list、append 新 ID，并把 list 重新赋回 `session["reading_list"]`。Flask 默认 Cookie session 会检测顶层键赋值；对嵌套可变对象只做 `session["reading_list"].append(id)` 时，修改标记可能不会自动更新，所以要重新赋值或显式设置 `session.modified = True`。这个列表很小且只是演示；客户端 Cookie 有体积限制，正式购物车/大量状态应考虑服务端存储。POST 仍需 CSRF 防护，本演示没有，不能部署。

## 常见坑与安全检查

- Flask `route` 默认支持 GET，并自动处理相应的 HEAD/OPTIONS；POST 要明确用 `@app.post` 或 `methods=["GET", "POST"]`。
- `request.args` 对应 URL 查询；`request.form` 对应常规表单正文。用错常得到空值。
- `request` 只能在有效请求上下文里取值；不要在模块导入时读取 `request.args`。
- `g.db` 只活在当前应用上下文；本例 teardown 关闭它，不能跨线程共享连接。
- SQLite 占位符只绑定值，不要把用户输入拼入 SQL。
- Jinja 默认转义 HTML 普通变量；`|safe` 关闭这道防线。
- Session 的签名不隐藏 Cookie 内容；secret 不能公开或提交。
- `debug=True` 可能暴露交互式调试器；`0.0.0.0` 会把服务暴露给其他网络设备。本章只绑定 `127.0.0.1` 且关闭 debug。
- POST 并不自动防 CSRF；示例没有 CSRF token，不能上线。
- `user_id` 存在 session 仅代表客户端持有经过签名的数据；演示中的身份选择不是认证。

## 独立练习：给文档 API 加分页

需求：扩展已完成的 `/api/documents`，增加可选 `limit` 参数限制返回条数，默认 20、最大 100；保留可选 `q` 标题筛选，并按 id 稳定排序。

输入输出契约：`GET /api/documents?q=SQL&limit=1` 返回 JSON 数组，元素形状为 `{"id":3,"title":"SQL 查询","owner_id":9}`；无匹配返回空数组和 200；limit 非整数或不在 1 到 100 之间返回 400。不得返回 Cookie secret，不得让客户端指定身份后读取未经授权的私有数据；这份 demo 数据公开仅用于课程练习。

验收：test_client 断言 JSON content type、对象字段、筛选结果、分页上限、非法 limit 与空结果状态；标题中包含引号仍是数据。保持不启动服务和不访问真实 DB。定位提示：先校验 limit 的类型/范围，再把它作为 SQL 参数绑定；不要把 Python `str(dict)` 当 JSON。

## 对应官方资料与作业

本章依据 [CS50x Week 9](https://cs50.harvard.edu/x/weeks/9/) 与 [Lecture 9 notes](https://cs50.harvard.edu/x/notes/9/) 的 http-server、Flask、Forms、Templates、Request Methods、Frosh IMs、Flask and SQL、Cookies and Session、Shopping Cart、Shows、APIs、JSON 内容。目录应用包含 JSON API/fetch 数据流与待读 session list 实验，覆盖主要机制；Frosh IMs 与 Shows 的业务项目仍可按官方讲义继续实践。

官方问题集入口为 [Problem Set 9](https://cs50.harvard.edu/x/psets/9/)，其中 [Birthdays](https://cs50.harvard.edu/x/psets/9/birthdays/) 的中文主题说明：构建一个 Flask 应用，通过表单录入生日、用 SQLite 持久化并展示数据；重点是让 HTML、Python 路由和 SQL 共同完成可验证的读写流程。官方要求以原页面为准，这里不提供题解。

同一问题集还要求 [Finance](https://cs50.harvard.edu/x/psets/9/finance/)，将账户、会话、数据查询与交易记录组织成完整应用。完成 Birthdays 不等于已经完成整个 Problem Set 9；正式验收按两项要求分别进行。

## 课后压缩

心智模型：Flask 把“方法 + 路径”分派给视图函数；函数从 request 取输入，调用数据库，再构造响应。模板负责呈现，数据库连接按请求创建并关闭。

最小链路：浏览器 POST → Flask route → 校验 → 参数化 SQL → commit → `redirect(url_for(...))` → GET 页面。

边界：签名 session 不等于加密或真实登录；本示例没有 CSRF 防护。复习问题：谁创建 `g.db`，何时关闭，为什么不能放在模块级共享？

## 导航

- 上一章：[08 · HTML、CSS 与 JavaScript](08_HTML_CSS_JavaScript.md)
- 下一章：[10 · 课程收束与后续学习](10_课程收束与后续学习.md)
- 本目录：[CS50x 中文课程索引](README.md)
