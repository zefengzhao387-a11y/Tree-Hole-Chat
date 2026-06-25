<template>
  <div class="page chat-page">
    <div class="card chat-box">
      <header class="chat-head">
        <div class="chat-info">
          <button type="button" class="back-btn" aria-label="返回" @click="goBack">←</button>
          <span class="avatar">{{ avatarChar }}</span>
          <div>
            <h2>{{ friendName }}</h2>
            <span class="status live">好友在线</span>
          </div>
        </div>
      </header>

      <div class="chat-body" ref="bodyRef">
        <div v-if="!messages.length && !loading" class="welcome">
          <p class="welcome-title">和 {{ friendName }} 说说话吧</p>
          <p class="welcome-desc">好友之间的消息会保存在这里，彼此可见。</p>
        </div>

        <div v-for="m in messages" :key="m.id" class="msg" :class="m.is_mine ? 'user' : 'assistant'">
          <div class="bubble">{{ m.content }}</div>
          <time class="time">{{ formatTime(m.created_at) }}</time>
        </div>
        <div ref="endRef"></div>
      </div>

      <footer class="chat-foot">
        <textarea
          v-model="input"
          class="chat-input"
          placeholder="发一条消息…"
          rows="1"
          @keydown.enter.exact.prevent="send"
          @input="autoGrow"
          ref="inputRef"
        ></textarea>
        <button class="btn btn-primary send" @click="send" :disabled="!input.trim() || sending">
          {{ sending ? '发送中' : '发送' }}
        </button>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { friendsAPI } from '../api/friends'
import { useFriendNotifyStore } from '../stores/friendNotify'

const route = useRoute()
const router = useRouter()
const friendNotify = useFriendNotifyStore()

const friendId = computed(() => Number(route.params.friendId))
const friendName = computed(() => route.query.name || '好友')
const avatarChar = computed(() => friendName.value.charAt(0))

const messages = ref([])
const input = ref('')
const sending = ref(false)
const loading = ref(false)
const bodyRef = ref(null)
const endRef = ref(null)
const inputRef = ref(null)
let pollTimer = null
let lastId = 0

function formatTime(t) {
  if (!t) return ''
  const d = new Date(t)
  return d.toLocaleString('zh-CN', { hour: '2-digit', minute: '2-digit', month: 'numeric', day: 'numeric' })
}

function autoGrow() {
  const el = inputRef.value
  if (el) {
    el.style.height = 'auto'
    el.style.height = Math.min(el.scrollHeight, 100) + 'px'
  }
}

async function scrollDown() {
  await nextTick()
  endRef.value?.scrollIntoView({ behavior: 'smooth' })
}

async function loadMessages(initial = false) {
  if (!friendId.value) return
  try {
    const { data } = await friendsAPI.getMessages(friendId.value, lastId)
    const items = data.items || []
    if (items.length) {
      const incoming = items.filter((m) => !m.is_mine)
      messages.value.push(...items)
      lastId = items[items.length - 1].id

      if (!initial && incoming.length) {
        for (const m of incoming) {
          ElMessage.info({
            message: `${friendName.value}：${friendNotify.preview(m.content, 36)}`,
            duration: 2800,
            grouping: true,
          })
        }
      }

      if (initial || !document.hidden) await scrollDown()
      friendNotify.poll(() => route)
    }
  } catch (err) {
    if (initial) {
      ElMessage.error(err.response?.data?.detail || '加载消息失败')
      router.replace('/my')
    }
  } finally {
    loading.value = false
  }
}

async function send() {
  const text = input.value.trim()
  if (!text || sending.value) return

  sending.value = true
  try {
    const { data } = await friendsAPI.sendMessage(friendId.value, text)
    messages.value.push(data)
    lastId = Math.max(lastId, data.id)
    input.value = ''
    if (inputRef.value) inputRef.value.style.height = 'auto'
    await scrollDown()
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '发送失败')
  } finally {
    sending.value = false
  }
}

function goBack() {
  router.push('/my')
}

function startPolling() {
  pollTimer = setInterval(() => {
    if (!document.hidden) loadMessages()
  }, 4000)
}

onMounted(async () => {
  loading.value = true
  await loadMessages(true)
  startPolling()
})

onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer)
})
</script>

<style scoped>
.chat-page { max-width: 680px; }

.chat-box {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 116px);
  overflow: hidden;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border);
  box-shadow: var(--shadow-md), var(--shadow-glow);
}

.chat-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid rgba(228, 220, 208, 0.5);
  background: rgba(255, 252, 248, 0.45);
}

.chat-info { display: flex; align-items: center; gap: 10px; }

.back-btn {
  border: none;
  background: rgba(244, 237, 228, 0.9);
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  color: var(--c-text-dim);
  font-size: 1rem;
}

.avatar {
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-handwrite);
  font-size: 1rem;
  color: var(--c-wood-deep);
  background: linear-gradient(145deg, rgba(255, 248, 240, 0.95), rgba(238, 244, 239, 0.85));
  border: 1px solid rgba(90, 122, 98, 0.25);
  border-radius: 50%;
}

.chat-info h2 {
  font-family: var(--font-handwrite);
  font-size: 1.0625rem;
  font-weight: 400;
  color: var(--c-wood-deep);
  letter-spacing: 0.08em;
}

.status {
  font-family: var(--font-ui);
  font-size: 0.75rem;
  color: var(--c-primary);
}

.chat-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px 18px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.welcome {
  text-align: center;
  padding: 40px 16px;
  color: var(--c-text-dim);
}

.welcome-title {
  font-family: var(--font-handwrite);
  font-size: 1.25rem;
  color: var(--c-wood-deep);
  margin-bottom: 8px;
}

.welcome-desc {
  font-family: var(--font-ui);
  font-size: 0.875rem;
  line-height: 1.6;
}

.msg {
  display: flex;
  flex-direction: column;
  max-width: 78%;
}

.msg.user {
  align-self: flex-end;
  align-items: flex-end;
}

.msg.assistant {
  align-self: flex-start;
  align-items: flex-start;
}

.bubble {
  padding: 10px 14px;
  border-radius: 16px;
  font-family: var(--font-ui);
  font-size: 0.9375rem;
  line-height: 1.55;
  word-break: break-word;
}

.msg.user .bubble {
  background: linear-gradient(135deg, var(--c-primary), var(--c-primary-hover));
  color: #fff;
  border-bottom-right-radius: 4px;
}

.msg.assistant .bubble {
  background: rgba(255, 252, 248, 0.92);
  color: var(--c-text);
  border: 1px solid rgba(228, 220, 208, 0.7);
  border-bottom-left-radius: 4px;
}

.time {
  margin-top: 4px;
  font-family: var(--font-ui);
  font-size: 0.6875rem;
  color: var(--c-text-muted);
}

.chat-foot {
  display: flex;
  gap: 10px;
  align-items: flex-end;
  padding: 14px 16px;
  border-top: 1px solid rgba(228, 220, 208, 0.5);
  background: rgba(255, 252, 248, 0.5);
}

.chat-input {
  flex: 1;
  resize: none;
  min-height: 42px;
  max-height: 100px;
  padding: 10px 14px;
  border-radius: 20px;
  border: 1px solid var(--c-border);
  background: rgba(255, 252, 248, 0.9);
  font-family: var(--font-ui);
  font-size: 0.9375rem;
  line-height: 1.5;
}

.send { flex-shrink: 0; border-radius: 20px; padding: 10px 18px; }
</style>
