<template>
  <header class="hero">
    <div class="hero-bg" aria-hidden="true">
      <span class="orb orb-1"></span>
      <span class="orb orb-2"></span>
    </div>
    <div class="hero-content">
      <span v-if="badge" class="hero-badge">{{ badge }}</span>
      <ShimmerTitle :tag="titleTag" :size="size">{{ title }}</ShimmerTitle>
      <p v-if="desc" class="hero-desc">{{ desc }}</p>
      <div v-if="$slots.actions" class="hero-actions">
        <slot name="actions" />
      </div>
    </div>
    <div v-if="$slots.extra" class="hero-extra">
      <slot name="extra" />
    </div>
  </header>
</template>

<script setup>
import ShimmerTitle from '../ui/ShimmerTitle.vue'

defineProps({
  title: { type: String, required: true },
  desc: { type: String, default: '' },
  badge: { type: String, default: '' },
  titleTag: { type: String, default: 'h1' },
  size: { type: String, default: 'lg' },
})
</script>

<style scoped>
.hero {
  position: relative;
  margin-bottom: 28px;
  padding: 28px 24px;
  border-radius: var(--radius-xl);
  background: linear-gradient(135deg, var(--page-accent-soft) 0%, rgba(255,255,255,0.02) 60%);
  border: 1px solid var(--c-border);
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(40px);
}

.orb-1 {
  width: 180px;
  height: 180px;
  top: -60px;
  right: -40px;
  background: var(--page-glow);
  animation: orb-float 8s ease-in-out infinite;
}

.orb-2 {
  width: 120px;
  height: 120px;
  bottom: -40px;
  left: 10%;
  background: rgba(255, 255, 255, 0.04);
  animation: orb-float 10s ease-in-out infinite reverse;
}

@keyframes orb-float {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(-8px, 6px); }
}

.hero-content { position: relative; z-index: 1; }

.hero-badge {
  display: inline-block;
  font-family: var(--font-ui);
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  padding: 4px 12px;
  margin-bottom: 10px;
  border-radius: 100px;
  color: var(--page-accent);
  background: var(--page-accent-soft);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.hero-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 18px;
}

.hero-extra {
  position: relative;
  z-index: 1;
  margin-top: 20px;
  padding-top: 18px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}
</style>
