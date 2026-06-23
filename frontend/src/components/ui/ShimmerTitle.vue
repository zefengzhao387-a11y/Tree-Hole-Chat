<template>
  <!-- 马善政毛笔楷：介于草隶与宋体之间 -->
  <component :is="tag" class="shimmer-title" :class="size">
    <slot />
  </component>
</template>

<script setup>
defineProps({
  tag: { type: String, default: 'h1' },
  size: { type: String, default: 'lg' },
})
</script>

<style scoped>
.shimmer-title {
  font-family: var(--font-handwrite);
  font-weight: 400;
  letter-spacing: 0.02em;
  line-height: 1.35;
  color: var(--c-wood-deep);
  background: linear-gradient(
    115deg,
    #4a3d30 0%,
    #5c4a38 22%,
    #526848 45%,
    #5a7a62 58%,
    #5c4a38 78%,
    #4a3d30 100%
  );
  background-size: 220% auto;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  paint-order: stroke fill;
  -webkit-text-stroke: 0.4px rgba(58, 52, 46, 0.22);
  filter: drop-shadow(0 1px 0 rgba(255, 252, 248, 0.35));
  animation: shimmer 10s linear infinite;
}

.shimmer-title.lg { font-size: 1.9rem; }
.shimmer-title.md { font-size: 1.5rem; }
.shimmer-title.sm { font-size: 1.125rem; }

@keyframes shimmer {
  0% { background-position: 0% center; }
  100% { background-position: 220% center; }
}

@media (prefers-reduced-motion: reduce) {
  .shimmer-title {
    animation: none;
    -webkit-text-fill-color: var(--c-wood-deep);
    background: none;
    filter: none;
    text-shadow: var(--grass-shadow);
  }
}
</style>
