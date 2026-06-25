<!-- 灵感来源: https://www.reactbits.dev/text-animations/shiny-text -->
<template>
  <component
    :is="tag"
    class="shiny-text"
    :class="[{ paused: isPaused }, className]"
    :style="styleVars"
    @mouseenter="pauseOnHover && (isPaused = true)"
    @mouseleave="pauseOnHover && (isPaused = false)"
  >{{ text }}<slot /></component>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  text: { type: String, default: '' },
  tag: { type: String, default: 'span' },
  className: { type: String, default: '' },
  speed: { type: Number, default: 3 },
  color: { type: String, default: '#5c4a38' },
  shineColor: { type: String, default: '#8fb896' },
  spread: { type: Number, default: 120 },
  pauseOnHover: { type: Boolean, default: false },
})

const isPaused = ref(false)

const styleVars = computed(() => ({
  '--shiny-color': props.color,
  '--shiny-shine': props.shineColor,
  '--shiny-spread': `${props.spread}deg`,
  '--shiny-duration': `${props.speed}s`,
}))
</script>

<style scoped>
.shiny-text {
  display: inline-block;
  background-image: linear-gradient(
    var(--shiny-spread),
    var(--shiny-color) 0%,
    var(--shiny-color) 38%,
    var(--shiny-shine) 50%,
    var(--shiny-color) 62%,
    var(--shiny-color) 100%
  );
  background-size: 200% auto;
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shiny-sweep var(--shiny-duration) ease-in-out infinite;
}

.shiny-text.paused {
  animation-play-state: paused;
}

.shiny-text:hover {
  /* pauseOnHover 由 JS class 控制 */
}

@keyframes shiny-sweep {
  0% { background-position: 150% center; }
  100% { background-position: -50% center; }
}

@media (prefers-reduced-motion: reduce) {
  .shiny-text {
    animation: none;
    -webkit-text-fill-color: var(--shiny-color);
    background: none;
  }
}
</style>
