<template>
  <div class="tree-hole-ambient" aria-hidden="true">
    <div class="glow glow-warm" />
    <div class="glow glow-sage" />
    <div class="glow glow-center" />
    <div class="niche-glow niche-left">
      <span class="niche-core" />
    </div>
    <div class="niche-glow niche-right">
      <span class="niche-core" />
    </div>
    <div class="mote-layer">
      <span
        v-for="n in moteCount"
        :key="n"
        class="mote"
        :class="'mote-' + ((n % 3) + 1)"
        :style="moteStyle(n)"
      />
    </div>
  </div>
</template>

<script setup>
const moteCount = 24

function moteStyle(n) {
  const left = ((n * 23 + 9) % 93) + 3.5
  const delay = ((n * 0.72) % 9).toFixed(2)
  const duration = (11 + (n % 5) * 1.4).toFixed(1)
  const size = 3 + (n % 4) * 1.2
  const drift = ((n % 7) - 3) * 8
  return {
    left: `${left}%`,
    width: `${size}px`,
    height: `${size}px`,
    '--drift': `${drift}px`,
    animationDelay: `${delay}s`,
    animationDuration: `${duration}s`,
  }
}
</script>

<style scoped>
.tree-hole-ambient {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.mote-layer {
  position: absolute;
  inset: 0;
  z-index: 2;
}

/* ── 环境光晕 ── */
.glow {
  position: absolute;
  border-radius: 50%;
  will-change: transform, opacity;
  z-index: 0;
}

.glow-warm {
  width: min(56vw, 460px);
  height: min(52vw, 400px);
  top: 7%;
  left: 15%;
  background: radial-gradient(
    circle at 40% 40%,
    rgba(255, 220, 160, 0.55) 0%,
    rgba(210, 160, 95, 0.38) 45%,
    rgba(210, 160, 95, 0) 72%
  );
  filter: blur(58px);
  animation: glow-drift-a 12s cubic-bezier(0.45, 0, 0.55, 1) infinite;
}

.glow-sage {
  width: min(60vw, 500px);
  height: min(54vw, 420px);
  bottom: 5%;
  right: 8%;
  background: radial-gradient(
    circle at 55% 45%,
    rgba(130, 165, 130, 0.42) 0%,
    rgba(90, 122, 98, 0.28) 50%,
    rgba(90, 122, 98, 0) 72%
  );
  filter: blur(62px);
  animation: glow-drift-b 13s cubic-bezier(0.45, 0, 0.55, 1) infinite;
}

.glow-center {
  width: min(48vw, 380px);
  height: min(44vw, 340px);
  top: 35%;
  left: 50%;
  transform: translateX(-50%);
  background: radial-gradient(
    circle at 50% 45%,
    rgba(255, 252, 240, 0.62) 0%,
    rgba(255, 245, 220, 0.35) 55%,
    rgba(255, 248, 235, 0) 75%
  );
  filter: blur(52px);
  animation: glow-pulse 9s ease-in-out infinite;
}

/* ── 两侧树洞小灯 ── */
.niche-glow {
  position: absolute;
  width: min(20vw, 148px);
  height: min(20vw, 148px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
  animation: niche-pulse 4.5s ease-in-out infinite;
}

.niche-glow::before {
  content: '';
  position: absolute;
  inset: -20%;
  border-radius: 50%;
  background: radial-gradient(
    circle,
    rgba(255, 215, 140, 0.5) 0%,
    rgba(255, 190, 100, 0.22) 50%,
    transparent 72%
  );
  filter: blur(28px);
}

.niche-core {
  width: 28%;
  height: 28%;
  border-radius: 50%;
  background: radial-gradient(
    circle at 38% 32%,
    rgba(255, 248, 230, 0.95) 0%,
    rgba(255, 210, 130, 0.75) 55%,
    rgba(255, 180, 90, 0.35) 100%
  );
  box-shadow:
    0 0 12px rgba(255, 220, 150, 0.75),
    0 0 28px rgba(255, 200, 120, 0.45);
  animation: niche-core-flicker 4.5s ease-in-out infinite;
}

.niche-left {
  left: 7%;
  top: 41%;
  animation-delay: -1.2s;
}

.niche-right {
  right: 7%;
  top: 37%;
  animation-delay: -2.8s;
}

.niche-right .niche-core {
  animation-delay: -2.8s;
}

/* ── 浮尘微粒 ── */
.mote {
  position: absolute;
  bottom: -2%;
  border-radius: 50%;
  animation: mote-rise linear infinite;
}

.mote-1 {
  background: radial-gradient(
    circle at 35% 30%,
    rgba(255, 255, 252, 1) 0%,
    rgba(255, 248, 225, 0.85) 55%,
    rgba(255, 235, 190, 0.4) 100%
  );
  box-shadow:
    0 0 6px rgba(255, 250, 235, 0.95),
    0 0 14px rgba(255, 230, 180, 0.55);
}

.mote-2 {
  background: radial-gradient(
    circle at 40% 35%,
    rgba(255, 253, 248, 0.98) 0%,
    rgba(255, 244, 215, 0.75) 100%
  );
  box-shadow:
    0 0 5px rgba(255, 248, 228, 0.85),
    0 0 12px rgba(255, 220, 160, 0.45);
  border-radius: 45% 55% 50% 50%;
}

.mote-3 {
  background: rgba(255, 252, 245, 0.95);
  box-shadow:
    0 0 8px rgba(255, 250, 235, 1),
    0 0 18px rgba(255, 235, 200, 0.65);
}

@keyframes glow-drift-a {
  0%, 100% {
    transform: translate(0, 0) scale(1);
    opacity: 0.88;
  }
  50% {
    transform: translate(8%, 9%) scale(1.12);
    opacity: 1;
  }
}

@keyframes glow-drift-b {
  0%, 100% {
    transform: translate(0, 0) scale(1);
    opacity: 0.82;
  }
  50% {
    transform: translate(-9%, -7%) scale(1.1);
    opacity: 1;
  }
}

@keyframes glow-pulse {
  0%, 100% {
    transform: translateX(-50%) scale(0.9);
    opacity: 0.72;
  }
  50% {
    transform: translateX(-50%) scale(1.14);
    opacity: 1;
  }
}

@keyframes niche-pulse {
  0%, 100% {
    transform: scale(0.9);
    opacity: 0.72;
  }
  50% {
    transform: scale(1.15);
    opacity: 1;
  }
}

@keyframes niche-core-flicker {
  0%, 100% {
    opacity: 0.82;
    transform: scale(0.92);
  }
  35% {
    opacity: 1;
    transform: scale(1.05);
  }
  65% {
    opacity: 0.9;
    transform: scale(0.98);
  }
}

@keyframes mote-rise {
  0% {
    transform: translateY(0) translateX(0) scale(0.6);
    opacity: 0;
  }
  4% {
    opacity: 1;
  }
  30% {
    transform: translateY(-32vh) translateX(calc(var(--drift, 0px) * 0.35)) scale(1);
    opacity: 0.92;
  }
  55% {
    transform: translateY(-58vh) translateX(calc(var(--drift, 0px) * 0.7)) scale(0.95);
    opacity: 0.78;
  }
  80% {
    transform: translateY(-84vh) translateX(var(--drift, 0px)) scale(1);
    opacity: 0.55;
  }
  100% {
    transform: translateY(-110vh) translateX(calc(var(--drift, 0px) * 1.15)) scale(0.85);
    opacity: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .glow,
  .niche-glow,
  .niche-core,
  .mote {
    animation: none !important;
  }

  .glow-center {
    opacity: 0.78;
  }

  .niche-glow {
    opacity: 0.85;
  }
}
</style>
