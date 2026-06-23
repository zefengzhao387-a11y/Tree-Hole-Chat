<template>
  <!-- 灵感来源: React Bits Gradient Text -->
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
  font-family: var(--font-display);
  background: linear-gradient(
    115deg,
    #f4efe8 0%,
    var(--page-accent) 35%,
    #c4b0dc 65%,
    #a8c4ae 85%,
    #f4efe8 100%
  );
  background-size: 200% auto;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shimmer 6s linear infinite;
  letter-spacing: 0.03em;
}

.shimmer-title.lg { font-size: 1.65rem; font-weight: 600; }
.shimmer-title.md { font-size: 1.35rem; font-weight: 600; }
.shimmer-title.sm { font-size: 1rem; font-weight: 550; }

@keyframes shimmer {
  0% { background-position: 0% center; }
  100% { background-position: 200% center; }
}
</style>
