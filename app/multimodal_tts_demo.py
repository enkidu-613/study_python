"""第 35 章：使用 OpenRouter 的 TTS 接口把文本转换为音频。"""

from __future__ import annotations

import os
from pathlib import Path

import httpx
from dotenv import load_dotenv


load_dotenv()

OPENROUTER_BASE_URL = os.getenv(
    "OPENROUTER_BASE_URL",
    "https://openrouter.ai/api/v1",
)


def synthesize_speech(text: str, output_path: str | Path) -> Path:
    """调用 TTS 接口，并把返回的音频字节保存到文件。"""
    if not text.strip():
        raise ValueError("TTS 输入文本不能为空")

    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("TTS_MODEL")
    voice = os.getenv("TTS_VOICE")
    response_format = os.getenv("TTS_FORMAT", "mp3")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY 未配置")
    if not model:
        raise RuntimeError("TTS_MODEL 未配置")
    if not voice:
        raise RuntimeError("TTS_VOICE 未配置")

    payload = {
        "model": model,
        "input": text,
        "voice": voice,
        "response_format": response_format,
        "speed": float(os.getenv("TTS_SPEED", "1")),
    }

    with httpx.Client(timeout=60.0) as client:
        response = client.post(
            f"{OPENROUTER_BASE_URL}/audio/speech",
            headers={"Authorization": f"Bearer {api_key}"},
            json=payload,
        )
        response.raise_for_status()

    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(response.content)
    return target


def main() -> None:
    text = os.getenv("TTS_TEXT", "你好，这是一次文字转语音测试。")
    output_path = os.getenv("TTS_OUTPUT_PATH", "artifacts/tts-output.mp3")
    print(f"音频已保存到：{synthesize_speech(text, output_path)}")


if __name__ == "__main__":
    main()
