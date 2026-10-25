"""第 33 章：使用项目现有模型配置发送一次图像理解请求。"""

import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import SecretStr


load_dotenv()

IMAGE_URL = os.getenv(
    "VISION_IMAGE_URL",
    "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/bee.jpg",
).strip()


def build_vision_llm() -> ChatOpenAI:
    """创建视觉模型客户端。

    本示例不根据模型名称猜测供应商；模型、API 地址和密钥都由视觉配置明确提供。
    """
    model_name = os.getenv("VISION_MODEL_NAME", "").strip()
    if not model_name:
        raise RuntimeError("VISION_MODEL_NAME 未配置")

    api_key = os.getenv("VISION_API_KEY", "").strip()
    api_base = os.getenv("VISION_API_BASE", "").strip()

    if not api_key:
        raise RuntimeError("VISION_API_KEY 未配置")
    if not api_base:
        raise RuntimeError("VISION_API_BASE 未配置")

    return ChatOpenAI(
        model=model_name,
        base_url=api_base,
        api_key=SecretStr(api_key),
        temperature=0,
        streaming=False,
    )


def main() -> None:
    if not IMAGE_URL:
        raise RuntimeError("VISION_IMAGE_URL 未配置")

    model = build_vision_llm()  # 构建视觉模型实例

    message = HumanMessage(
        # 构建一个图片+文字的多模态消息
        content=[
            {
                "type": "text",
                "text": "请描述图片中的主要对象，并说明你最确定和最不确定的内容。",
            },
            {
                "type": "image_url",
                "image_url": {"url": IMAGE_URL},
            },
        ]
    )

    response = model.invoke([message])
    print(response.content)


if __name__ == "__main__":
    main()
