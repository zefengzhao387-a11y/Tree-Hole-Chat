<template>
  <div class="bubble-wrapper" :class="role">
    <div class="avatar-ring" :class="role">
      <span class="avatar-emoji">{{ role === 'assistant' ? '🌳' : '😊' }}</span>
    </div>
    <div class="bubble-body">
      <div class="bubble" :class="role">
        <div class="bubble-text" v-html="rendered"></div>
      </div>
      <div v-if="role === 'assistant' && diaryIds?.length" class="refs">
        <span class="ref-label">📖 想起了你的日记 #</span>
        <span class="ref-nums">{{ diaryIds.join(', #') }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  role: { type: String, required: true },
  content: { type: String, required: true },
  diaryIds: { type: Array, default: null },
})

const rendered = computed(() => {
  let t = props.content
  t = t.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
  t = t.replace(/\n/g, '<br>')
  return t
})
</script>

<style scoped>
.bubble-wrapper {
  display: flex; gap: 10px; margin-bottom: 18px;
  align-items: flex-start;
  animation: msg-in 0.4s cubic-bezier(0.4,0,0.2,1);
}

@keyframes msg-in {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

.bubble-wrapper.user { flex-direction: row-reverse; }

.avatar-ring {
  width: 40px; height: 40px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; font-size: 22px;
  position: relative;
}

.avatar-ring.assistant {
  background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
  box-shadow: 0 2px 12px rgba(130,180,120,0.2);
}

.avatar-ring.user {
  background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
  box-shadow: 0 2px 12px rgba(210,160,100,0.2);
}

.avatar-emoji { line-height: 1; }

.bubble-body { max-width: 78%; }

.bubble {
  padding: 14px 18px; line-height: 1.75;
  font-size: 14px; font-family: 'Noto Serif SC', serif;
  word-break: break-word;
}

.bubble.assistant {
  background: rgba(255,255,255,0.65);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.35);
  border-radius: 20px 20px 20px 6px;
  color: #4a3728;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}

.bubble.user {
  background: linear-gradient(135deg, rgba(212,165,116,0.85) 0%, rgba(180,132,94,0.85) 100%);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 20px 20px 6px 20px;
  color: white;
  box-shadow: 0 2px 12px rgba(180,130,90,0.15);
}

.bubble-text strong { color: #8b6914; }
.bubble.user .bubble-text strong { color: #fff8e1; }

.refs { margin-top: 6px; font-size: 11px; padding-left: 4px; }
.ref-label { color: #b0a090; }
.ref-nums { color: #c4956a; font-weight: 500; }
</style>
