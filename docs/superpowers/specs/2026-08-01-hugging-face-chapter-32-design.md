# 第 32 章 Hugging Face 生态教学优化设计

## 目标

把 `md/32_HuggingFace生态.md` 从“调用项目已有的 AI 生成封装”调整为“先亲手写出最小模型加载代码，再看懂项目封装”。章节仍然聚焦 Hugging Face 生态和预训练模型使用，不扩展为设备兼容或并发编程课程。

## 学习起点

`app/embedding.py` 是当前项目资产，但由 AI 辅助生成，不能据此推断学习者已经掌握模型加载、设备选择、缓存和回退。教程必须把“能够运行已有函数”和“能够独立写出最小实现”分开评价。

## 章节结构

1. 声明学习起点和本章掌握边界。
2. 介绍本章首次实际使用的三个第三方包及其职责和项目版本。
3. 学习者亲手跟写最小 `SentenceTransformer` 加载与 `encode()` 推理代码。
4. 通过修改文本和查看 `shape` 验证模型确实执行。
5. 按真实调用链阅读 `app/embedding.py`：模型配置、设备检测、模型选择、加载、缓存、单条和批量编码。
6. 区分必须会写、必须看懂和只需识别的内容。
7. 补充模型 ID、revision、向量维度和预处理一致性，以及更换模型后重新建立向量索引的边界。
8. 保留 `pipeline()`、模型卡和 `InferenceClient`，但将其放在本地 Embedding 主线之后，并明确本章掌握程度。
9. 用读懂、跟写、独立重写三遍练习验证学习结果。

## 掌握边界

学习者必须能够独立写出：模型 ID、`SentenceTransformer(...)`、`model.encode(...)`、输出类型和维度检查，以及一个最小 `get_embedding_demo(text)` 函数。

学习者必须能够看懂：`TIER_DISPATCH`、`_get_model_name()`、`_load_model()`、`get_embedding_model()`、`get_embedding()` 和 `get_embeddings()` 的调用关系。

学习者本章只需识别：CUDA/MPS/DirectML 的完整检测细节、双重检查锁、显存异常回退和跨平台兼容实现，不要求从零重写。

## 内容修正

- 不再把项目实现描述为固定的 `bge-base + mps`。
- 使用项目真实调用链解释不同设备可能选择不同模型。
- 说明 `bge-small`、`bge-base`、`bge-large` 的向量维度不同。
- 说明建库和查询必须保持模型、版本、维度和预处理一致。
- 说明模块级 `_model` 只在当前 Python 进程中复用。
- 区分本地 `SentenceTransformer`、Transformers `pipeline()`、远程 `InferenceClient` 和 TEI 向量服务。

## 验证方式

- 检查文档中的代码和 `app/embedding.py` 当前实现一致。
- 使用项目 Poetry 环境验证关键导入与最小代码形状。
- 检查所有本地文件链接和命令。
- 执行 Markdown 差异检查和 `git diff --check`。
- 最终练习必须包含实际运行验证，不能只要求填写模型资料或回答概念题。

## 修改范围

只修改 `md/32_HuggingFace生态.md`。不修改 `app/embedding.py`、前序章节、试卷、错题本和学习状态。
