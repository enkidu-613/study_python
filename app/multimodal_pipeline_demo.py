"""第 36 章：语音输入 -> 文本模型 -> 语音输出的最小串联。"""

from __future__ import annotations

import os
from pathlib import Path

import httpx
from dotenv import load_dotenv

from app.multimodal_stt_demo import transcribe_audio
from app.multimodal_tts_demo import synthesize_speech


load_dotenv()

OPENROUTER_BASE_URL = os.getenv(
    "OPENROUTER_BASE_URL",
    "https://openrouter.ai/api/v1",
)


def answer_with_text_model(question: str) -> str:
    """调用文本模型；真实项目中可替换为已有 RAG 或 Agent。"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("TEXT_MODEL")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY 未配置")
    if not model:
        raise RuntimeError("TEXT_MODEL 未配置")

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "请用简洁、准确的中文回答用户问题。",
            },
            {"role": "user", "content": question},
        ],
    }
    with httpx.Client(timeout=60.0) as client:
        response = client.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json=payload,
        )
        response.raise_for_status()

    result = response.json()
    answer = result.get("choices", [{}])[0].get("message", {}).get("content")
    if not isinstance(answer, str) or not answer.strip():
        raise RuntimeError("文本模型响应中没有有效的 content")
    return answer.strip()


def run_voice_question(audio_path: str | Path, output_path: str | Path) -> str:
    """完成语音输入、文本回答和语音输出，返回文本答案。"""
    transcript = transcribe_audio(audio_path)

    # 这里可以替换为已有的 RAG 或 Agent：answer_with_existing_rag(transcript)
    answer_text = answer_with_text_model(transcript)
    synthesize_speech(answer_text, output_path)
    return answer_text


def main() -> None:
    audio_path = os.getenv("PIPELINE_AUDIO_PATH", "samples/voice.wav")
    output_path = os.getenv("PIPELINE_OUTPUT_PATH", "artifacts/voice-answer.mp3")
    answer = run_voice_question(audio_path, output_path)
    print(f"文字答案：{answer}")
    print(f"语音答案：{Path(output_path)}")


if __name__ == "__main__":
    main()
