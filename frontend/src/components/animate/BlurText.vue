<!-- 灵感来源: https://www.reactbits.dev/text-animations/blur-text -->
<template>
  <component :is="tag" ref="targetRef" class="blur-text" :class="[className, `dir-${direction}`]">
    <span
      v-for="(segment, index) in segments"
      :key="`${segment}-${index}`"
      class="blur-text-segment"
      :class="{ visible: inView }"
      :style="{ animationDelay: `${index * delay}ms` }"
    >{{ displaySegment(segment, index) }}</span>
  </component>
</template>

<script setup>
import { computed } from 'vue'
import { useInView } from '../../composables/useInView'

const props = defineProps({
  text: { type: String, default: '' },
  tag: { type: String, default: 'span' },
  className: { type: String, default: '' },
  animateBy: { type: String, default: 'words' }, // words | chars
  delay: { type: Number, default: 80 },
  direction: { type: String, default: 'top' }, // top | bottom
})

const { targetRef, inView } = useInView({ threshold: 0.15 })

const segments = computed(() => {
  if (!props.text) return []
  return props.animateBy === 'chars' ? [...props.text] : props.text.split(' ')
})

function displaySegment(segment, index) {
  if (props.animateBy === 'words' && index < segments.value.length - 1) {
    return segment + '\u00A0'
  }
  return segment === ' ' ? '\u00A0' : segment
}
</script>

<style scoped>
.blur-text {
  display: inline;
}

.blur-text-segment {
  display: inline-block;
  will-change: transform, filter, opacity;
  filter: blur(10px);
  opacity: 0;
}

.dir-top .blur-text-segment { transform: translateY(-18px); }
.dir-bottom .blur-text-segment { transform: translateY(18px); }

.blur-text-segment.visible {
  animation: blur-text-in-top 0.65s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}

.dir-bottom .blur-text-segment.visible {
  animation-name: blur-text-in-bottom;
}

@keyframes blur-text-in-top {
  0% { filter: blur(10px); opacity: 0; transform: translateY(-18px); }
  55% { filter: blur(4px); opacity: 0.65; transform: translateY(4px); }
  100% { filter: blur(0); opacity: 1; transform: translateY(0); }
}

@keyframes blur-text-in-bottom {
  0% { filter: blur(10px); opacity: 0; transform: translateY(18px); }
  55% { filter: blur(4px); opacity: 0.65; transform: translateY(-4px); }
  100% { filter: blur(0); opacity: 1; transform: translateY(0); }
}

@media (prefers-reduced-motion: reduce) {
  .blur-text-segment {
    filter: none;
    opacity: 1;
    transform: none;
    animation: none !important;
  }
}
</style>
