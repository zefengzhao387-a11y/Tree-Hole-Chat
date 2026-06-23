<template>
  <!-- 萤火虫粒子 — 灵感来源: React Bits Particles -->
  <canvas ref="canvasRef" class="particles-canvas" aria-hidden="true"></canvas>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const canvasRef = ref(null)
let animId = null
let particles = []

function initParticles(w, h) {
  const count = Math.min(40, Math.floor((w * h) / 25000))
  particles = Array.from({ length: count }, () => ({
    x: Math.random() * w,
    y: Math.random() * h,
    r: Math.random() * 2 + 0.8,
    vx: (Math.random() - 0.5) * 0.3,
    vy: (Math.random() - 0.5) * 0.25 - 0.1,
    phase: Math.random() * Math.PI * 2,
    hue: Math.random() > 0.5 ? '210, 180, 140' : '155, 181, 160',
  }))
}

function draw() {
  const canvas = canvasRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  const w = canvas.width
  const h = canvas.height

  ctx.clearRect(0, 0, w, h)

  const t = Date.now() * 0.001
  for (const p of particles) {
    p.x += p.vx
    p.y += p.vy
    if (p.x < -10) p.x = w + 10
    if (p.x > w + 10) p.x = -10
    if (p.y < -10) p.y = h + 10
    if (p.y > h + 10) p.y = -10

    const glow = 0.35 + 0.35 * Math.sin(t * 1.5 + p.phase)
    const grad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 4)
    grad.addColorStop(0, `rgba(${p.hue}, ${glow})`)
    grad.addColorStop(1, `rgba(${p.hue}, 0)`)
    ctx.fillStyle = grad
    ctx.beginPath()
    ctx.arc(p.x, p.y, p.r * 4, 0, Math.PI * 2)
    ctx.fill()
  }

  animId = requestAnimationFrame(draw)
}

function resize() {
  const canvas = canvasRef.value
  if (!canvas) return
  const dpr = Math.min(window.devicePixelRatio || 1, 2)
  const w = window.innerWidth
  const h = window.innerHeight
  canvas.width = w * dpr
  canvas.height = h * dpr
  canvas.style.width = w + 'px'
  canvas.style.height = h + 'px'
  const ctx = canvas.getContext('2d')
  ctx.scale(dpr, dpr)
  initParticles(w, h)
}

onMounted(() => {
  resize()
  draw()
  window.addEventListener('resize', resize)
})

onUnmounted(() => {
  cancelAnimationFrame(animId)
  window.removeEventListener('resize', resize)
})
</script>

<style scoped>
.particles-canvas {
  position: fixed;
  inset: 0;
  z-index: -3;
  pointer-events: none;
}
</style>
