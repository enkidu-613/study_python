# threading 基础

> 本章学什么：线程是什么、`threading.Lock` 怎么用、在本项目里保护什么。
> 本章不学什么：不学 `asyncio`、不学进程池、不学并发设计模式。

## 库定位

| 属性 | 值 |
|------|-----|
| 分类 | Python 标准库（无需安装） |
| 导入写法 | `import threading` |
| 解决什么问题 | 多个线程同时操作共享资源时，防止数据竞争和重复执行 |
| 不负责什么 | 不负责异步 IO（那是 `asyncio`）、不负责进程管理（那是 `multiprocessing`） |
| 本章要求 | 认识并会用：`Lock()`、`with lock:`、理解"双重检查锁定"模式 |

## 1. 心智模型

`threading.Lock` 就是一把**厕所门的插销**——进去插上，别人进不来；出来拔掉，下一个人才能进。

## 2. 准确术语

- **线程（Thread）**：程序执行的最小单位。一个进程可以有多个线程，线程间共享内存。
- **`threading.Lock`**：互斥锁对象。同一时间只允许一个线程持有锁，其他线程必须等待。
- **`acquire()` / `release()`**：获取锁 / 释放锁。`with lock:` 是自动 acquire/release 的语法糖。
- **双重检查锁定（Double-Checked Locking）**：先无锁检查 → 加锁 → 再检查一次的模式，避免每次都加锁。

## 3. 边界

| 包含 | 不包含 |
|------|--------|
| `Lock` 的 acquire / release | `asyncio.Lock`（异步锁） |
| `with lock:` 语法糖 | `RLock`（可重入锁） |
| `Thread` 的创建和启动 | `multiprocessing.Process`（进程） |
| 双重检查锁定模式 | `Semaphore`、`Event`、`Condition` |

## 4. 最小可运行模板

```python
import threading

# 创建锁
lock = threading.Lock()

# 使用锁
with lock:          # 进入 → 自动 acquire（上锁）
    shared_data += 1  # 同一时间只有一个线程能执行这里
                    # 退出 → 自动 release（解锁）
```

## 5. 为什么需要锁

FastAPI 服务是多线程的，多个用户可以同时发请求。不加锁会出问题：

```python
# 不加锁：两个线程同时加载模型
_model = None

def get_model():
    if _model is None:           # 线程 A 和 B 同时到这里，都是 True
        _model = load_model()    # A 和 B 都执行了加载！模型被加载两次
    return _model
```

加锁后：

```python
_model = None
_lock = threading.Lock()

def get_model():
    if _model is not None:       # 第一步：无锁快速检查（已有就直接返回）
        return _model

    with _lock:                  # 第二步：加锁
        if _model is not None:   # 第三步：再检查一次（可能别人刚加载完）
            return _model
        _model = load_model()    # 只有第一个线程会走到这里
    return _model
```

## 6. 核心操作

### 6.1 创建锁

```python
import threading

lock = threading.Lock()  # 创建一个锁对象
```

### 6.2 手动 acquire / release

```python
lock.acquire()       # 上锁，其他线程到这里会阻塞等待
try:
    shared_data += 1
finally:
    lock.release()   # 解锁，必须在 finally 里，防止异常时死锁
```

### 6.3 with 语法糖（推荐）

```python
with lock:           # 进入时自动 acquire
    shared_data += 1
                       # 退出时自动 release，即使异常也会释放
```

`with lock:` 等价于上面的 `acquire` + `try/finally release`，但更简洁、更安全。

### 6.4 创建和启动线程

```python
import threading

def worker(name):
    print(f"线程 {name} 开始工作")

# 创建线程
t = threading.Thread(target=worker, args=("A",))

# 启动线程
t.start()  # 立即返回，worker 在后台执行

# 等待线程结束
t.join()   # 阻塞直到 worker 执行完毕
```

### 6.5 双重检查锁定模式

```python
_model = None
_lock = threading.Lock()

def get_model():
    # 第一次检查：无锁，快速返回（99% 的情况走这里）
    if _model is not None:
        return _model

    # 加锁
    with _lock:
        # 第二次检查：可能第一个线程刚加载完
        if _model is not None:
            return _model

        # 真正加载（只执行一次）
        _model = load_model()

    return _model
```

为什么要检查两次？

```
线程 A 和 B 同时通过第一次检查（都是 None）

线程 A 拿到锁，进入 with 块
线程 B 等待锁

线程 A 加载模型，_model 有值了，释放锁
线程 B 拿到锁，进入 with 块

如果没有第二次检查 → 线程 B 又加载了一次模型（浪费！）
有第二次检查 → 线程 B 发现 _model 已经有值，直接返回
```

## 7. 在本项目中的用法

### 7.1 保护模型加载

```python
# app/embedding.py 第 34 行
_load_lock = threading.Lock()

# app/embedding.py get_embedding_model 函数
def get_embedding_model() -> SentenceTransformer:
    if _model is not None:          # 第一次检查：无锁
        return _model

    with _load_lock:                # 加锁
        if _model is not None:      # 第二次检查：防止重复加载
            return _model

        info = _detect_device()
        model = _load_model(model_name, device)
        _model = model              # 缓存

    return _model
```

### 7.2 为什么 FastAPI 需要锁

FastAPI 默认用线程池处理同步路由（`def` 而不是 `async def`）。多个用户同时请求 `/chat`，多个线程同时调用 `get_embedding_model()`，不加锁会导致模型被加载多次，浪费内存和加载时间。

## 8. 常见坑

### 坑 1：忘记 release 导致死锁

```python
lock.acquire()
shared_data += 1
# 忘了 release() → 锁永远不释放，其他线程永远等待（死锁）

# ✅ 用 with 自动释放
with lock:
    shared_data += 1
```

### 坑 2：锁范围太大

```python
# ❌ 锁住了不需要保护的操作，降低并发性能
with lock:
    data = fetch_from_api()  # 网络请求，很慢，但不需要锁
    result = process(data)   # 只有这里需要锁
    save(result)

# ✅ 只锁需要保护的部分
data = fetch_from_api()
with lock:
    result = process(data)
save(result)
```

### 坑 3：第一次检查忘了

```python
# ❌ 每次都加锁，即使模型已经加载好了，性能差
def get_model():
    with _lock:
        if _model is not None:
            return _model
        _model = load_model()
    return _model

# ✅ 先无锁检查，避免不必要的加锁
def get_model():
    if _model is not None:
        return _model
    with _lock:
        ...
```

## 9. 和 asyncio 的区别

| | `threading.Lock` | `asyncio.Lock` |
|---|---|---|
| 来源 | `import threading` | `import asyncio` |
| 适用场景 | 多线程同步代码 | 协程异步代码 |
| 阻塞方式 | 阻塞整个线程 | 只挂起当前协程 |
| 在项目中 | 保护 `get_embedding_model()` | FastAPI 的 `async def` 路由 |
| 能混用吗 | 不能 | 不能 |

**规则**：`def` 函数用 `threading.Lock`，`async def` 函数用 `asyncio.Lock`。

## 10. 常用 API 速查

| 方法 | 作用 | 示例 |
|------|------|------|
| `threading.Lock()` | 创建锁 | `lock = threading.Lock()` |
| `with lock:` | 自动加锁/解锁 | `with lock: ...` |
| `lock.acquire()` | 手动加锁 | `lock.acquire()` |
| `lock.release()` | 手动解锁 | `lock.release()` |
| `threading.Thread()` | 创建线程 | `Thread(target=fn, args=())` |
| `.start()` | 启动线程 | `t.start()` |
| `.join()` | 等待线程结束 | `t.join()` |
| `threading.current_thread()` | 获取当前线程对象 | `threading.current_thread().name` |

## 11. 检查点

验证四条理解标准：

1. **核心思想是什么？** `threading.Lock` 是互斥锁，保证同一时间只有一个线程执行被保护的代码块，防止多线程数据竞争。

2. **它解决什么问题？** FastAPI 多线程环境下，多个请求同时触发模型加载，不加锁会导致模型被加载多次，浪费内存和时间。

3. **为什么不用常见替代方案？** `asyncio.Lock` 只能用在协程里，不能用在 `def` 同步函数中；不加锁则无法保证线程安全。

4. **在本项目里怎么实现或识别？** `app/embedding.py` 第 34 行定义 `_load_lock = threading.Lock()`，`get_embedding_model()` 用双重检查锁定模式——先无锁检查 `_model is not None`，再加锁、二次检查、加载模型。
