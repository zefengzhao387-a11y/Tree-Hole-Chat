<template>
  <div class="skeleton-list">
    <div v-for="n in count" :key="n" class="skeleton-card card">
      <div class="sk-line sk-meta" />
      <div class="sk-line sk-title" />
      <div class="sk-line sk-text" />
      <div class="sk-line sk-text short" />
    </div>
  </div>
</template>

<script setup>
defineProps({
  count: { type: Number, default: 3 },
})
</script>

<style scoped>
.skeleton-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.skeleton-card {
  padding: 20px 22px;
  overflow: hidden;
}

.sk-line {
  height: 12px;
  border-radius: 6px;
  background: linear-gradient(
    90deg,
    rgba(228, 220, 208, 0.45) 0%,
    rgba(255, 252, 248, 0.9) 50%,
    rgba(228, 220, 208, 0.45) 100%
  );
  background-size: 200% 100%;
  animation: shimmer-load 1.4s ease-in-out infinite;
}

.sk-meta { width: 28%; margin-bottom: 14px; height: 10px; }
.sk-title { width: 55%; margin-bottom: 12px; height: 16px; }
.sk-text { width: 100%; margin-bottom: 8px; }
.sk-text.short { width: 72%; }

@keyframes shimmer-load {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

@media (prefers-reduced-motion: reduce) {
  .sk-line { animation: none; background: rgba(228, 220, 208, 0.5); }
}
</style>
