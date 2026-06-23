<template>
  <header class="nav">
    <div class="nav-inner">
      <router-link to="/diary" class="brand">
        <img src="/logo.png" alt="" class="brand-logo" />
        <span>解忧树洞</span>
      </router-link>
      <nav class="tabs">
        <router-link
          v-for="item in links"
          :key="item.to"
          :to="item.to"
          class="tab"
          active-class="active"
        >{{ item.label }}</router-link>
      </nav>
    </div>
  </header>
</template>

<script setup>
const links = [
  { to: '/diary', label: '日记' },
  { to: '/chat', label: '树洞' },
  { to: '/trend', label: '心情' },
  { to: '/settings', label: '设置' },
]
</script>

<style scoped>
.nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: rgba(247, 242, 234, 0.88);
  backdrop-filter: blur(14px);
  border-bottom: 1px solid rgba(228, 220, 208, 0.65);
}

.nav-inner {
  max-width: 720px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 56px;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-handwrite);
  font-size: 1.3125rem;
  font-weight: 400;
  color: var(--c-wood-deep);
  text-decoration: none;
  letter-spacing: 0.02em;
  text-shadow: var(--grass-shadow);
}

.brand-logo {
  width: 28px;
  height: 28px;
  object-fit: contain;
  flex-shrink: 0;
}

.tabs {
  display: flex;
  gap: 4px;
}

.tab {
  padding: 6px 14px;
  border-radius: var(--radius-sm);
  font-family: var(--font-ui);
  font-size: 0.8125rem;
  color: var(--c-text-dim);
  text-decoration: none;
  transition: color var(--transition), background var(--transition);
}

.tab:hover {
  color: var(--c-text);
  background: rgba(239, 232, 220, 0.5);
}

.tab.active {
  color: var(--c-wood-deep);
  background: rgba(255, 252, 248, 0.9);
  font-weight: 500;
  box-shadow: var(--shadow-sm);
}

@media (max-width: 480px) {
  .tab { padding: 6px 10px; font-size: 0.75rem; }
  .brand { font-size: 1.125rem; }
}
</style>
