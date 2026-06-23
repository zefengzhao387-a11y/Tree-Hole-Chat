<template>
  <span class="badge" :class="sentiment">
    <span v-if="showLabel">{{ emotion || '未知' }}</span>
    <span v-if="intensity" class="int">{{ intensity }}/10</span>
  </span>
</template>

<script setup>
defineProps({
  emotion: { type: String, default: '未知' },
  sentiment: { type: String, default: 'neutral' },
  intensity: { type: Number, default: null },
  showLabel: { type: Boolean, default: true },
})
</script>

<style scoped>
.badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 10px;
  border-radius: 100px;
  font-family: var(--font-ui);
  font-size: 0.75rem;
  font-weight: 500;
  background: var(--c-bg-alt);
  color: var(--c-text-dim);
}

.badge.positive { background: #eef4ef; color: var(--c-positive); }
.badge.negative { background: #f9eeee; color: var(--c-negative); }
.badge.neutral  { background: #eef2f5; color: var(--c-neutral); }

.int { opacity: 0.7; font-size: 0.6875rem; }
</style>
