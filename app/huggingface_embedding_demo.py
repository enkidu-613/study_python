"""第 32 章：Hugging Face 本地 Embedding 最小可运行示例。"""

from sentence_transformers import SentenceTransformer #用来创建句向量模型对象，创建时加载制定模型，实例随后可以调用encode
# 句向量模型中的句不只表示语法上的句子，句向量模型会把一段具有整体含义的文本转换成向量。
# sentence-transformers poetry管理的第三方包，也是项目直接依赖
# 本章引用的类是SentenceTransformer类，使用该类实例的通用方法是encode，业务作用是将句子和文档转为适合的向量



MODEL_ID = "BAAI/bge-base-zh-v1.5" #制定HUB上的模型仓库
TEXT = [
    "退款需要几天内申请？",
    "用户应该在七天内提交退款申请。",
]


def main() -> None:
    model = SentenceTransformer(MODEL_ID, device="mps") #SentenceTransformer实例，已加载、可以执行推理的本地模型对象
    embedding = model.encode(TEXT, convert_to_numpy=True) #当前文本经过模型计算后得到的一维向量

    print(f"model_id: {MODEL_ID}")
    print(f"model_type: {type(model).__name__}")
    print(f"embedding_type: {type(embedding).__name__}")
    print(f"embedding_shape: {embedding.shape}")
    print(f"embedding_preview: {embedding[:5]}")


if __name__ == "__main__":
    main()
