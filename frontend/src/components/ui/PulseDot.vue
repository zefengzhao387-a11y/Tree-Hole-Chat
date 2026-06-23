<template>
  <!-- 灵感来源: Uiverse Status / Loader dots -->
  <span class="pulse-dot" :class="color">
    <span class="dot-core"></span>
    <span class="dot-ring"></span>
  </span>
</template>

<script setup>
defineProps({
  color: { type: String, default: 'sage' },
})
</script>

<style scoped>
.pulse-dot {
  position: relative;
  display: inline-flex;
  width: 10px;
  height: 10px;
}

.dot-core {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #8ab88a;
}

.dot-ring {
  position: absolute;
  inset: -3px;
  border-radius: 50%;
  border: 2px solid #8ab88a;
  animation: pulse-ring 2s ease-out infinite;
}

.pulse-dot.sage .dot-core { background: #8ab88a; }
.pulse-dot.sage .dot-ring { border-color: #8ab88a; }

.pulse-dot.gold .dot-core { background: #c4956a; }
.pulse-dot.gold .dot-ring { border-color: #c4956a; }

@keyframes pulse-ring {
  0% { transform: scale(0.8); opacity: 0.8; }
  70% { transform: scale(1.6); opacity: 0; }
  100% { transform: scale(1.6); opacity: 0; }
}
</style>
