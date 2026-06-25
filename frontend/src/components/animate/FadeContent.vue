<!-- 灵感来源: https://www.reactbits.dev/animations/fade-content -->
<template>
  <div
    ref="targetRef"
    class="fade-content"
    :class="[
      { visible: inView },
      `from-${direction}`,
      { blur: blur },
      className,
    ]"
    :style="{ transitionDelay: `${delay}ms`, transitionDuration: `${duration}ms` }"
  >
    <slot />
  </div>
</template>

<script setup>
import { useInView } from '../../composables/useInView'

defineProps({
  direction: { type: String, default: 'up' }, // up | down | left | right | none
  blur: { type: Boolean, default: false },
  delay: { type: Number, default: 0 },
  duration: { type: Number, default: 700 },
  className: { type: String, default: '' },
  threshold: { type: Number, default: 0.12 },
})

const { targetRef, inView } = useInView({ threshold: 0.12 })
</script>

<style scoped>
.fade-content {
  opacity: 0;
  will-change: opacity, transform, filter;
  transition-property: opacity, transform, filter;
  transition-timing-function: cubic-bezier(0.22, 1, 0.36, 1);
}

.fade-content.from-up { transform: translateY(28px); }
.fade-content.from-down { transform: translateY(-28px); }
.fade-content.from-left { transform: translateX(-28px); }
.fade-content.from-right { transform: translateX(28px); }
.fade-content.from-none { transform: none; }

.fade-content.blur { filter: blur(8px); }

.fade-content.visible {
  opacity: 1;
  transform: translate(0, 0);
  filter: blur(0);
}

@media (prefers-reduced-motion: reduce) {
  .fade-content {
    opacity: 1 !important;
    transform: none !important;
    filter: none !important;
    transition: none !important;
  }
}
</style>
