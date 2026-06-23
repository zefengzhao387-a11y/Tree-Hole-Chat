<template>
  <!-- 灵感来源: React Bits Aurora — https://www.reactbits.dev/backgrounds/aurora -->
  <div class="aurora" aria-hidden="true">
    <div class="aurora-layer layer-1"></div>
    <div class="aurora-layer layer-2"></div>
    <div class="aurora-layer layer-3"></div>
    <div class="aurora-stars"></div>
  </div>
</template>

<style scoped>
.aurora {
  position: fixed;
  inset: 0;
  z-index: -5;
  overflow: hidden;
  background: linear-gradient(165deg, #1a1528 0%, #231e35 35%, #1e2438 70%, #1a1f2e 100%);
}

.aurora-layer {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.55;
  mix-blend-mode: screen;
  will-change: transform;
}

.layer-1 {
  width: 70vw;
  height: 70vw;
  max-width: 900px;
  max-height: 900px;
  top: -20%;
  left: -15%;
  background: radial-gradient(circle, rgba(196, 149, 106, 0.7) 0%, rgba(196, 149, 106, 0) 70%);
  animation: aurora-drift-1 18s ease-in-out infinite;
}

.layer-2 {
  width: 60vw;
  height: 60vw;
  max-width: 800px;
  max-height: 800px;
  top: 30%;
  right: -20%;
  background: radial-gradient(circle, rgba(155, 181, 160, 0.55) 0%, rgba(155, 181, 160, 0) 70%);
  animation: aurora-drift-2 22s ease-in-out infinite;
}

.layer-3 {
  width: 55vw;
  height: 55vw;
  max-width: 700px;
  max-height: 700px;
  bottom: -15%;
  left: 20%;
  background: radial-gradient(circle, rgba(180, 160, 210, 0.45) 0%, rgba(180, 160, 210, 0) 70%);
  animation: aurora-drift-3 26s ease-in-out infinite;
}

.aurora-stars {
  position: absolute;
  inset: 0;
  opacity: 0.35;
  background-image:
    radial-gradient(1px 1px at 10% 20%, rgba(255,255,255,0.6) 50%, transparent 50%),
    radial-gradient(1px 1px at 30% 65%, rgba(255,255,255,0.4) 50%, transparent 50%),
    radial-gradient(1.5px 1.5px at 55% 15%, rgba(255,255,255,0.5) 50%, transparent 50%),
    radial-gradient(1px 1px at 72% 42%, rgba(255,255,255,0.35) 50%, transparent 50%),
    radial-gradient(1px 1px at 88% 78%, rgba(255,255,255,0.45) 50%, transparent 50%),
    radial-gradient(1px 1px at 45% 88%, rgba(255,255,255,0.3) 50%, transparent 50%);
  animation: stars-twinkle 8s ease-in-out infinite alternate;
}

@keyframes aurora-drift-1 {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(8%, 5%) scale(1.08); }
  66% { transform: translate(-5%, 8%) scale(0.95); }
}

@keyframes aurora-drift-2 {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(-10%, -6%) scale(1.12); }
}

@keyframes aurora-drift-3 {
  0%, 100% { transform: translate(0, 0) scale(1); }
  40% { transform: translate(6%, -8%) scale(1.06); }
  80% { transform: translate(-8%, 4%) scale(0.92); }
}

@keyframes stars-twinkle {
  from { opacity: 0.25; }
  to { opacity: 0.45; }
}
</style>
