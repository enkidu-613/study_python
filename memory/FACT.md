# 项目持久知识

## 用户画像
- ADHD 学习者，偏好：类比、视觉化（流程图/表格）、详细解释、循序渐进
- 数学基础较弱，需要逐步直观解释
- 已掌握：Python 基础、FastAPI + SQLAlchemy、代码分层与模块化
- 当前阶段：RAG 入门（已完成 Embedding 和余弦相似度概念理解）
- 技能层级：TIER 0-2 已掌握，即将进入 TIER 3（RAG/Agent/MCP）

## 项目偏好
- 包管理器：首选 Poetry，备选 pip
- 代码风格：学习代码，注释需要详细保留
- 文档格式：ADHD 友好的 Markdown（分段、表格、流程图、速查表）

## 项目结构
- `md/` 文件夹：包含 7 个学习文档（00-06）+ 代码分层文档（07）
- `.trae/memory/` ：旧记忆系统（project_overview、code_patterns、learning_notes、conversations）
- `py_ORM.py`：FastAPI + SQLAlchemy 学习代码
- 已实现代码分层：routers.py / models.py / schemas.py / database.py / main.py

## 关键学习节点
- IoC/DI 深入理解（yield vs return、依赖注入）
- APIRouter 工作原理（prefix、tags、include_router）
- Embedding = 给文字颁发"语义身份证"
- 余弦相似度 = 比方向不比长度（norm 归一化）
- 向量数据库 vs 关系型数据库（ANN vs LIKE）

## 下一步学习路线
1. RAG 第一周：向量数据库（当前 - 运行 Embedding 脚本）
2. RAG 第二周：LangChain 集成
3. 前端框架基础 (React/Vue)
4. 前后端对接
5. 用户认证 (JWT)
6. 项目部署 (Docker)