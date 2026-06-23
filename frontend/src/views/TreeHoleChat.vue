<template>
  <div class="page chat-page">
    <div class="card chat-box">
      <header class="chat-head">
        <div class="chat-info">
          <span class="avatar">树</span>
          <div>
            <h2>小树</h2>
            <span class="status">{{ streaming ? '回复中…' : '在线' }}</span>
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
          <p v-if="m.role === 'assistant' && m.diary_ids?.length" class="ref">
            关联日记 #{{ parseIds(m.diary_ids).join(', #') }}
          </p>
        </div>

        <div v-if="streaming" class="msg assistant">
          <div class="bubble" v-html="render(streamText)"></div>
        </div>
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
          {{ streaming ? '…' : '发送' }}
        </button>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { chatAPI } from '../api/chat'

const messages = ref([])
const input = ref('')
const streaming = ref(false)
const streamText = ref('')
const endRef = ref(null)
const inputRef = ref(null)

const prompts = [
  '今天有点累…',
  '最近心情起伏很大',
  '有一件事一直放不下',
]

function parseIds(ids) {
  if (Array.isArray(ids)) return ids
  try { return JSON.parse(ids) } catch { return [] }
}

function render(t) {
  return t.replace(/\*\*(.+?)\*\*/g, '<b>$1</b>').replace(/\n/g, '<br>')
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
          if (d.content) { streamText.value += d.content; await scrollDown() }
          if (d.done) {
            messages.value.push({
              id: Date.now(),
              role: 'assistant',
              content: streamText.value,
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
    messages.value = data.messages
    await scrollDown()
  } catch { /* ignore */ }
}

onMounted(loadHistory)
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
  font-family: var(--font-ui);
  font-size: 0.75rem;
  color: var(--c-primary);
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

.send { flex-shrink: 0; padding: 10px 18px; }
</style>
