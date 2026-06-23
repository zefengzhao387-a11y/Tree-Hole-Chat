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
| **部署** | Docker + docker-compose / Vercel + Railway |

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

## ☁️ 云端部署（Vercel 前端 + Railway 后端）

推荐架构：前端静态页放 **Vercel**，FastAPI + SQLite + Chroma 放 **Railway**（数据也在 Railway 磁盘上，是「云上的 SQLite 文件」）。

```
浏览器 → Vercel（Vue） → Railway（FastAPI + data/diary.db + chroma_db/）
```

### 第一步：部署后端到 Railway

1. 打开 [Railway](https://railway.app)，用 GitHub 导入本仓库
2. 新建 Service → **Root Directory 选 `backend`**
3. Railway 会读取 `backend/Dockerfile` 构建镜像
4. 在 **Variables** 里配置环境变量：

| 变量 | 示例 | 说明 |
|------|------|------|
| `DEEPSEEK_API_KEY` | `sk-xxx` | DeepSeek 密钥 |
| `DATABASE_URL` | `sqlite+aiosqlite:///./data/diary.db` | 默认即可 |
| `CHROMA_PERSIST_DIRECTORY` | `./data/chroma_db` | 默认即可 |
| `JWT_SECRET` | 随机长字符串 | 生产必改 |
| `CORS_ORIGINS` | `https://xxx.vercel.app` | 部署前端后填入 Vercel 域名 |

5. **挂载持久卷（重要）**：Service → Settings → Volumes → 添加 Volume，挂载到 `/app/data`  
   否则重新部署后 SQLite 和 Chroma 数据会丢失。
6. 部署完成后复制公网地址，例如 `https://treehole-api.up.railway.app`
7. 浏览器访问 `https://treehole-api.up.railway.app/api/system/health`，应返回 `{"status":"ok",...}`

> Render 同理：选 Docker 部署、`backend` 目录、挂载 `/app/data`、配置相同环境变量。平台会注入 `PORT`，Dockerfile 已支持。

### 第二步：部署前端到 Vercel

1. 打开 [Vercel](https://vercel.com)，导入同一 GitHub 仓库
2. **Root Directory 选 `frontend`**
3. Framework Preset：**Vite**（Build: `npm run build`，Output: `dist`）
4. 在 **Environment Variables** 添加：

| 变量 | 值 |
|------|-----|
| `VITE_API_BASE_URL` | `https://treehole-api.up.railway.app/api` |

注意：末尾要带 `/api`，与本地开发 axios 的 baseURL 一致。

5. Deploy。`frontend/vercel.json` 已配置 SPA 路由，刷新子页面不会 404。

### 第三步：回填 CORS

前端部署完成后，把 Vercel 域名（如 `https://treehole.vercel.app`）写回 Railway 的 `CORS_ORIGINS`，重新部署后端。

### 本地开发与线上差异

| 环境 | API 地址 |
|------|----------|
| 本地 | 不配置 `VITE_API_BASE_URL`，走 Vite 代理 `/api` → `127.0.0.1:8000` |
| Vercel | `VITE_API_BASE_URL=https://你的后端/api` |

树洞对话的 SSE 请求（`chat.js`）同样使用该变量，无需额外配置。

## ☁️ 云端部署（前后端都在 Railway）

同一仓库里建 **两个 Service**，都在 Railway 上，不必再用 Vercel。

```
浏览器 → Railway 前端 Service（Nginx 静态页）
              ↓ 直连 HTTPS
         Railway 后端 Service（FastAPI + SQLite + Chroma）
```

### 和 Vercel 方案的区别

| | Vercel + Railway | 全 Railway |
|---|---|---|
| 前端 | Vercel 托管静态文件 | Railway Docker（Nginx） |
| 后端 | Railway | Railway |
| 公网地址 | 两个域名 | 两个域名（或自定义域名） |
| 配置 | 前端 `VITE_API_BASE_URL` | 同样要设，且在 **构建时** 生效 |

### 第一步：部署后端

与上文相同：

1. New Service → Root Directory = **`backend`**
2. 环境变量：`DEEPSEEK_API_KEY`、`JWT_SECRET` 等
3. Volume 挂载 **`/app/data`**
4. 记下公网地址，例如 `https://treehole-api.up.railway.app`
5. 验证 `/api/system/health`

### 第二步：部署前端

1. 同一 Project 里再 **New Service** → Root Directory = **`frontend`**
2. 在 **Variables** 添加（Railway 会在 Docker 构建时传给 Vite）：

| 变量 | 值 |
|------|-----|
| `VITE_API_BASE_URL` | `https://treehole-api.up.railway.app/api` |

3. Deploy。访问前端公网地址即可。

> 前端 Dockerfile 已支持构建期注入 `VITE_API_BASE_URL`。不设则默认 `/api`（适合 docker-compose 本地一键部署，由 Nginx 反代到 `backend:8000`）。

### 第三步：回填 CORS

后端 Variables 增加：

```
CORS_ORIGINS=https://你的前端.up.railway.app
```

重新部署后端。

### 可选：只暴露一个域名

若希望用户只访问一个 URL，可改 Nginx 把 `/api` 反代到后端 **Railway 内网地址**（Private Networking），前端构建时不设 `VITE_API_BASE_URL`。这需要改 Nginx 配置，课程演示用 **两个 Service + 两个域名** 更简单。

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
