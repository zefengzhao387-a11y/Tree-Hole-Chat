<template>
  <div class="page">
    <header class="page-header stack">
      <h1 class="page-title">设置</h1>
      <p class="page-desc">配置 AI 与查看使用概况</p>
    </header>

    <div class="card pad section">
      <h2 class="section-label">账号</h2>
      <p class="hint" v-if="auth.user">当前用户：{{ auth.user.nickname || auth.user.username }}</p>
      <button class="btn btn-ghost" @click="logout">退出登录</button>
    </div>

    <div class="card pad section">
      <p class="hint">配置 API Key 以启用情感分析和树洞对话</p>
      <input v-model="key" type="password" class="input-heal" placeholder="sk-xxxxxxxx" />
      <button class="btn btn-primary" style="margin-top:12px" @click="saveKey">保存</button>
    </div>

    <div v-if="stats" class="card pad section">
      <h2 class="section-label">使用统计</h2>
      <div class="stats">
        <div class="stat"><b>{{ stats.diary_count }}</b><span>日记</span></div>
        <div class="stat"><b>{{ stats.analysis_count }}</b><span>分析</span></div>
        <div class="stat"><b>{{ stats.conversation_count }}</b><span>对话</span></div>
      </div>
    </div>

    <div class="card pad section about">
      <h2 class="section-label">关于</h2>
      <p>解忧树洞 v1.0</p>
      <p class="muted">Vue 3 · FastAPI · LangChain · Chroma · DeepSeek</p>
      <p class="motto">每一份心情，都值得被温柔以待</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '../api'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()

const key = ref('')
const stats = ref(null)

onMounted(async () => {
  key.value = localStorage.getItem('deepseek_api_key') || ''
  try {
    const { data } = await api.get('/system/stats')
    stats.value = data
  } catch { /* ignore */ }
})

function saveKey() {
  localStorage.setItem('deepseek_api_key', key.value)
  ElMessage.success('已保存')
}

function logout() {
  auth.logout()
  router.replace('/')
}
</script>

<style scoped>
.section { margin-bottom: 12px; }

.hint {
  font-family: var(--font-ui);
  font-size: 0.8125rem;
  color: var(--c-text-muted);
  margin-bottom: 12px;
}

.stats {
  display: flex;
  gap: 12px;
  margin-top: 4px;
}

.stat {
  flex: 1;
  text-align: center;
  padding: 16px;
  background: var(--c-bg);
  border-radius: var(--radius-sm);
}

.stat b {
  display: block;
  font-family: var(--font-handwrite);
  font-size: 1.625rem;
  font-weight: 400;
  color: var(--c-wood-deep);
}

.stat span {
  font-family: var(--font-ui);
  font-size: 0.75rem;
  color: var(--c-text-muted);
}

.about p {
  font-family: var(--font-ui);
  font-size: 0.875rem;
  color: var(--c-text-dim);
  line-height: 1.8;
}

.muted { color: var(--c-text-muted) !important; font-size: 0.8125rem !important; }

.motto {
  margin-top: 8px;
  font-family: var(--font-handwrite);
  font-size: 0.9375rem;
  font-style: normal;
  letter-spacing: 0.1em;
  color: var(--c-wood) !important;
}
</style>
