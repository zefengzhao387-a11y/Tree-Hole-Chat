<template>
  <div class="auth-page paper-bg">
    <div class="auth-card card pad">
      <router-link to="/" class="back-home">
        <svg class="back-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M14 6 L8 12 L14 18" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" />
          <path d="M8 12 H18" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" />
        </svg>
        <span class="back-text">返回首页</span>
        <span class="back-leaf" aria-hidden="true" />
      </router-link>

      <header class="auth-head">
        <img src="/logo.png" alt="解忧树洞" class="auth-logo" />
        <BlurText tag="h1" text="进入树洞" animate-by="chars" :delay="90" />
        <p>登录或注册后，开始记录与倾诉</p>
      </header>

      <FadeContent :delay="300" direction="up">
      <div class="tabs">
        <button :class="{ active: mode === 'login' }" @click="mode = 'login'">登录</button>
        <button :class="{ active: mode === 'register' }" @click="mode = 'register'">注册</button>
      </div>

      <form class="form" @submit.prevent="submit">
        <div class="field">
          <label class="label">用户名</label>
          <input v-model="form.username" class="input-heal" placeholder="3–50 个字符" required />
        </div>

        <div v-if="mode === 'register'" class="field">
          <label class="label">昵称（可选）</label>
          <input v-model="form.nickname" class="input-heal" placeholder="显示名称" />
        </div>

        <div class="field">
          <label class="label">密码</label>
          <input v-model="form.password" type="password" class="input-heal" placeholder="至少 6 位" required />
        </div>

        <p v-if="error" class="error">{{ error }}</p>

        <button class="btn btn-primary btn-block" type="submit" :disabled="loading">
          {{ loading ? '处理中…' : mode === 'login' ? '登录' : '注册并进入' }}
        </button>
      </form>
      </FadeContent>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import BlurText from '../components/animate/BlurText.vue'
import FadeContent from '../components/animate/FadeContent.vue'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const mode = ref(route.query.mode === 'register' ? 'register' : 'login')
const loading = ref(false)
const error = ref('')
const form = reactive({ username: '', password: '', nickname: '' })

function formatError(e) {
  const status = e.response?.status
  const detail = e.response?.data?.detail

  if (!e.response) {
    return '无法连接服务器，请确认后端已启动'
  }
  if (status === 404) {
    return '注册服务未就绪，请重启后端后再试'
  }
  if (Array.isArray(detail)) {
    return detail.map((item) => item.msg || item.message).filter(Boolean).join('；') || '输入有误，请检查'
  }
  if (typeof detail === 'string' && detail !== 'Not Found') {
    return detail
  }
  return '操作失败，请重试'
}

async function submit() {
  error.value = ''
  loading.value = true
  try {
    if (mode.value === 'login') {
      await auth.login({ username: form.username.trim(), password: form.password })
    } else {
      await auth.register({
        username: form.username.trim(),
        password: form.password,
        nickname: form.nickname.trim() || undefined,
      })
    }
    const redirect = route.query.redirect || '/diary'
    router.replace(typeof redirect === 'string' ? redirect : '/diary')
  } catch (e) {
    error.value = formatError(e)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.auth-card {
  position: relative;
  width: 100%;
  max-width: 400px;
  padding-top: 52px;
}

.back-home {
  position: absolute;
  top: 14px;
  left: 14px;
  z-index: 2;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 6px 13px 6px 9px;
  border-radius: 999px;
  font-family: var(--font-ui);
  font-size: 0.75rem;
  color: var(--c-text-dim);
  text-decoration: none;
  background: rgba(255, 252, 248, 0.92);
  border: 1px solid rgba(184, 137, 94, 0.28);
  box-shadow: 0 1px 6px rgba(58, 52, 46, 0.04);
  overflow: hidden;
  transition:
    color 0.3s ease,
    border-color 0.3s ease,
    transform 0.35s cubic-bezier(0.34, 1.2, 0.64, 1),
    box-shadow 0.3s ease;
}

.back-home::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: linear-gradient(120deg, rgba(255, 210, 150, 0.22), transparent 55%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.back-home:hover {
  color: var(--c-wood-deep);
  border-color: rgba(184, 137, 94, 0.5);
  transform: translateX(-4px);
  box-shadow: 0 3px 14px rgba(92, 74, 56, 0.1);
}

.back-home:hover::after {
  opacity: 1;
}

.back-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  color: var(--c-wood);
  transition: transform 0.35s cubic-bezier(0.34, 1.2, 0.64, 1);
}

.back-home:hover .back-icon {
  transform: translateX(-2px);
  color: var(--c-wood-deep);
}

.back-text {
  position: relative;
  z-index: 1;
  letter-spacing: 0.06em;
}

.back-leaf {
  position: relative;
  z-index: 1;
  width: 6px;
  height: 9px;
  margin-left: 1px;
  border-radius: 0 80% 0 80%;
  background: linear-gradient(145deg, rgba(122, 158, 112, 0.55), rgba(90, 122, 98, 0.35));
  transform: rotate(-28deg);
  opacity: 0.65;
  transition: transform 0.4s ease, opacity 0.3s ease;
}

.back-home:hover .back-leaf {
  transform: rotate(-38deg) translateY(-1px);
  opacity: 0.9;
}

.auth-head {
  text-align: center;
  margin-bottom: 24px;
}

.auth-logo {
  display: block;
  width: 72px;
  height: 72px;
  margin: 0 auto 12px;
  object-fit: contain;
}

.auth-head h1 {
  font-family: var(--font-handwrite);
  font-size: 1.875rem;
  font-weight: 400;
  color: var(--c-wood-deep);
  letter-spacing: 0.02em;
  margin-bottom: 8px;
  text-shadow: var(--grass-shadow);
}

.auth-head p {
  font-family: var(--font-ui);
  font-size: 0.875rem;
  color: var(--c-text-dim);
}

.tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  padding: 4px;
  background: rgba(239, 232, 220, 0.6);
  border-radius: var(--radius-sm);
}

.tabs button {
  flex: 1;
  padding: 8px;
  border: none;
  border-radius: 6px;
  background: transparent;
  font-family: var(--font-ui);
  font-size: 0.875rem;
  color: var(--c-text-dim);
  cursor: pointer;
  transition: all var(--transition);
}

.tabs button.active {
  background: rgba(255, 252, 248, 0.95);
  color: var(--c-wood-deep);
  font-weight: 500;
  box-shadow: var(--shadow-sm);
}

.field { margin-bottom: 16px; }

.error {
  font-family: var(--font-ui);
  font-size: 0.8125rem;
  color: var(--c-negative);
  margin-bottom: 12px;
}
</style>
