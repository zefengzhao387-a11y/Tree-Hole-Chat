# 🌳 解忧树洞 — 基于 LangChain 的个人日记情感分析与对话系统

> 《软件工程专业方向综合实习》人工智能Ⅰ方向 课程设计

## 📖 项目简介

解忧树洞是一个基于 **LangChain + RAG** 的个人日记情感分析与智能对话系统。用户可以：

- ✍️ **记录日记** — 随时记录生活点滴和心情
- 🎯 **情感分析** — LLM 自动分析每篇日记的情绪维度
- 🌳 **树洞对话** — 基于历史日记的 RAG 智能树洞，温暖共情地陪伴聊天
- 📈 **情感趋势** — 可视化展示情绪变化，生成情感报告

## 🏗️ 技术架构

```
前端 (Vue 3 + Element Plus)  ←→  后端 (FastAPI + LangChain)  ←→  DeepSeek API
                                      ↓
                              Chroma 向量数据库 (RAG)
                                      ↓
                              SQLite (日记/对话存储)
```

## 🛠️ 技术栈

| 层次 | 技术 |
|------|------|
| **LLM** | DeepSeek API (deepseek-chat) |
| **Embedding** | BGE-small-zh (HuggingFace) |
| **RAG框架** | LangChain + Chroma |
| **后端** | FastAPI + SQLAlchemy + SSE |
| **前端** | Vue 3 + Vite + Element Plus + ECharts |
| **部署** | Docker + docker-compose |

## 🚀 快速开始

### 前置要求

- Python 3.10+
- Node.js 18+
- DeepSeek API Key（[注册获取](https://platform.deepseek.com/)）

### 方法一：本地运行

```bash
# 1. 克隆项目
cd 个人日记情感分析与解忧树洞对话系统

# 2. 配置 API Key
cp backend/.env.example backend/.env
# 编辑 backend/.env，填入 DEEPSEEK_API_KEY=sk-xxxx

# 3. 安装后端依赖
cd backend
pip install -r requirements.txt

# 4. 启动后端
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 5. 新终端，安装前端依赖
cd frontend
npm install

# 6. 启动前端
npm run dev
```

访问：
- 前端：http://localhost:5173
- API 文档：http://localhost:8000/docs

### 方法二：Docker 部署

```bash
# 设置环境变量
export DEEPSEEK_API_KEY=sk-xxxx

# 一键启动
docker-compose up -d

# 访问 http://localhost:5173
```

## 📁 项目结构

```
├── backend/                    # 后端 Python 项目
│   ├── app/
│   │   ├── main.py            # FastAPI 入口
│   │   ├── config.py          # 配置管理
│   │   ├── database.py        # SQLite 数据库
│   │   ├── models/            # 数据模型 (Diary, EmotionAnalysis, Conversation)
│   │   ├── schemas/           # Pydantic 请求/响应模型
│   │   ├── routers/           # API 路由 (diary, analysis, chat)
│   │   ├── services/          # 业务逻辑 (diary, emotion, chat)
│   │   └── rag/               # LangChain RAG 模块
│   │       ├── embeddings.py  # Embedding 封装
│   │       ├── loader.py      # Document Loader
│   │       ├── splitter.py    # Text Splitter
│   │       ├── vector_store.py # Chroma 向量存储
│   │       ├── retriever.py   # 混合检索 + Re-ranking
│   │       ├── prompts.py     # Prompt Templates
│   │       └── chain.py       # RAG Chain + 情感分析
│   ├── tests/                 # 单元测试
│   └── Dockerfile
├── frontend/                   # 前端 Vue 3 项目
│   ├── src/
│   │   ├── views/             # 页面 (DiaryList, TreeHoleChat, EmotionTrend, Settings)
│   │   ├── components/        # 组件 (NavBar, EmotionBadge, ChatBubble, EmotionChart)
│   │   ├── api/               # API 封装
│   │   ├── stores/            # Pinia 状态管理
│   │   └── router/            # Vue Router
│   └── Dockerfile
├── docker-compose.yml         # Docker 编排
└── README.md
```

## 📡 API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/diary` | 日记列表（分页+筛选） |
| POST | `/api/diary` | 创建日记（自动分析+向量化） |
| GET/PUT/DELETE | `/api/diary/{id}` | 日记详情/更新/删除 |
| POST | `/api/analysis/{id}` | 执行情感分析 |
| GET | `/api/analysis/trend` | 情感趋势数据 |
| GET | `/api/analysis/report` | 情感分析报告 |
| POST | `/api/chat/send` | 树洞对话（SSE流式） |
| GET | `/api/chat/history` | 对话历史 |
| DELETE | `/api/chat/history` | 清空对话 |

## 🎓 课程知识点覆盖

- ✅ LangChain 核心组件（Model I/O、Prompt Templates、Chains、Memory）
- ✅ RAG Pipeline（Document Loader → Text Splitter → Embedding → Vector Store → Retrieval）
- ✅ Advanced RAG（Query Rewrite + Hybrid Search + Re-ranking）
- ✅ 向量数据库（Chroma）
- ✅ FastAPI 流式输出（SSE）
- ✅ Docker 容器化部署
- ✅ LLM 应用开发最佳实践

## 📝 License

本项目仅用于课程学习目的。
