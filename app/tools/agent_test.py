import json
from app.tools.registry import TOOLS, TOOL_FUNCTIONS
from pydantic import BaseModel


class FunctionCall(BaseModel):
    name: str
    arguments: str  # OpenAI tool call 的 arguments 是 JSON 字符串


class ToolCall(BaseModel):
    function: FunctionCall


def run_tools_call(tool_call: ToolCall) -> dict:
    tool_name = tool_call.function.name
    raw_args = tool_call.function.arguments
    tool_args = json.loads(raw_args)

    if tool_name not in TOOL_FUNCTIONS:
        raise ValueError(f"Tool '{tool_name}' is not registered.")

    tool_function = TOOL_FUNCTIONS[tool_name]
    result = tool_function(**tool_args)
    return result


tool_call_data = ToolCall(
    function=FunctionCall(
        name="search_knowledge_base",
        arguments=json.dumps({"query": "秦始皇是哪里人？", "limit": 3}),
    )
)
print(run_tools_call(tool_call_data))
