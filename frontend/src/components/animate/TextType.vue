<!-- 灵感来源: https://www.reactbits.dev/text-animations/text-type -->
<template>
  <component :is="tag" class="text-type">
    <span>{{ displayed }}</span>
    <span v-if="showCursor && !finished" class="cursor" aria-hidden="true">|</span>
  </component>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  text: { type: String, required: true },
  tag: { type: String, default: 'p' },
  speed: { type: Number, default: 55 },
  delay: { type: Number, default: 400 },
  showCursor: { type: Boolean, default: true },
  loop: { type: Boolean, default: false },
})

const displayed = ref('')
const finished = ref(false)
let timer = null
let index = 0

function clearTimer() {
  if (timer) {
    clearTimeout(timer)
    timer = null
  }
}

function typeNext() {
  if (index < props.text.length) {
    displayed.value += props.text[index]
    index += 1
    timer = setTimeout(typeNext, props.speed)
  } else {
    finished.value = true
    if (props.loop) {
      timer = setTimeout(resetAndStart, 2400)
    }
  }
}

function resetAndStart() {
  displayed.value = ''
  index = 0
  finished.value = false
  timer = setTimeout(typeNext, props.delay)
}

function start() {
  clearTimer()
  displayed.value = ''
  index = 0
  finished.value = false
  timer = setTimeout(typeNext, props.delay)
}

watch(() => props.text, start)

onMounted(start)
onUnmounted(clearTimer)
</script>

<style scoped>
.text-type {
  display: inline;
}

.cursor {
  display: inline-block;
  margin-left: 1px;
  color: var(--c-primary);
  animation: cursor-blink 0.9s step-end infinite;
}

@keyframes cursor-blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

@media (prefers-reduced-motion: reduce) {
  .cursor { display: none; }
}
</style>
