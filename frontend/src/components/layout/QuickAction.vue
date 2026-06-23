<template>
  <router-link :to="to" class="quick-action" :class="variant">
    <span class="qa-icon">{{ icon }}</span>
    <span class="qa-text">
      <strong>{{ label }}</strong>
      <small>{{ hint }}</small>
    </span>
    <span class="qa-arrow">→</span>
  </router-link>
</template>

<script setup>
defineProps({
  to: { type: String, required: true },
  icon: { type: String, required: true },
  label: { type: String, required: true },
  hint: { type: String, default: '' },
  variant: { type: String, default: 'gold' },
})
</script>

<style scoped>
.quick-action {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: var(--radius-md);
  text-decoration: none;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.07);
  transition: all var(--transition);
  flex: 1;
  min-width: 140px;
}

.quick-action:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.07);
  border-color: rgba(255, 255, 255, 0.12);
}

.quick-action.gold:hover { box-shadow: 0 8px 24px rgba(232, 196, 154, 0.12); }
.quick-action.sage:hover { box-shadow: 0 8px 24px rgba(168, 196, 174, 0.12); }
.quick-action.lavender:hover { box-shadow: 0 8px 24px rgba(196, 176, 220, 0.12); }

.qa-icon {
  font-size: 1.5rem;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.05);
}

.quick-action.gold .qa-icon { background: rgba(232, 196, 154, 0.12); }
.quick-action.sage .qa-icon { background: rgba(168, 196, 174, 0.12); }
.quick-action.lavender .qa-icon { background: rgba(196, 176, 220, 0.12); }

.qa-text {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.qa-text strong {
  font-family: var(--font-ui);
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--c-text);
}

.qa-text small {
  font-family: var(--font-ui);
  font-size: 0.72rem;
  color: var(--c-text-muted);
}

.qa-arrow {
  font-size: 0.9rem;
  color: var(--c-text-muted);
  transition: transform var(--transition), color var(--transition);
}

.quick-action:hover .qa-arrow {
  transform: translateX(3px);
  color: var(--c-text-dim);
}
</style>
