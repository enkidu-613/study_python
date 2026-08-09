# PyTorch 基础

> 本章学什么：PyTorch 是什么、Tensor 是什么、在本项目里做什么。
> 本章不学什么：不学神经网络搭建、不学自动求导、不学训练循环（这些属于深度学习课程）。

## 库定位

| 属性 | 值 |
|------|-----|
| 分类 | Python 第三方库 |
| 依赖名 | `torch`（Poetry 管理，项目锁定 2.12.0） |
| 导入写法 | `import torch` |
| 解决什么问题 | NumPy 数组只能跑 CPU，PyTorch Tensor 能跑 GPU 加速，是深度学习的基础设施 |
| 不负责什么 | 不负责模型下载和管理（那是 HuggingFace / SentenceTransformer 的职责） |
| 本章要求 | 认识并会用：创建 Tensor、设备迁移、和 NumPy 互转、`torch.cuda.synchronize()` |

## 1. 心智模型

PyTorch Tensor 就是**能跑 GPU 的 NumPy 数组**——语法和 NumPy 几乎一样，但多了 GPU 加速和自动求导。

## 2. 准确术语

- **`torch.Tensor`**：PyTorch 的核心类型，多维张量。和 `numpy.ndarray` 类似，但可以放在 GPU 上。
- **设备（Device）**：Tensor 所在的计算设备，`"cpu"` / `"cuda"` / `"mps"`。Tensor 必须先迁移到目标设备才能在该设备上运算。
- **异步提交**：CUDA 操作是异步的，CPU 提交指令后不等待 GPU 执行完毕就继续往下走。
- **`torch.cuda.synchronize()`**：强制 CPU 等待 GPU 把前面所有指令执行完，确保结果可用。

## 3. 边界

| 包含 | 不包含 |
|------|--------|
| Tensor 创建、索引、切片 | 神经网络层（`nn.Module`） |
| 设备迁移（`.to(device)`） | 训练循环（loss、optimizer） |
| GPU 加速运算 | 自动求导（`backward()`） |
| 和 NumPy 互转 | 模型保存加载（`torch.save`） |
| CUDA 同步 | 分布式训练 |

## 4. 最小可运行模板

```python
import torch

# 创建 Tensor
t = torch.tensor([1.0, 2.0, 3.0])

# 运算（和 NumPy 语法几乎一样）
result = t * 2  # tensor([2., 4., 6.])

# 迁移到 GPU（如果可用）
device = "cuda" if torch.cuda.is_available() else "cpu"
t = t.to(device)

# 迁移回 CPU + 转 NumPy
numpy_arr = t.cpu().numpy()
```

## 5. 为什么不用 NumPy

```python
# NumPy：只能跑 CPU，大矩阵运算慢
import numpy as np
a = np.random.rand(1000, 1000)
b = np.dot(a, a)  # CPU 逐核计算，约 50ms

# PyTorch：能跑 GPU，同样运算快 10~50 倍
import torch
a = torch.rand(1000, 1000, device="cuda")
b = torch.matmul(a, a)  # GPU 数千核心并行，约 1ms
```

NumPy 没有设备概念，所有运算都在 CPU 上。PyTorch Tensor 可以放在 GPU 上，利用 GPU 的数千个并行核心加速矩阵运算。

## 6. 核心操作

### 6.1 创建 Tensor

```python
import torch

# 从列表创建
t = torch.tensor([1.0, 2.0, 3.0])
# tensor([1., 2., 3.])

# 创建全零 Tensor
zeros = torch.zeros(512)  # 512 维全零

# 创建随机 Tensor
rand = torch.rand(3, 4)  # 3×4 随机矩阵

# 直接指定设备
t_cuda = torch.tensor([1.0, 2.0], device="cuda")
```

### 6.2 设备迁移

```python
t = torch.tensor([1.0, 2.0, 3.0])  # 默认在 CPU

# 迁移到 GPU
t = t.to("cuda")
# 或
t = t.cuda()

# 迁移回 CPU
t = t.to("cpu")
# 或
t = t.cpu()
```

**关键规则**：两个 Tensor 必须在**同一设备**上才能运算，否则报错：

```python
a = torch.tensor([1.0], device="cuda")
b = torch.tensor([2.0], device="cpu")
a + b  # ❌ RuntimeError: Expected all tensors on the same device
```

### 6.3 运算

```python
a = torch.tensor([1.0, 2.0, 3.0])

a * 2              # tensor([2., 4., 6.])
a + 1              # tensor([2., 3., 4.])
a ** 2             # tensor([1., 4., 9.])

# 两个 Tensor 运算
b = torch.tensor([4.0, 5.0, 6.0])
a + b              # tensor([5., 7., 9.])

# 矩阵乘法
m1 = torch.tensor([[1, 2], [3, 4]])
m2 = torch.tensor([[5, 6], [7, 8]])
torch.matmul(m1, m2)  # 2×2 矩阵乘法
```

### 6.4 聚合

```python
a = torch.tensor([1.0, 2.0, 3.0])

a.sum()    # tensor(6.)
a.mean()   # tensor(2.)
a.max()    # tensor(3.)
```

### 6.5 和 NumPy 互转

```python
import numpy as np

# NumPy → Tensor
arr = np.array([1.0, 2.0, 3.0])
t = torch.from_numpy(arr)  # 共享内存，不复制

# Tensor → NumPy（必须先迁回 CPU）
t = torch.tensor([1.0, 2.0, 3.0], device="cuda")
arr = t.cpu().numpy()  # GPU Tensor 不能直接 .numpy()
```

### 6.6 CUDA 异步与同步

```python
# CUDA 操作是异步的：提交指令后 CPU 不等待
t = torch.tensor([1.0, 2.0], device="cuda")
result = t * 2  # ← 几乎瞬间返回，GPU 可能在后台才算

# 强制等待 GPU 执行完
torch.cuda.synchronize()  # ← CPU 在这里阻塞，直到 GPU 完成
```

为什么需要同步？因为异步模式下，GPU 的错误不会立即抛出。如果不同步，你可能以为"成功了"，但实际 GPU 报错了，错误要等到后续某个操作才暴露。

## 7. 在本项目中的用法

### 7.1 设备检测

```python
# app/embedding.py _try_tensor 函数
def _try_tensor(device):
    try:
        tensor = torch.tensor([1.0, 2.0], device=device)  # 在目标设备创建 Tensor
        _ = tensor * 2                                      # 做一次运算
        if str(device).startswith("cuda"):
            torch.cuda.synchronize()                        # CUDA 需要同步确保真的执行了
        return True
    except Exception:
        return False
```

这是"冒烟测试"——不只是检查设备是否存在，而是**真正跑一下**确认能用。

### 7.2 SentenceTransformer 内部

```python
# SentenceTransformer 内部用 PyTorch Tensor 做 GPU 推理
# model.encode() 返回时用 convert_to_numpy=True 转成 NumPy 数组
model.encode("test", convert_to_numpy=True)
# 内部流程: CPU 文本 → Token → GPU Tensor → GPU 推理 → CPU NumPy 数组
```

### 7.3 MPS 支持（Apple Silicon）

```python
# app/embedding.py _detect_device 函数
if torch.backends.mps.is_available() and _try_tensor("mps"):
    info = {"tier": "mps", "device_str": "mps", ...}
```

MPS 是 Apple 自研的 GPU 加速后端，M1/M2/M3/M4 芯片可以用 `device="mps"` 做 GPU 加速。

## 8. 常见坑

### 坑 1：设备不匹配

```python
a = torch.tensor([1.0], device="cuda")
b = torch.tensor([2.0], device="cpu")
a + b  # ❌ RuntimeError: Expected all tensors on the same device

# ✅ 统一到同一设备
a + b.to("cuda")  # tensor([3.], device='cuda:0')
```

### 坑 2：忘了 .cpu() 就 .numpy()

```python
t = torch.tensor([1.0], device="cuda")
t.numpy()  # ❌ RuntimeError: Can't call numpy() on Tensor that requires grad

# ✅ 先迁回 CPU
t.cpu().numpy()  # array([1.], dtype=float32)
```

### 坑 3：CUDA 异步导致错误延迟

```python
t = torch.tensor([1.0], device="cuda")
result = t * 2  # 可能已经出错了，但 CPU 不知道
print("成功")    # 打印了"成功"，但 GPU 实际崩溃了
torch.cuda.synchronize()  # 这里才抛出异常
```

## 9. 和 NumPy 的关系

| | NumPy 数组 | PyTorch Tensor |
|---|---|---|
| 来源 | `import numpy as np` | `import torch` |
| 能跑 GPU | 不能 | 能 |
| 用途 | CPU 上的向量运算 | GPU 上的深度学习 |
| 互转 | `torch.from_numpy(arr)` | `tensor.cpu().numpy()` |
| 内存共享 | `from_numpy` 后两者共享内存 | 修改一个另一个也变 |
| 在项目中 | `convert_to_numpy=True` 输出 | SentenceTransformer 内部计算用 |

## 10. 常用 API 速查

| 方法 | 作用 | 示例 |
|------|------|------|
| `torch.tensor()` | 从列表创建 Tensor | `torch.tensor([1, 2, 3])` |
| `torch.zeros()` | 创建全零 Tensor | `torch.zeros(512)` |
| `torch.rand()` | 创建随机 Tensor | `torch.rand(3, 4)` |
| `.to(device)` | 迁移设备 | `t.to("cuda")` |
| `.cpu()` | 迁移回 CPU | `t.cpu()` |
| `.cuda()` | 迁移到 CUDA | `t.cuda()` |
| `.numpy()` | 转 NumPy 数组（必须先 .cpu()） | `t.cpu().numpy()` |
| `torch.matmul()` | 矩阵乘法 | `torch.matmul(a, b)` |
| `torch.cuda.synchronize()` | 等待 GPU 执行完 | `torch.cuda.synchronize()` |
| `.sum()` | 求和 | `t.sum()` |
| `.shape` | 查看形状 | `t.shape` |
| `torch.cuda.is_available()` | 检查 CUDA 是否可用 | `True / False` |

## 11. 检查点

验证四条理解标准：

1. **核心思想是什么？** PyTorch Tensor 是能跑 GPU 的多维数组，语法和 NumPy 几乎一样，但多了设备迁移和 GPU 加速能力。

2. **它解决什么问题？** NumPy 只能跑 CPU，大矩阵运算慢；PyTorch Tensor 放在 GPU 上，利用数千个并行核心加速运算。

3. **为什么不用常见替代方案？** NumPy 没有 GPU 支持；TensorFlow 有 GPU 但 API 更重、调试不直观（PyTorch 是动态图，更像写 Python）。

4. **在本项目里怎么实现或识别？** `app/embedding.py` 的 `_try_tensor` 用 `torch.tensor(device=...)` + `torch.cuda.synchronize()` 做设备冒烟测试；SentenceTransformer 内部用 PyTorch Tensor 做 GPU 推理，`convert_to_numpy=True` 把结果转回 NumPy。
