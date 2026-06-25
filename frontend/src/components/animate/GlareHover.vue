<!-- 灵感来源: https://www.reactbits.dev/animations/glare-hover -->
<template>
  <div
    class="glare-hover"
    :class="[{ 'play-once': playOnce }, className]"
    :style="styleVars"
  >
    <slot />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  borderRadius: { type: String, default: 'var(--radius-lg)' },
  glareColor: { type: String, default: '#ffffff' },
  glareOpacity: { type: Number, default: 0.35 },
  glareAngle: { type: Number, default: -45 },
  glareSize: { type: Number, default: 250 },
  transitionDuration: { type: Number, default: 650 },
  playOnce: { type: Boolean, default: false },
  className: { type: String, default: '' },
})

const styleVars = computed(() => {
  const hex = props.glareColor.replace('#', '')
  let rgba = props.glareColor
  if (/^[0-9A-Fa-f]{6}$/.test(hex)) {
    const r = parseInt(hex.slice(0, 2), 16)
    const g = parseInt(hex.slice(2, 4), 16)
    const b = parseInt(hex.slice(4, 6), 16)
    rgba = `rgba(${r}, ${g}, ${b}, ${props.glareOpacity})`
  }
  return {
    '--gh-br': props.borderRadius,
    '--gh-angle': `${props.glareAngle}deg`,
    '--gh-duration': `${props.transitionDuration}ms`,
    '--gh-size': `${props.glareSize}%`,
    '--gh-rgba': rgba,
  }
})
</script>

<style scoped>
.glare-hover {
  position: relative;
  overflow: hidden;
  display: block;
}

.glare-hover::before {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 1;
  background: linear-gradient(
    var(--gh-angle),
    hsla(0, 0%, 0%, 0) 60%,
    var(--gh-rgba) 70%,
    hsla(0, 0%, 0%, 0) 100%
  );
  transition: var(--gh-duration) ease;
  background-size: var(--gh-size) var(--gh-size), 100% 100%;
  background-repeat: no-repeat;
  background-position: -100% -100%, 0 0;
}

.glare-hover:hover::before {
  background-position: 100% 100%, 0 0;
}

.glare-hover.play-once::before {
  transition: none;
}

.glare-hover.play-once:hover::before {
  transition: var(--gh-duration) ease;
  background-position: 100% 100%, 0 0;
}

@media (prefers-reduced-motion: reduce) {
  .glare-hover::before {
    display: none;
  }
}
</style>
