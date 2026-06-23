<template>
  <!-- 灵感来源: Uiverse Glassmorphism / Gradient Border Cards -->
  <div
    class="glow-card"
    :class="{ interactive, 'glow-active': active }"
    @click="$emit('click', $event)"
  >
    <div class="glow-border"></div>
    <div class="glow-inner">
      <slot />
    </div>
  </div>
</template>

<script setup>
defineProps({
  interactive: { type: Boolean, default: false },
  active: { type: Boolean, default: false },
})
defineEmits(['click'])
</script>

<style scoped>
.glow-card {
  position: relative;
  border-radius: var(--radius-lg);
  padding: 1px;
  overflow: hidden;
}

.glow-border {
  position: absolute;
  inset: -50%;
  background: conic-gradient(
    from 0deg,
    rgba(196, 149, 106, 0.5),
    rgba(155, 181, 160, 0.4),
    rgba(180, 160, 210, 0.35),
    rgba(212, 165, 165, 0.4),
    rgba(196, 149, 106, 0.5)
  );
  animation: border-spin 8s linear infinite;
  opacity: 0.35;
  transition: opacity 0.4s ease;
}

.glow-card.interactive:hover .glow-border,
.glow-card.glow-active .glow-border {
  opacity: 0.75;
}

.glow-inner {
  position: relative;
  border-radius: calc(var(--radius-lg) - 1px);
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(24px) saturate(160%);
  -webkit-backdrop-filter: blur(24px) saturate(160%);
  border: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow:
    0 4px 24px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.08);
  transition: transform 0.35s cubic-bezier(0.25, 0.1, 0.25, 1),
              box-shadow 0.35s ease;
}

.glow-card.interactive {
  cursor: pointer;
}

.glow-card.interactive:hover .glow-inner {
  transform: translateY(-3px);
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.22),
    0 0 40px rgba(196, 149, 106, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.12);
}

@keyframes border-spin {
  to { transform: rotate(360deg); }
}
</style>
