"""第 34 章：使用 OpenRouter 的 STT 接口把音频转换为文本。"""

from __future__ import annotations

import base64
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv


load_dotenv()

OPENROUTER_BASE_URL = os.getenv(
    "OPENROUTER_BASE_URL",
    "https://openrouter.ai/api/v1",
)
DEFAULT_MAX_AUDIO_BYTES = 20 * 1024 * 1024


def _read_audio_as_base64(audio_path: Path, max_bytes: int) -> tuple[str, str]:
    """读取音频，并返回 base64 数据和不带点号的格式名。"""
    if not audio_path.is_file():
        raise FileNotFoundError(f"音频文件不存在：{audio_path}")

    audio_bytes = audio_path.read_bytes()
    if not audio_bytes:
        raise ValueError("音频文件为空")
    if len(audio_bytes) > max_bytes:
        raise ValueError(f"音频超过大小限制：{max_bytes} bytes")

    audio_format = audio_path.suffix.lower().lstrip(".")
    allowed_formats = {"wav", "mp3", "flac", "m4a", "ogg", "webm", "aac"}
    if audio_format not in allowed_formats:
        raise ValueError(f"暂不支持的音频格式：{audio_format or '未知'}")

    return base64.b64encode(audio_bytes).decode("ascii"), audio_format


def transcribe_audio(audio_path: str | Path) -> str:
    """调用 STT 接口，把本地音频转换为文本。"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("STT_MODEL")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY 未配置")
    if not model:
        raise RuntimeError("STT_MODEL 未配置")

    encoded_audio, audio_format = _read_audio_as_base64(
        Path(audio_path),
        int(os.getenv("STT_MAX_AUDIO_BYTES", DEFAULT_MAX_AUDIO_BYTES)),
    )
    payload = {
        "model": model,
        "input_audio": {
            "data": encoded_audio,
            "format": audio_format,
        },
        "language": os.getenv("STT_LANGUAGE", "zh"),
    }

    with httpx.Client(timeout=60.0) as client:
        response = client.post(
            f"{OPENROUTER_BASE_URL}/audio/transcriptions",
            headers={"Authorization": f"Bearer {api_key}"},
            json=payload,
        )
        response.raise_for_status()

    result = response.json()
    transcript = result.get("text")
    if not isinstance(transcript, str) or not transcript.strip():
        raise RuntimeError("STT 响应中没有有效的 text")
    return transcript.strip()


def main() -> None:
    audio_path = os.getenv("STT_AUDIO_PATH", "samples/voice.wav")
    print(transcribe_audio(audio_path))


if __name__ == "__main__":
    main()
