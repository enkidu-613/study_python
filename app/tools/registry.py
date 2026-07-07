from app.tools.knowledge_base import search_knowledge_base

TOOLS = [ #是把所有的工具说明书集合为一个列表，发给大模型查阅得到工具的使用方法
    {
        "name": "search_knowledge_base",
        "description": "在知识库中搜索相关文档切片，并返回结果列表。",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "要搜索的查询字符串。"
                },
                "limit": {
                    "type": "integer",
                    "description": "返回的结果数量限制。"
                }
            },
            "required": ["query"]
        }
    }
]

TOOL_FUNCTIONS = { #后端自己使用的工具列表
    "search_knowledge_base": search_knowledge_base
}
# 一句话 tools 给模型看， tools_functions 给后端使用