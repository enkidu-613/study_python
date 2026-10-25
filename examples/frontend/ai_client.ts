/**
 * 第 44 章的浏览器端请求模板。
 * 放进 Vue / React 项目后，传入 VITE_API_BASE_URL 等实际配置。
 */

export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

type AskDifyInput = {
  question: string;
};

export async function askDifyWorkflow(
  apiBaseUrl: string,
  accessToken: string,
  question: string,
): Promise<string> {
  const payload: AskDifyInput = { question };
  const response = await fetch(`${apiBaseUrl}/dify/rag`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new ApiError("Dify 工作流请求失败", response.status);
  }

  const data: unknown = await response.json();
  if (typeof data !== "string") {
    throw new Error("后端返回的 Dify 答案不是字符串");
  }
  return data;
}
