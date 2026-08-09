# NumPy 基础

> 本章学什么：NumPy 数组是什么、怎么用、在本项目里做什么。
> 本章不学什么：不学矩阵分解、线性代数推导、不学 GPU 加速（那是 PyTorch 的活）。

## 库定位

| 属性 | 值 |
|------|-----|
| 分类 | Python 第三方库 |
| 依赖名 | `numpy`（Poetry 管理间接依赖，随 `sentence-transformers` 安装） |
| 导入写法 | `import numpy as np` |
| 解决什么问题 | Python 列表做数值运算太慢，NumPy 提供内存连续、C 底层的向量化数组 |
| 不负责什么 | 不负责 GPU 加速、不负责自动求导、不负责深度学习模型（这些是 PyTorch 的职责） |
| 本章要求 | 认识并会用：创建数组、向量化运算、`.tolist()`、`np.dot()` |

## 1. 心智模型

NumPy 数组就是**加了加速引擎的列表**——语法和列表差不多，但运算速度快几十倍。

## 2. 准确术语

- **`numpy.ndarray`**：NumPy 的核心类型，N 维数组对象。代码里用 `np.array([1, 2, 3])` 创建。
- **向量化运算（Vectorization）**：对整个数组做运算时不需要写 `for` 循环，底层 C 一次性批量执行。
- **`dtype`**：数组元素的数据类型，如 `float64`、`int32`。和 Python 列表不同，同一个数组里所有元素类型必须一致。

## 3. 边界

| 包含 | 不包含 |
|------|--------|
| N 维数组创建、索引、切片 | GPU 加速（用 PyTorch） |
| 向量化算术运算（+、-、*、/） | 自动求导（用 PyTorch） |
| 聚合运算（sum、mean、max） | 深度学习模型层（用 PyTorch） |
| 线性代数（dot、norm） | 神经网络训练（用 PyTorch） |
| 和 Python 列表 / PyTorch Tensor 互转 | DataFrame 操作（用 Pandas） |

## 4. 最小可运行模板

```python
import numpy as np

# 创建
a = np.array([1.0, 2.0, 3.0])

# 向量化运算（不需要 for 循环）
b = a * 2                # array([2., 4., 6.])

# 聚合
total = a.sum()          # 6.0

# 和 Python 列表互转
back_to_list = a.tolist()  # [1.0, 2.0, 3.0]
```

## 5. 为什么不用 Python 列表

```python
# Python 列表：逐个元素相乘，每次都要查找对象、类型检查
a = [1.0, 2.0, 3.0]
b = [x * 2 for x in a]  # [2.0, 4.0, 6.0]

# NumPy 数组：底层 C 一次性批量运算
a = np.array([1.0, 2.0, 3.0])
b = a * 2  # array([2., 4., 6.])，一条指令搞定全部
```

数据量大时（比如 512 维向量），NumPy 比纯 Python 快 **10~100 倍**。

类比：

```
Python 列表 = 每个数字装一个独立盒子，标签贴在外面，找起来要逐个翻
NumPy 数组   = 所有数字排成一排放进流水带，机器一批一批处理
```

## 6. 核心操作

### 6.1 创建数组

```python
import numpy as np

# 从列表创建
arr = np.array([1.0, 2.0, 3.0])
# array([1., 2., 3.])

# 创建全零数组（常用于初始化向量）
zeros = np.zeros(512)  # 512 维全零向量

# 创建全一数组
ones = np.ones(4)
# array([1., 1., 1., 1.])

# 创建二维数组（矩阵）
matrix = np.array([[1, 2], [3, 4]])
# array([[1, 2],
#        [3, 4]])
```

### 6.2 形状与类型

```python
arr = np.array([1.0, 2.0, 3.0])
arr.shape      # (3,)     → 一维，3 个元素
arr.ndim       # 1        → 一维
arr.dtype      # float64  → 元素类型（全数组统一）
```

### 6.3 向量化运算

```python
a = np.array([1.0, 2.0, 3.0])

a * 2          # array([2., 4., 6.])    每个元素乘 2
a + 1          # array([2., 3., 4.])    每个元素加 1
a ** 2         # array([1., 4., 9.])    每个元素平方

# 两个数组运算（逐元素）
b = np.array([4.0, 5.0, 6.0])
a + b          # array([5., 7., 9.])
a * b          # array([4., 10., 18.])
```

### 6.4 聚合运算

```python
a = np.array([1.0, 2.0, 3.0])

a.sum()        # 6.0     求和
a.mean()       # 2.0     平均值
a.max()        # 3.0     最大值
a.min()        # 1.0     最小值
```

### 6.5 索引与切片

```python
a = np.array([1.0, 2.0, 3.0, 4.0, 5.0])

a[0]           # 1.0     第一个（和 Python 列表一样）
a[-1]          # 5.0     最后一个
a[1:3]         # array([2., 3.])   切片（和 Python 列表一样）

# 布尔索引（Python 列表做不到）
a[a > 3]       # array([4., 5.])   筛选大于 3 的元素
```

### 6.6 和 Python 列表互转

```python
# 列表 → NumPy 数组
python_list = [1.0, 2.0, 3.0]
arr = np.array(python_list)

# NumPy 数组 → 列表
arr = np.array([1.0, 2.0, 3.0])
back_to_list = arr.tolist()  # [1.0, 2.0, 3.0]
```

## 7. 在本项目中的用法

### 7.1 SentenceTransformer 输出

```python
# app/embedding.py _load_model 函数
model.encode(
    "test",
    convert_to_numpy=True,      # 输出 NumPy 数组而不是 PyTorch Tensor
    normalize_embeddings=True,   # 归一化
)
# 返回 np.array([0.12, -0.03, 0.88, ...])，512 维
```

`convert_to_numpy=True` 让模型输出 NumPy 数组，方便 CPU 端做向量运算。

### 7.2 最终转成 Python 列表存入 ChromaDB

```python
# app/embedding.py get_document_embeddings 函数
model.encode(
    clean_texts,
    batch_size=_get_batch_size(tier),
    convert_to_numpy=True,
    normalize_embeddings=True,
).tolist()  # ← .tolist() 把 NumPy 数组转回 Python 列表
```

为什么最后要 `.tolist()`？因为 ChromaDB 的 API 要求 Python 列表，不收 NumPy 数组。

### 7.3 余弦相似度计算

```python
# NumPy 点积（一条指令）
similarity = np.dot(vec_a, vec_b)

# 等价的 Python 写法（慢几十倍）
similarity = sum(a * b for a, b in zip(vec_a, vec_b))
```

## 8. 常见坑

### 坑 1：dtype 隐式转换

```python
a = np.array([1, 2, 3])       # dtype=int64
b = np.array([1.0, 2.0, 3.0]) # dtype=float64

c = a + b                      # dtype=float64（int 被提升为 float）
# 不报错，但如果你以为 c 还是整数，可能出 bug
```

### 坑 2：忘了 .tolist() 导致 ChromaDB 报错

```python
# ❌ 直接传 NumPy 数组给 ChromaDB
collection.add(embeddings=model.encode(texts, convert_to_numpy=True))
# → 报错：ChromaDB 不接受 numpy.ndarray

# ✅ 转成 Python 列表
collection.add(embeddings=model.encode(texts, convert_to_numpy=True).tolist())
```

### 坑 3：和 Python 列表的乘法语义不同

```python
# Python 列表：* 是重复
[1, 2] * 3    # [1, 2, 1, 2, 1, 2]

# NumPy 数组：* 是逐元素乘法
np.array([1, 2]) * 3    # array([3, 6])
```

## 9. 和 PyTorch Tensor 的关系

| | NumPy 数组 | PyTorch Tensor |
|---|---|---|
| 来源 | `import numpy as np` | `import torch` |
| 能跑 GPU | 不能 | 能 |
| 用途 | CPU 上的向量运算 | GPU 上的深度学习 |
| 互转 | `torch.from_numpy(arr)` | `tensor.numpy()` |
| 在项目中 | `convert_to_numpy=True` 输出 | SentenceTransformer 内部计算用 |

SentenceTransformer 内部用 PyTorch Tensor 做 GPU 推理，`convert_to_numpy=True` 把结果转成 NumPy 数组方便 CPU 端使用。

## 10. 常用 API 速查

| 方法 | 作用 | 示例 |
|------|------|------|
| `np.array()` | 从列表创建数组 | `np.array([1, 2, 3])` |
| `np.zeros()` | 创建全零数组 | `np.zeros(512)` |
| `np.ones()` | 创建全一数组 | `np.ones(3)` |
| `.shape` | 查看形状 | `(512,)` |
| `.dtype` | 查看元素类型 | `float64` |
| `.tolist()` | 转回 Python 列表 | `[1.0, 2.0, 3.0]` |
| `np.dot()` | 点积（余弦相似度用） | `np.dot(a, b)` |
| `np.linalg.norm()` | 向量范数（归一化用） | `np.linalg.norm(a)` |
| `.sum()` | 求和 | `a.sum()` |
| `.mean()` | 平均值 | `a.mean()` |

## 11. 检查点

验证四条理解标准：

1. **核心思想是什么？** NumPy 数组是内存连续、类型统一的 N 维数组，用 C 底层实现向量化运算，比 Python 列表快几十倍。

2. **它解决什么问题？** Python 列表做批量数值运算（如 512 维向量计算）太慢，NumPy 把整个数组的运算下沉到 C 层一次性完成。

3. **为什么不用常见替代方案？** Python 列表没有向量化运算，`for` 循环逐个处理慢 10~100 倍；PyTorch Tensor 能做 GPU 加速但太重，CPU 端的向量运算用 NumPy 更轻量。

4. **在本项目里怎么实现或识别？** `app/embedding.py` 里 `model.encode(convert_to_numpy=True)` 输出 NumPy 数组，最终 `.tolist()` 转成 Python 列表存入 ChromaDB；余弦相似度计算用 `np.dot()`。
