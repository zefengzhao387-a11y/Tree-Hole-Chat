<template>
  <div class="typing-indicator" role="status" :aria-label="hint">
    <span class="typing-avatar" aria-hidden="true">树</span>
    <div class="typing-bubble">
      <div class="typing-dots" aria-hidden="true">
        <span v-for="i in 3" :key="i" class="dot" :style="{ animationDelay: `${(i - 1) * 0.18}s` }" />
      </div>
      <p class="typing-hint">{{ hint }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  hint: { type: String, default: '小树正在想…' },
})
</script>

<style scoped>
.typing-indicator {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  max-width: 85%;
  align-self: flex-start;
  animation: typing-in 0.35s cubic-bezier(0.34, 1.1, 0.64, 1);
}

@keyframes typing-in {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
}

.typing-avatar {
  width: 36px;
  height: 36px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-handwrite);
  font-size: 0.875rem;
  color: var(--c-wood-deep);
  background: rgba(255, 248, 240, 0.95);
  border: 1px solid rgba(184, 137, 94, 0.22);
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(90, 122, 98, 0.08);
}

.typing-bubble {
  padding: 12px 16px 10px;
  border-radius: 14px 14px 14px 4px;
  background: rgba(255, 252, 248, 0.95);
  border: 1px solid rgba(228, 220, 208, 0.75);
  box-shadow: 0 2px 12px rgba(58, 52, 46, 0.04);
  min-width: 120px;
}

.typing-dots {
  display: flex;
  align-items: center;
  gap: 6px;
  height: 18px;
  margin-bottom: 6px;
}

.dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--c-primary);
  animation: dot-bounce 1.2s ease-in-out infinite;
  opacity: 0.55;
}

.dot:nth-child(2) { background: #7a9a72; }
.dot:nth-child(3) { background: var(--c-warm); }

@keyframes dot-bounce {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.45;
  }
  30% {
    transform: translateY(-5px);
    opacity: 1;
  }
}

.typing-hint {
  font-family: var(--font-ui);
  font-size: 0.75rem;
  color: var(--c-text-muted);
  letter-spacing: 0.04em;
  animation: hint-pulse 2.4s ease-in-out infinite;
}

@keyframes hint-pulse {
  0%, 100% { opacity: 0.65; }
  50% { opacity: 1; }
}

@media (prefers-reduced-motion: reduce) {
  .typing-indicator { animation: none; }
  .dot { animation: none; opacity: 0.8; }
  .typing-hint { animation: none; opacity: 1; }
}
</style>
