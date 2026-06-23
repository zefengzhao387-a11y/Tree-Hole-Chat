# 解忧树洞 API 契约

> **那亮** 按本文实现后端 · **郝昡** 按本文对接前端  
> 变更接口必须先改此文件，并在群里 @ 另一人。

Base URL（开发）：`/api`（Vite 代理到 `http://127.0.0.1:8000`）

鉴权：除注册/登录外，请求头 `Authorization: Bearer <token>`

---

## 认证

### POST `/auth/register`

```json
// Request
{ "username": "string", "password": "string" }
// Response 201
{ "id": 1, "username": "demo" }
```

### POST `/auth/login`

```json
// Request
{ "username": "string", "password": "string" }
// Response 200
{ "access_token": "jwt...", "token_type": "bearer" }
```

### GET `/auth/me`

```json
// Response 200
{ "id": 1, "username": "demo" }
```

---

## 日记

### GET `/diary?page=1&page_size=20`

```json
// Response 200
{
  "items": [
    {
      "id": 1,
      "title": "标题",
      "content": "正文",
      "mood_label": "平静",
      "created_at": "2026-06-23T10:00:00"
    }
  ],
  "total": 1
}
```

### POST `/diary`

```json
// Request
{ "title": "string", "content": "string" }
// Response 201 → 同单条日记对象，并触发情感分析 + 向量入库
```

### GET `/diary/{id}` · PUT `/diary/{id}` · DELETE `/diary/{id}`

（那亮实现时补充字段，与列表 item 结构一致）

---

## 情感分析

### GET `/analysis/trend?days=30`

```json
// Response 200
{
  "dates": ["2026-06-01", "..."],
  "scores": [0.6, "..."],
  "labels": ["平静", "..."]
}
```

### GET `/analysis/report`

```json
// Response 200
{ "summary": "本周整体情绪…", "suggestion": "建议…" }
```

---

## 树洞对话

### POST `/chat/send`

- Content-Type: `application/json`
- Response: `text/event-stream`

```json
// Request
{ "message": "最近有点焦虑" }
// SSE data 示例
data: {"token": "我"}
data: {"token": "理解"}
data: [DONE]
```

### GET `/chat/history`

```json
// Response 200
{
  "messages": [
    { "role": "user", "content": "...", "created_at": "..." },
    { "role": "assistant", "content": "...", "created_at": "..." }
  ]
}
```

### DELETE `/chat/history`

```json
// Response 204 无 body
```

---

## 错误格式（统一）

```json
{ "detail": "错误说明" }
```

| 状态码 | 含义 |
|--------|------|
| 401 | 未登录 / Token 失效 |
| 403 | 无权限访问他人数据 |
| 404 | 资源不存在 |
| 422 | 参数校验失败 |

---

*实现细节以后端 Swagger `/docs` 为准；本文与 Swagger 冲突时，以群里确认后的 `api.md` 为准。*
