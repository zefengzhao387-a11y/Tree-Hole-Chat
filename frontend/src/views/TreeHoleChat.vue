<template>
  <div class="page chat-page">
    <div class="card chat-box">
      <header class="chat-head">
        <div class="chat-info">
          <span class="avatar">树</span>
          <div>
            <h2>小树</h2>
            <span class="status" :class="{ live: streaming }">
              <span v-if="streaming" class="status-dot" aria-hidden="true"></span>
              {{ streaming ? '回复中' : '在线' }}
            </span>
          </div>
        </div>
        <button class="btn btn-ghost" @click="clear" :disabled="!messages.length">清空</button>
      </header>

      <div class="chat-body" ref="bodyRef">
        <div v-if="!messages.length" class="welcome">
          <p class="welcome-title">嗨，我是小树</p>
          <p class="welcome-desc">一个安静倾听的树洞。你说的话会被保密，我也会结合你的日记来理解你。</p>
          <div class="prompts">
            <button v-for="p in prompts" :key="p" class="prompt" @click="usePrompt(p)">{{ p }}</button>
          </div>
        </div>

        <div v-for="m in messages" :key="m.id" class="msg" :class="m.role">
          <div class="bubble" v-html="render(m.content)"></div>
          <p v-if="m.role === 'assistant' && hasDiaryRefs(m.diary_ids)" class="ref">
            关联日记 #{{ formatDiaryRefs(m.diary_ids) }}
          </p>
        </div>

        <template v-if="streaming">
          <ChatTypingIndicator v-if="!streamText" :hint="typingHint" />
          <div v-else class="msg assistant streaming-msg">
            <div class="bubble streaming-bubble">
              <span class="stream-content" v-html="render(streamText)"></span>
              <span class="stream-cursor" aria-hidden="true"></span>
            </div>
          </div>
        </template>
        <div ref="endRef"></div>
      </div>

      <footer class="chat-foot">
        <textarea
          v-model="input"
          class="chat-input"
          placeholder="说说你的心里话…"
          rows="1"
          @keydown.enter.exact.prevent="send"
          @input="autoGrow"
          :disabled="streaming"
          ref="inputRef"
        ></textarea>
        <button class="btn btn-primary send" @click="send" :disabled="!input.trim() || streaming">
          <span v-if="streaming" class="send-loading">
            <span class="send-spinner" aria-hidden="true"></span>
            回复中
          </span>
          <span v-else>发送</span>
        </button>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { chatAPI } from '../api/chat'
import ChatTypingIndicator from '../components/ChatTypingIndicator.vue'

const messages = ref([])
const input = ref('')
const streaming = ref(false)
const streamText = ref('')
const typingHint = ref('小树正在听…')
const bodyRef = ref(null)
const endRef = ref(null)
const inputRef = ref(null)

const typingHints = [
  '小树正在听…',
  '翻翻你的日记…',
  '正在组织语言…',
]
let typingTimer = null

function startTypingHints() {
  let i = 0
  typingHint.value = typingHints[0]
  typingTimer = setInterval(() => {
    i = (i + 1) % typingHints.length
    typingHint.value = typingHints[i]
  }, 2200)
}

function stopTypingHints() {
  if (typingTimer) {
    clearInterval(typingTimer)
    typingTimer = null
  }
}

const prompts = [
  '今天有点累…',
  '最近心情起伏很大',
  '有一件事一直放不下',
]

function parseIds(ids) {
  if (ids == null || ids === '') return []
  if (Array.isArray(ids)) return ids.filter((id) => id != null)
  if (typeof ids === 'number') return [ids]
  try {
    const parsed = JSON.parse(ids)
    if (Array.isArray(parsed)) return parsed.filter((id) => id != null)
    if (parsed == null) return []
    if (typeof parsed === 'number') return [parsed]
    return []
  } catch {
    return []
  }
}

function formatDiaryRefs(ids) {
  const list = parseIds(ids)
  return list.length ? list.join(', #') : ''
}

function hasDiaryRefs(ids) {
  return parseIds(ids).length > 0
}

function normalizeMessage(raw) {
  if (!raw || typeof raw !== 'object') return null
  return {
    id: raw.id ?? Date.now(),
    role: raw.role === 'user' ? 'user' : 'assistant',
    content: typeof raw.content === 'string' ? raw.content : String(raw.content ?? ''),
    diary_ids: raw.diary_ids ?? null,
  }
}

function render(t) {
  if (t == null) return ''
  const text = typeof t === 'string' ? t : String(t)
  return text.replace(/\*\*(.+?)\*\*/g, '<b>$1</b>').replace(/\n/g, '<br>')
}

function usePrompt(p) {
  input.value = p
  inputRef.value?.focus()
  autoGrow()
}

function autoGrow() {
  const el = inputRef.value
  if (el) { el.style.height = 'auto'; el.style.height = Math.min(el.scrollHeight, 100) + 'px' }
}

async function scrollDown() {
  await nextTick()
  endRef.value?.scrollIntoView({ behavior: 'smooth' })
}

async function send() {
  const text = input.value.trim()
  if (!text || streaming.value) return

  messages.value.push({ id: Date.now(), role: 'user', content: text })
  input.value = ''
  if (inputRef.value) inputRef.value.style.height = 'auto'
  await scrollDown()

  streaming.value = true
  streamText.value = ''
  startTypingHints()

  try {
    const resp = await chatAPI.sendMessage(text)
    const reader = resp.body.getReader()
    const dec = new TextDecoder()
    let buf = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      buf += dec.decode(value, { stream: true })
      const lines = buf.split('\n')
      buf = lines.pop() || ''
      for (const l of lines) {
        if (!l.startsWith('data: ')) continue
        try {
          const d = JSON.parse(l.slice(6))
          if (d.content) {
            stopTypingHints()
            streamText.value += d.content
            await scrollDown()
          }
          if (d.done) {
            if (d.error) console.error('[chat]', d.error)
            const reply = (streamText.value || d.content || '').trim()
            messages.value.push({
              id: Date.now(),
              role: 'assistant',
              content: reply || '小树走神了一下，可以再说一次吗？',
              diary_ids: d.diary_ids || [],
            })
            streamText.value = ''
          }
        } catch { /* skip */ }
      }
    }
  } catch {
    messages.value.push({
      id: Date.now(),
      role: 'assistant',
      content: '小树走神了一下，可以再说一次吗？',
    })
  } finally {
    stopTypingHints()
    streaming.value = false
    await scrollDown()
  }
}

async function clear() {
  try {
    await ElMessageBox.confirm('确定清空对话吗？', '确认', {
      confirmButtonText: '清空',
      cancelButtonText: '取消',
    })
    await chatAPI.clearHistory()
    messages.value = []
    ElMessage.success('已清空')
  } catch { /* cancelled */ }
}

async function loadHistory() {
  try {
    const { data } = await chatAPI.getHistory()
    const list = Array.isArray(data?.messages) ? data.messages : []
    messages.value = list.map(normalizeMessage).filter(Boolean)
    await scrollDown()
  } catch (err) {
    console.warn('[chat] load history failed:', err)
    messages.value = []
  }
}

onMounted(loadHistory)
onUnmounted(stopTypingHints)
</script>

<style scoped>
.chat-page { max-width: 680px; }

.chat-box {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 112px);
  overflow: hidden;
  background: var(--c-surface);
}

.chat-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--c-border-light);
}

.chat-info { display: flex; align-items: center; gap: 12px; }

.avatar {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-handwrite);
  font-size: 1rem;
  color: var(--c-wood-deep);
  background: rgba(255, 248, 240, 0.9);
  border: 1px solid rgba(184, 137, 94, 0.25);
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
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-family: var(--font-ui);
  font-size: 0.75rem;
  color: var(--c-primary);
}

.status.live { color: var(--c-warm); }

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--c-warm);
  animation: status-blink 1.2s ease-in-out infinite;
}

@keyframes status-blink {
  0%, 100% { opacity: 0.35; transform: scale(0.85); }
  50% { opacity: 1; transform: scale(1); }
}

.chat-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.welcome { text-align: center; padding: 24px 0; }

.welcome-title {
  font-family: var(--font-handwrite);
  font-size: 1.375rem;
  font-weight: 400;
  color: var(--c-wood-deep);
  letter-spacing: 0.1em;
  margin-bottom: 8px;
}

.welcome-desc {
  font-family: var(--font-ui);
  font-size: 0.875rem;
  color: var(--c-text-dim);
  line-height: 1.6;
  max-width: 320px;
  margin: 0 auto 20px;
}

.prompts {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}

.prompt {
  padding: 8px 14px;
  border: 1px solid var(--c-border);
  border-radius: 100px;
  background: var(--c-bg);
  font-family: var(--font-ui);
  font-size: 0.8125rem;
  color: var(--c-text-dim);
  cursor: pointer;
  transition: border-color var(--transition);
}

.prompt:hover {
  border-color: var(--c-wood);
  color: var(--c-wood-deep);
  background: rgba(255, 252, 248, 0.9);
}

.msg { display: flex; flex-direction: column; max-width: 85%; }
.msg.user { align-self: flex-end; align-items: flex-end; }
.msg.assistant { align-self: flex-start; }

.streaming-msg {
  animation: typing-in 0.25s ease;
}

@keyframes typing-in {
  from { opacity: 0; transform: translateY(6px); }
}

.streaming-bubble {
  display: inline-flex;
  align-items: flex-end;
  flex-wrap: wrap;
  gap: 1px;
}

.stream-content :deep(b) {
  color: var(--c-wood-deep);
}

.stream-cursor {
  display: inline-block;
  width: 2px;
  height: 1em;
  margin-left: 2px;
  margin-bottom: 2px;
  background: var(--c-primary);
  border-radius: 1px;
  animation: cursor-blink 0.9s step-end infinite;
}

@keyframes cursor-blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.bubble {
  padding: 10px 14px;
  border-radius: 14px;
  font-size: 0.9375rem;
  line-height: 1.65;
}

.msg.user .bubble {
  background: var(--c-wood-deep);
  color: #f5ebe0;
  border-bottom-right-radius: 4px;
}

.msg.assistant .bubble {
  background: rgba(255, 252, 248, 0.92);
  color: var(--c-text);
  border: 1px solid rgba(228, 220, 208, 0.6);
  border-bottom-left-radius: 4px;
}

.ref {
  font-family: var(--font-ui);
  font-size: 0.6875rem;
  color: var(--c-text-muted);
  margin-top: 4px;
}

.chat-foot {
  display: flex;
  gap: 10px;
  padding: 14px 16px;
  border-top: 1px solid var(--c-border-light);
  align-items: flex-end;
}

.chat-input {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid var(--c-border);
  border-radius: var(--radius-sm);
  font-family: var(--font-display);
  font-size: 0.9375rem;
  line-height: 1.5;
  background: #fff;
  color: var(--c-text);
  outline: none;
  resize: none;
  min-height: 42px;
  max-height: 100px;
}

.chat-input:focus { border-color: var(--c-wood); }

.send { flex-shrink: 0; padding: 10px 18px; min-width: 88px; }

.send-loading {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.send-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.35);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.75s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (prefers-reduced-motion: reduce) {
  .status-dot,
  .stream-cursor,
  .send-spinner {
    animation: none;
  }
}
</style>
