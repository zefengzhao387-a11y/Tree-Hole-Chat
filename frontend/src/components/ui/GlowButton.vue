<template>
  <!-- 灵感来源: Uiverse Animated Gradient Buttons -->
  <button
    class="glow-btn"
    :class="{ block, ghost }"
    :disabled="disabled"
    :type="type"
    @click="$emit('click', $event)"
  >
    <span v-if="!ghost" class="glow-ring" aria-hidden="true"></span>
    <span class="glow-content"><slot /></span>
  </button>
</template>

<script setup>
defineProps({
  disabled: { type: Boolean, default: false },
  block: { type: Boolean, default: false },
  ghost: { type: Boolean, default: false },
  type: { type: String, default: 'button' },
})
defineEmits(['click'])
</script>

<style scoped>
.glow-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 28px;
  border: none;
  border-radius: 100px;
  font-family: inherit;
  font-size: 0.9rem;
  font-weight: 500;
  letter-spacing: 0.04em;
  cursor: pointer;
  overflow: hidden;
  color: #fff;
  background: linear-gradient(135deg, #c4956a 0%, #a87d55 50%, #8b6b4a 100%);
  box-shadow: 0 4px 20px rgba(196, 149, 106, 0.35);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.glow-btn.block { width: 100%; padding: 14px; font-size: 1rem; }

.glow-btn.ghost {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: var(--c-text-dim);
  box-shadow: none;
}

.glow-btn.ghost:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.12);
  color: var(--c-text);
  box-shadow: 0 0 20px rgba(255, 255, 255, 0.06);
}

.glow-ring {
  position: absolute;
  inset: -2px;
  border-radius: inherit;
  background: linear-gradient(
    90deg,
    #c4956a, #9bb5a0, #b8a0d0, #d4a5a5, #c4956a
  );
  background-size: 300% 100%;
  animation: ring-flow 4s linear infinite;
  z-index: 0;
  opacity: 0;
  filter: blur(6px);
  transition: opacity 0.3s;
}

.glow-btn:hover:not(:disabled) .glow-ring { opacity: 0.7; }

.glow-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(196, 149, 106, 0.45);
}

.glow-btn:active:not(:disabled) { transform: translateY(0); }

.glow-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.glow-content {
  position: relative;
  z-index: 1;
}

@keyframes ring-flow {
  0% { background-position: 0% 50%; }
  100% { background-position: 300% 50%; }
}
</style>
