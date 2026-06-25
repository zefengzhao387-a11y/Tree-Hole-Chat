<template>
  <span class="badge" :class="sentiment">
    <span v-if="showLabel" class="badge-label">{{ emotion || '未知' }}</span>
    <span v-if="intensity != null" class="int">{{ intensity }}/10</span>
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
  gap: 5px;
  padding: 3px 11px;
  border-radius: 100px;
  font-family: var(--font-ui);
  font-size: 0.75rem;
  font-weight: 500;
  border: 1px solid transparent;
  box-shadow: 0 1px 4px rgba(58, 52, 46, 0.04);
}

.badge.positive {
  background: linear-gradient(135deg, #eef6ef 0%, #e4efe6 100%);
  color: var(--c-positive);
  border-color: rgba(90, 122, 98, 0.18);
}

.badge.negative {
  background: linear-gradient(135deg, #faf0f0 0%, #f5e8e8 100%);
  color: var(--c-negative);
  border-color: rgba(176, 112, 112, 0.18);
}

.badge.neutral {
  background: linear-gradient(135deg, #f0f3f6 0%, #e8edf2 100%);
  color: var(--c-neutral);
  border-color: rgba(138, 154, 170, 0.18);
}

.badge-label { letter-spacing: 0.02em; }

.int {
  opacity: 0.75;
  font-size: 0.6875rem;
  padding-left: 4px;
  border-left: 1px solid currentColor;
  opacity: 0.5;
}
</style>
