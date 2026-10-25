/** 第 45 章：读取现有 POST /ai/chat 返回的 SSE 事件。 */

export type AiStreamEvent = {
  type: "thinking" | "divider" | "answer";
  content: string;
};

export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

type StreamAiChatOptions = {
  apiBaseUrl: string;
  message: string;
  signal: AbortSignal;
  onEvent: (event: AiStreamEvent) => void;
};

export async function streamAiChat({
  apiBaseUrl,
  message,
  signal,
  onEvent,
}: StreamAiChatOptions): Promise<void> {
  const response = await fetch(`${apiBaseUrl}/ai/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
    signal,
  });

  if (!response.ok) {
    throw new ApiError("AI 对话请求失败", response.status);
  }
  if (!response.body) {
    throw new Error("浏览器没有返回可读取的响应流");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const blocks = buffer.split("\n\n");
    buffer = blocks.pop() ?? "";

    for (const block of blocks) {
      const dataLine = block
        .split("\n")
        .find((line) => line.startsWith("data: "));
      if (!dataLine) continue;
      onEvent(JSON.parse(dataLine.slice(6)) as AiStreamEvent);
    }
  }
}
