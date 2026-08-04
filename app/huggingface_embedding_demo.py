"""第 32 章：Hugging Face 本地 Embedding 最小可运行示例。"""

from sentence_transformers import SentenceTransformer


MODEL_ID = "BAAI/bge-base-zh-v1.5"
TEXT = "退款需要几天内申请？"


def main() -> None:
    model = SentenceTransformer(MODEL_ID, device="mps")
    embedding = model.encode(TEXT, convert_to_numpy=True)

    print(f"model_id: {MODEL_ID}")
    print(f"model_type: {type(model).__name__}")
    print(f"embedding_type: {type(embedding).__name__}")
    print(f"embedding_shape: {embedding.shape}")
    print(f"embedding_preview: {embedding[:5]}")


if __name__ == "__main__":
    main()
