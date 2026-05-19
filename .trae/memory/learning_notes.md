# 学习笔记与重点

## 核心概念理解

### 1. 依赖注入 (DI) 和控制反转 (IoC)

**一句话理解**: 把创建和管理对象的工作交给框架，我只负责使用。

**类比**:
- 传统方式：自己买菜、做饭、洗碗
- IoC方式：去餐厅，点菜后厨师做好端给你

**代码体现**:
```python
# 传统方式 - 自己管理
def create_todo():
    db = SessionLocal()      # 自己创建
    try:
        # 使用 db
    finally:
        db.close()           # 自己关闭

# IoC方式 - 框架管理
def create_todo(db: Session = Depends(get_db)):
    # 框架创建并注入 db，我只管使用
    # 框架还会自动关闭
```

### 2. 为什么用 yield 而不是 return

**关键区别**:
- `return`: 立即结束函数，后面的代码不执行
- `yield`: 暂停函数，保留状态，可以恢复继续执行

**资源管理场景**:
```python
def get_db():
    db = SessionLocal()      # 1. 创建资源
    try:
        yield db             # 2. 返回资源，暂停等待
    finally:
        db.close()           # 3. 使用完后，恢复执行，清理资源
```

**执行流程**:
1. 调用 `get_db()`，执行到 `yield db`，返回 `db`，暂停
2. 路由函数使用 `db` 执行业务逻辑
3. 路由函数结束，回到 `yield` 处，继续执行 `finally` 块
4. `db.close()` 被执行，资源释放

### 3. APIRouter 的作用

**解决的问题**:
- 代码文件过大
- 路由管理混乱
- 团队协作冲突

**三步使用法**:
1. **创建**: `router = APIRouter(prefix="/todos", tags=["Todos"])`
2. **装饰**: `@router.post("/")` 定义路由
3. **注册**: `app.include_router(router)` 挂载到主应用

**prefix 工作原理**:
```
router prefix = "/todos"
@router.post("/")      → 实际路径: /todos/ + / = /todos/
@router.get("/{id}")   → 实际路径: /todos/ + /{id} = /todos/{id}
```

### 4. ORM 脏数据追踪

**概念**: SQLAlchemy 会自动追踪对象的属性变化

**流程**:
```python
todo = db.query(DBTodo).filter(DBTodo.id == 1).first()  # 查询，对象干净
todo.title = "新标题"                                      # 修改，对象变"脏"
# 此时 SQLAlchemy 记录了变化，但未执行 SQL
db.commit()                                              # 提交，执行 UPDATE
```

**好处**: 只需操作 Python 对象，ORM 自动生成 SQL

## 常见错误与解决

### 错误1: 忘记注册 Router
**现象**: 访问接口返回 404
**原因**: 只定义了 `@router.post()` 但没有 `app.include_router(router)`
**解决**: 在 main.py 中注册

### 错误2: 循环导入
**现象**: `ImportError: cannot import name 'xxx'`
**原因**: A 导入 B，B 又导入 A
**解决**: 延迟导入或调整架构

### 错误3: 数据库连接泄漏
**现象**: 运行一段时间后报错，连接数过多
**原因**: 没有正确关闭数据库连接
**解决**: 使用 `yield` + `finally` 确保关闭

### 错误4: 忘记 commit
**现象**: 操作后数据没有保存到数据库
**原因**: 只执行了 `db.add()` 但没有 `db.commit()`
**解决**: 修改操作后必须 commit

## 学习技巧

1. **画图理解**: 把执行流程画出来，比看代码更直观
2. **对比学习**: 对比 "有" 和 "没有" 某个特性的代码差异
3. **类比生活**: 用生活中的例子理解抽象概念
4. **动手实验**: 修改代码，观察结果变化
5. **教别人**: 能讲清楚才是真正的理解

## 待解决问题

- [ ] 异步编程 async/await 的原理
- [ ] JWT 认证的完整流程
- [ ] 数据库迁移工具 Alembic 的使用
- [ ] 如何编写单元测试
- [ ] Docker 容器化部署
