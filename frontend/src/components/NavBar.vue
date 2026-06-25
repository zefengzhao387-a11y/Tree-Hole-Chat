<template>
  <header class="nav">
    <div class="nav-float">
      <router-link to="/diary" class="brand" aria-label="解忧树洞">
        <img src="/logo.png" alt="" class="brand-logo" />
        <span class="brand-text">解忧树洞</span>
      </router-link>

      <nav class="tabs" aria-label="主导航">
        <router-link
          v-for="item in links"
          :key="item.to"
          :to="item.to"
          class="tab"
          active-class="active"
        >
          {{ item.label }}
          <span
            v-if="item.to === '/my' && friendNotify.unreadTotal > 0"
            class="badge"
          >{{ friendNotify.unreadTotal > 99 ? '99+' : friendNotify.unreadTotal }}</span>
        </router-link>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { useFriendNotifyStore } from '../stores/friendNotify'

const friendNotify = useFriendNotifyStore()

const links = [
  { to: '/diary', label: '日记' },
  { to: '/chat', label: '树洞' },
  { to: '/trend', label: '心情' },
  { to: '/my', label: '我的' },
]
</script>

<style scoped>
.nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  padding: 14px 20px 0;
  pointer-events: none;
}

.nav-float {
  pointer-events: auto;
  max-width: 720px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  padding: 6px 6px 6px 14px;
  border-radius: 999px;
  background: rgba(255, 252, 248, 0.62);
  backdrop-filter: blur(18px) saturate(1.08);
  border: 1px solid rgba(255, 255, 255, 0.55);
  box-shadow:
    0 8px 32px rgba(58, 52, 46, 0.08),
    0 0 0 1px rgba(255, 255, 255, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.65);
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  flex-shrink: 0;
  font-family: var(--font-handwrite);
  font-size: 1.1875rem;
  font-weight: 400;
  color: var(--c-wood-deep);
  text-decoration: none;
  letter-spacing: 0.06em;
  text-shadow: var(--grass-shadow);
  transition: opacity var(--transition);
}

.brand:hover {
  opacity: 0.82;
}

.brand-logo {
  width: 26px;
  height: 26px;
  object-fit: contain;
  flex-shrink: 0;
  filter: drop-shadow(0 1px 2px rgba(90, 122, 98, 0.15));
}

.tabs {
  display: flex;
  align-items: center;
  gap: 2px;
  padding: 3px;
  border-radius: 999px;
  background: rgba(90, 122, 98, 0.07);
  border: 1px solid rgba(90, 122, 98, 0.06);
}

.tab {
  position: relative;
  padding: 7px 15px;
  border-radius: 999px;
  font-family: var(--font-ui);
  font-size: 0.8125rem;
  font-weight: 450;
  color: var(--c-text-dim);
  text-decoration: none;
  white-space: nowrap;
  transition:
    color 0.22s ease,
    background 0.22s ease,
    box-shadow 0.22s ease,
    transform 0.18s ease;
}

.tab:hover {
  color: var(--c-wood-deep);
  background: rgba(255, 252, 248, 0.45);
}

.tab.active {
  color: var(--c-wood-deep);
  font-weight: 500;
  background: rgba(255, 252, 248, 0.92);
  box-shadow:
    0 2px 8px rgba(58, 52, 46, 0.07),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
}

.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  margin-left: 4px;
  border-radius: 999px;
  font-family: var(--font-ui);
  font-size: 0.625rem;
  font-weight: 600;
  line-height: 1;
  color: #fff;
  background: var(--c-negative);
  vertical-align: middle;
}

.tab:active {
  transform: scale(0.97);
}

@media (max-width: 560px) {
  .nav {
    padding: 10px 12px 0;
  }

  .nav-float {
    flex-direction: column;
    align-items: stretch;
    gap: 8px;
    padding: 10px 10px 8px;
    border-radius: 20px;
  }

  .brand {
    justify-content: center;
    font-size: 1.0625rem;
  }

  .tabs {
    justify-content: space-between;
    border-radius: 14px;
  }

  .tab {
    flex: 1;
    text-align: center;
    padding: 8px 6px;
    font-size: 0.75rem;
  }
}

@media (max-width: 380px) {
  .brand-text {
    display: none;
  }

  .brand {
    justify-content: center;
  }
}

@media (prefers-reduced-motion: reduce) {
  .tab {
    transition: color 0.15s ease, background 0.15s ease;
  }

  .tab:active {
    transform: none;
  }
}
</style>
