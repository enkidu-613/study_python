# 01. 文本进入模型：Token、Tokenizer 与 Pooling

> 定位：这是 AI 应用开发的模型机制基础，不是 Python 新手前置，也不是要求你现在手写 Transformer 的研究教程。

数学补充：[从数字到平均池化：一步一步看懂 20×768](/Users/enkidu/PyCharmMiscProject/md/ai学习应用数学/02_从数字到平均池化.md:1)。

## 一句话心智模型

```text
文本
→ Tokenizer 拆成 token
→ token 映射为 token ID
→ Transformer 为每个 token 产生隐藏表示
→ Pooling 汇总成一条文本向量
```

## 学习顺序

1. 先理解 token 不等于词。
2. 再理解 Tokenizer 如何把文字转换成模型输入。
3. 再区分 token ID、隐藏表示和句向量。
4. 最后理解 Pooling 为什么把多条 token 表示汇总成一条文本向量。

## 1. Token 不一定等于一个词

Token 是 Tokenizer 划分出的文本片段，可能是：

```text
完整词：   "退款"
汉字：     "退"
英文子词： "play" + "##ing"
标点：     "？"
特殊标记： "[CLS]"、"[SEP]"
```

不同模型的词表不同，所以同一段文本可能被拆成不同数量的 token。

准确边界：

```text
一个词 → 一个或多个 token
一个 token → 一条 token ID
一个 token → 一条隐藏向量
```

这里的“一个 token 对应一条隐藏向量”是本章的简化理解。Transformer 内部还会在不同层产生中间结果，但当前不展开。

## 2. Tokenizer 是什么

Tokenizer 是模型前面的文本预处理对象。它负责：

- 把文本拆成 token；
- 把 token 转成 token ID；
- 管理特殊 token；
- 按需要进行截断、填充并整理模型输入。

它不是模型本身，也不执行神经网络计算。

最小调用形状：

```python
from transformers import AutoTokenizer


model_id = "BAAI/bge-base-zh-v1.5"
tokenizer = AutoTokenizer.from_pretrained(model_id)
encoded = tokenizer("退款需要几天内申请？")

print(encoded["input_ids"])
```

数据变化：

```text
"退款需要几天内申请？"
  → tokenizer 拆分 token
  → input_ids: [一串整数]
  → 模型可以读取的输入字典
```

`encoded` 通常类似一个字典：

```python
{
    "input_ids": [...],
    "attention_mask": [...],
}
```

- `input_ids`：每个 token 在当前词表中的编号。
- `attention_mask`：告诉模型哪些位置是真实内容，哪些位置是填充位置。

必须使用与模型配套的 Tokenizer，因为模型训练时使用的词表和编号就是配套的。

## 3. Token ID 是什么

Token ID 是 token 在当前模型词表中的整数编号。

```text
token：    "退款"
词表查找： 1205
token ID：  1205
```

它只是索引，不是：

- token 的语义；
- 向量；
- 相似度分数；
- 编号越近就越相似的证明。

完整链路可以写成：

```text
原始文本
→ token
→ token ID
→ Transformer 输入
```

## 4. 隐藏表示是什么

Transformer 读取 `input_ids` 后，会为每个 token 产生一条浮点向量，称为隐藏表示（hidden representation，常见术语是 hidden state）。

```text
token ID 1 → 隐藏向量 1
token ID 2 → 隐藏向量 2
token ID 3 → 隐藏向量 3
```

隐藏表示和 token ID 的区别：

| 数据 | 形态 | 作用 |
| --- | --- | --- |
| token ID | 整数 | 词表中的输入编号。 |
| 隐藏表示 | 浮点数数组 | 模型计算后的上下文表示。 |

隐藏表示不是固定的“字典向量”。由于 Transformer 会处理上下文，同一个 token 放在不同句子里，隐藏表示可能不同。

## 5. Pooling 是什么

如果文本有 3 个 token，Transformer 可能产生 3 条隐藏向量：

```text
token 1 → [1, 2]
token 2 → [3, 4]
token 3 → [5, 6]
```

向量数据库希望一段文本对应一条固定长度向量，所以需要汇总：

```text
多条 token 隐藏向量
→ Pooling
→ 一条文本/句向量
```

最简单的平均池化：

```text
([1, 2] + [3, 4] + [5, 6]) / 3
→ [3, 4]
```

### 从最基础的数学重新走一遍

如果你忘记了线性代数，可以先只记住下面五级，不需要先学完整本数学教材。

#### 第 1 级：数字

```text
1、2、3、4、5、6
```

每一个都是一个数字。数字可以做加法和除法：

```text
1 + 3 + 5 = 9
9 / 3 = 3
```

#### 第 2 级：向量

把多个有顺序的数字放在一起，就是一个向量：

```text
[1, 2]
```

它有两个位置，也可以说它是一个 **2 维向量**：

```text
第 1 个维度 = 1
第 2 个维度 = 2
```

向量相加时，只把相同位置的数字相加：

```text
[1, 2] + [3, 4] = [1 + 3, 2 + 4] = [4, 6]
```

向量除以一个数字时，每个位置都除以这个数字：

```text
[9, 12] / 3 = [9 / 3, 12 / 3] = [3, 4]
```

#### 第 3 级：矩阵

把多条同样长度的向量上下排列，就得到一个矩阵：

```text
H = [
    [1, 2],
    [3, 4],
    [5, 6],
]
```

这个矩阵有：

```text
3 行 × 2 列
```

在本章中可以这样理解：

```text
每一行 = 一个 token 的隐藏向量
每一列 = 所有 token 的同一个特征位置
```

#### 第 4 级：行和列

上面的矩阵按行看：

```text
第 1 行：[1, 2]
第 2 行：[3, 4]
第 3 行：[5, 6]
```

按列看：

```text
第 1 列：[1, 3, 5]
第 2 列：[2, 4, 6]
```

“逐列求平均”就是先把每一列单独拿出来，再分别求平均。

#### 第 5 级：平均数

平均数的规则是：

```text
平均数 = 所有数的总和 / 数的个数
```

对第 1 列求平均：

```text
(1 + 3 + 5) / 3 = 9 / 3 = 3
```

对第 2 列求平均：

```text
(2 + 4 + 6) / 3 = 12 / 3 = 4
```

所以矩阵的逐列平均结果是：

```text
[3, 4]
```

这也可以先做向量加法，再除以向量数量：

```text
[1, 2] + [3, 4] + [5, 6]
= [9, 12]

[9, 12] / 3
= [3, 4]
```

### 逐列求平均的数学原理

把每个 token 的隐藏向量排成矩阵：每一行代表一个 token，每一列代表隐藏向量的一个特征维度。

```text
H = [
    [1, 2],  # token 1
    [3, 4],  # token 2
    [5, 6],  # token 3
]
```

这里 `H` 的形状是 `3 × 2`：3 个 token，2 个特征维度。逐列平均就是分别计算每一列的平均值：

```text
第 1 列：(1 + 3 + 5) / 3 = 3
第 2 列：(2 + 4 + 6) / 3 = 4

平均池化结果：[3, 4]
```

用公式表示，假设有 `n` 个 token，每条隐藏向量有 `d` 个维度：

```text
H ∈ R^(n × d)
v_j = (1 / n) × Σ H[i, j]，其中 i = 1...n
```

`v_j` 表示结果向量的第 `j` 个维度。也可以写成向量形式：

```text
v = (h_1 + h_2 + ... + h_n) / n
```

所以平均池化的形状变化是：

```text
n × d 的 token 矩阵 → d 维文本向量
```

“逐列”很重要：它只汇总不同 token 在同一个特征维度上的数值，不会把所有数字混成一个标量，也不会改变最终的隐藏维度 `d`。

不要把“列数”当成除数。假设矩阵形状是 `20 × 768`：

```text
20 行 = 20 个 token
768 列 = 每个 token 的 768 个特征维度
```

那么每一列都有 20 个数字，所以每一列都除以 `20`，最后得到 768 个平均值：

```text
第 1 列：20 个数字相加 / 20 → 结果的第 1 个维度
第 2 列：20 个数字相加 / 20 → 结果的第 2 个维度
...
第 768 列：20 个数字相加 / 20 → 结果的第 768 个维度
```

如果只有一行、但有 100 列，那只是一个 token 的 100 维向量，不需要做跨 token 的平均；把这一行的 100 个数字全部相加再除以 100，只会得到一个标量，不能作为 100 维句向量。

如果输入为了补齐长度包含填充 token，则不能把填充位置一起平均。实际实现会用 `attention_mask` 做带掩码的平均：

```text
v = Σ(mask_i × h_i) / Σ(mask_i)
```

真实 token 的 `mask_i` 通常为 `1`，填充 token 的 `mask_i` 为 `0`。因此填充向量不会影响最终句向量。

这里平均的是隐藏向量，不是 token ID。

常见策略：

- Mean Pooling：逐维求平均；
- CLS Pooling：取 `[CLS]` 特殊 token 的隐藏向量；
- Max Pooling：逐维取最大值。

### CLS Pooling 到底取什么

在一些 BERT 风格的模型中，Tokenizer 会在文本开头加入特殊 token：

```text
[CLS] 退款 需要 几天 [SEP]
```

Transformer 处理后，每个位置都会有一条隐藏向量：

```text
H[0] = [CLS] 位置的隐藏向量
H[1] = "退款" 的隐藏向量
H[2] = "需要" 的隐藏向量
H[3] = "几天" 的隐藏向量
H[4] = [SEP] 位置的隐藏向量
```

CLS Pooling 就是直接取第一个位置：

```text
sentence_vector = H[0]
```

这里取的是 `[CLS]` 位置经过 Transformer 计算后的**隐藏向量**，不是 `[CLS]` 的 token ID，也不是把文本截断成一个 token。由于 `[CLS]` 位置可以通过注意力读取其他 token 的信息，它的最终隐藏向量可以作为整段文本的表示。

`[CLS]` 的“特殊”不是说它天生就等于整段文本的摘要，而是：

- 它有专门的特殊 token ID 和初始向量；
- 它固定放在输入序列的开头；
- BERT 类模型的训练任务经常使用它的位置接分类层；
- 训练过程让这个位置逐渐学会收集整段文本的信息。

所以，`[CLS]` 最终隐藏向量能否很好地代表整段文本，取决于模型的架构、训练任务和池化配置。不能把任何模型第 0 个位置都自动叫作 `[CLS]` 向量。

`[SEP]` 是 **separator token**，意思是“分隔符”。它主要用来告诉模型一段文本在哪里结束，或两段文本在哪里分开：

```text
单段文本： [CLS] 退款需要几天 [SEP]

文本对：  [CLS] 问题文本 [SEP] 参考文本 [SEP]
```

`[SEP]` 也会有自己的隐藏向量，但通常不会拿它做 CLS Pooling。它更像文本结构中的边界标记，不是实际业务文字。

所以 Mean Pooling 和 CLS Pooling 的区别是：

```text
Mean Pooling：多个 token 的隐藏向量逐列平均
CLS Pooling：只取 [CLS] 位置的隐藏向量
```

不是所有模型都有 `[CLS]`，也不是所有模型都适合 CLS Pooling；具体策略要看模型架构和模型配置。使用 `SentenceTransformer` 时，通常由模型配置自动完成，你不需要手动取 `H[0]`。

不同长度的文本经过池化后，可以得到相同维度的向量：

```text
2 个 token  → 1 条 768 维向量
20 个 token → 1 条 768 维向量
```

使用 `SentenceTransformer` 时，池化通常已经在模型配置中封装好了：

```python
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("BAAI/bge-base-zh-v1.5")
embedding = model.encode("退款需要几天内申请？")
```

你调用的是 `encode()`，不需要自己手写 Tokenizer、Transformer 和 Pooling 的组合。

## 6. 与 RAG 的关系

```text
文档 chunk
  → Embedding 模型
  → 一条 chunk 向量
  → 向量数据库

用户问题
  → 同一套兼容的 Embedding 模型
  → 一条 query 向量
  → 相似度检索
```

因此，建库和查询必须保持兼容：

- 模型 ID；
- 模型版本；
- Tokenizer；
- 预处理策略；
- Pooling 和归一化策略。

不能把 token ID 直接当作 RAG 向量，也不能把不同模型产生的隐藏表示随意放进同一个向量索引。

## 7. 本文不展开

当前只需识别，不要求推导或手写：

- Attention 的矩阵计算；
- Transformer 每一层的内部结构；
- 自定义 Tokenizer 训练；
- 从 `AutoModel` 手写完整 Embedding 模型；
- BPE、WordPiece、SentencePiece 的算法细节。

这些内容属于更底层的模型原理，不阻塞你完成 AI 应用开发。

## 四条理解检查

1. Token 是否一定等于词？为什么？
2. Tokenizer、token ID 和隐藏表示分别处在哪一步？
3. 为什么需要 Pooling？平均的到底是什么？
4. 为什么 RAG 建库和查询要使用兼容的模型与处理策略？

## 权威来源

- [Hugging Face Tokenizer 官方文档](https://huggingface.co/docs/transformers/main/en/main_classes/tokenizer)
- [Sentence Transformers 官方 API](https://www.sbert.net/docs/package_reference/sentence_transformer/model.html)
- [BGE 中文模型卡](https://huggingface.co/BAAI/bge-base-zh-v1.5)
