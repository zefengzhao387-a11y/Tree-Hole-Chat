<!-- 灵感来源: https://www.reactbits.dev/text-animations/count-up -->
<template>
  <span ref="targetRef" class="count-up">{{ formatted }}</span>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useInView } from '../../composables/useInView'

const props = defineProps({
  value: { type: Number, default: 0 },
  duration: { type: Number, default: 900 },
  decimals: { type: Number, default: 0 },
})

const { targetRef, inView } = useInView({ threshold: 0.3 })
const current = ref(0)
let raf = null

const formatted = computed(() => {
  if (props.decimals > 0) return current.value.toFixed(props.decimals)
  return Math.round(current.value).toString()
})

function animateTo(target) {
  if (raf) cancelAnimationFrame(raf)
  const start = performance.now()
  const from = current.value

  const tick = (now) => {
    const t = Math.min((now - start) / props.duration, 1)
    const eased = 1 - Math.pow(1 - t, 3)
    current.value = from + (target - from) * eased
    if (t < 1) raf = requestAnimationFrame(tick)
    else current.value = target
  }
  raf = requestAnimationFrame(tick)
}

watch(inView, (v) => {
  if (v) animateTo(props.value)
})

watch(() => props.value, (v) => {
  if (inView.value) animateTo(v)
})

onMounted(() => {
  if (inView.value) animateTo(props.value)
})
</script>

<style scoped>
.count-up {
  font-variant-numeric: tabular-nums;
}
</style>
