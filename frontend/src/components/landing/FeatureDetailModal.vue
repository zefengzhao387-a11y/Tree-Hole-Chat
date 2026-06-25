<template>
  <Teleport to="body">
    <div
      class="feature-modal"
      :class="{ open: isOpen, closing }"
      role="dialog"
      aria-modal="true"
      :aria-label="feature.detailTitle"
      @click.self="requestClose"
    >
      <div class="modal-backdrop" aria-hidden="true" />

      <div class="modal-panel" :style="originStyle">
        <button type="button" class="modal-close" aria-label="关闭" @click="requestClose">
          ×
        </button>

        <div class="modal-icon reveal" style="--i: 0" aria-hidden="true">{{ feature.icon }}</div>
        <p class="modal-kicker reveal" style="--i: 1">{{ feature.title }}</p>
        <h2 class="modal-title reveal" style="--i: 2">{{ feature.detailTitle }}</h2>
        <p class="modal-intro reveal" style="--i: 3">{{ feature.detailIntro }}</p>

        <ul class="modal-highlights">
          <li
            v-for="(item, idx) in feature.highlights"
            :key="idx"
            class="reveal"
            :style="{ '--i': 4 + idx }"
          >
            {{ item }}
          </li>
        </ul>

        <div v-if="feature.tech" class="modal-tech reveal" style="--i: 7">
          <span v-for="tag in feature.tech" :key="tag" class="tech-tag">{{ tag }}</span>
        </div>

        <div class="modal-actions reveal" style="--i: 8">
          <button type="button" class="btn btn-ghost" @click="requestClose">继续浏览</button>
          <button
            v-if="feature.route"
            type="button"
            class="btn btn-primary"
            @click="$emit('go', feature.route)"
          >
            {{ feature.cta || '立即体验' }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  feature: { type: Object, required: true },
  origin: { type: Object, default: null },
})

const emit = defineEmits(['close', 'go'])

const isOpen = ref(false)
const closing = ref(false)

const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches

const originStyle = computed(() => {
  if (!props.origin || prefersReducedMotion) return {}
  return {
    '--origin-top': `${props.origin.top}px`,
    '--origin-left': `${props.origin.left}px`,
    '--origin-width': `${props.origin.width}px`,
    '--origin-height': `${props.origin.height}px`,
  }
})

function requestClose() {
  if (closing.value) return
  closing.value = true
  isOpen.value = false
  window.setTimeout(() => emit('close'), prefersReducedMotion ? 0 : 420)
}

function onKeydown(e) {
  if (e.key === 'Escape') requestClose()
}

onMounted(() => {
  document.body.style.overflow = 'hidden'
  window.addEventListener('keydown', onKeydown)

  if (prefersReducedMotion) {
    isOpen.value = true
    return
  }

  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      isOpen.value = true
    })
  })
})

onUnmounted(() => {
  document.body.style.overflow = ''
  window.removeEventListener('keydown', onKeydown)
})
</script>

<style scoped>
/* 灵感: reactbits fade-content + spring scale 弹层 */
.feature-modal {
  position: fixed;
  inset: 0;
  z-index: 1000;
}

.modal-backdrop {
  position: absolute;
  inset: 0;
  background: rgba(244, 237, 228, 0);
  backdrop-filter: blur(0);
  -webkit-backdrop-filter: blur(0);
  transition: background 0.5s ease, backdrop-filter 0.5s ease;
}

.feature-modal.open .modal-backdrop {
  background: rgba(244, 237, 228, 0.88);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.feature-modal.closing .modal-backdrop {
  transition-duration: 0.32s;
}

.modal-panel {
  position: fixed;
  top: var(--origin-top, 50%);
  left: var(--origin-left, 50%);
  width: var(--origin-width, 240px);
  height: var(--origin-height, 130px);
  transform: translate(0, 0);
  display: flex;
  flex-direction: column;
  padding: 32px 28px 24px;
  overflow-y: auto;
  border-radius: 14px;
  background: var(--c-surface-solid);
  border: 1px solid var(--c-border);
  box-shadow: var(--shadow-lg);
  transition:
    top 0.62s cubic-bezier(0.22, 1, 0.36, 1),
    left 0.62s cubic-bezier(0.22, 1, 0.36, 1),
    width 0.62s cubic-bezier(0.22, 1, 0.36, 1),
    height 0.62s cubic-bezier(0.22, 1, 0.36, 1),
    transform 0.62s cubic-bezier(0.22, 1, 0.36, 1),
    border-radius 0.5s ease,
    box-shadow 0.5s ease;
}

.feature-modal.open .modal-panel {
  top: 50%;
  left: 50%;
  width: min(580px, 94vw);
  height: min(86vh, 720px);
  transform: translate(-50%, -50%);
  border-radius: 20px;
  box-shadow:
    0 24px 64px rgba(58, 52, 46, 0.2),
    0 0 0 1px rgba(90, 122, 98, 0.08);
}

.feature-modal.closing .modal-panel {
  transition-duration: 0.38s;
}

.modal-close {
  position: absolute;
  top: 14px;
  right: 16px;
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 50%;
  background: var(--c-bg-alt);
  color: var(--c-text-dim);
  font-size: 1.5rem;
  line-height: 1;
  cursor: pointer;
  transition: background var(--transition), color var(--transition), transform var(--transition);
  z-index: 2;
}

.modal-close:hover {
  background: var(--c-border);
  color: var(--c-wood-deep);
  transform: scale(1.05);
}

.reveal {
  opacity: 0;
  transform: translateY(14px);
}

.feature-modal.open .reveal {
  animation: modal-reveal 0.55s cubic-bezier(0.22, 1, 0.36, 1) forwards;
  animation-delay: calc(0.28s + var(--i, 0) * 55ms);
}

@keyframes modal-reveal {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-icon {
  font-size: 2.75rem;
  margin-bottom: 8px;
  filter: drop-shadow(0 4px 12px rgba(90, 122, 98, 0.15));
}

.modal-kicker {
  font-family: var(--font-ui);
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--c-primary);
  margin-bottom: 6px;
}

.modal-title {
  font-family: var(--font-handwrite);
  font-size: 1.875rem;
  font-weight: 400;
  color: var(--c-wood-deep);
  letter-spacing: 0.04em;
  line-height: 1.35;
  margin-bottom: 14px;
  text-shadow: var(--grass-shadow);
}

.modal-intro {
  font-family: var(--font-ui);
  font-size: 0.9375rem;
  color: var(--c-text-dim);
  line-height: 1.75;
  margin-bottom: 20px;
}

.modal-highlights {
  list-style: none;
  padding: 0;
  margin: 0 0 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.modal-highlights li {
  position: relative;
  padding: 12px 14px 12px 36px;
  font-family: var(--font-ui);
  font-size: 0.875rem;
  color: var(--c-text);
  line-height: 1.6;
  background: var(--c-primary-soft);
  border-radius: var(--radius-sm);
  border: 1px solid rgba(90, 122, 98, 0.14);
}

.modal-highlights li::before {
  content: '✦';
  position: absolute;
  left: 14px;
  top: 12px;
  color: var(--c-primary);
  font-size: 0.75rem;
}

.modal-tech {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 24px;
}

.tech-tag {
  font-family: var(--font-ui);
  font-size: 0.6875rem;
  padding: 4px 10px;
  border-radius: 100px;
  color: var(--c-primary);
  background: rgba(90, 122, 98, 0.1);
  border: 1px solid rgba(90, 122, 98, 0.15);
}

.modal-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  flex-wrap: wrap;
  padding-top: 8px;
  margin-top: auto;
  border-top: 1px dashed var(--c-border);
}

@media (prefers-reduced-motion: reduce) {
  .modal-panel,
  .modal-backdrop {
    transition: none !important;
  }

  .reveal {
    opacity: 1 !important;
    transform: none !important;
    animation: none !important;
  }
}

@media (max-width: 520px) {
  .modal-panel { padding: 28px 20px 22px; }
  .modal-title { font-size: 1.5rem; }
  .modal-actions { flex-direction: column-reverse; }
  .modal-actions .btn { width: 100%; }
}
</style>
