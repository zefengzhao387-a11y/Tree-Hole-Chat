<template>
  <router-view v-slot="{ Component, route }">
    <transition name="page-center" mode="out-in">
      <component :is="Component" :key="route.fullPath" class="page-view" />
    </transition>
  </router-view>
</template>

<script setup>
</script>

<style>
@import './styles/theme.css';

* { margin: 0; padding: 0; box-sizing: border-box; }

html { font-size: 16px; -webkit-font-smoothing: antialiased; }

body {
  font-family: var(--font-display);
  color: var(--c-text);
  background-color: var(--c-bg);
  background-image:
    radial-gradient(ellipse 120% 80% at 50% -10%, rgba(90, 122, 98, 0.07), transparent 50%),
    repeating-linear-gradient(
      92deg,
      transparent 0,
      transparent 3px,
      rgba(139, 115, 85, 0.028) 3px,
      rgba(139, 115, 85, 0.028) 4px
    ),
    repeating-linear-gradient(
      0deg,
      transparent 0,
      transparent 11px,
      rgba(160, 130, 95, 0.018) 11px,
      rgba(160, 130, 95, 0.018) 12px
    ),
    linear-gradient(180deg, #f7f2ea 0%, #f0e8dc 100%);
  line-height: 1.7;
}

.app {
  min-height: 100vh;
  background:
    radial-gradient(ellipse 100% 60% at 50% -20%, rgba(90, 122, 98, 0.07), transparent),
    var(--c-bg);
}

.page-view {
  min-height: 100vh;
  width: 100%;
}

.page-center-enter-active,
.page-center-leave-active {
  transition:
    opacity 0.42s cubic-bezier(0.4, 0, 0.2, 1),
    transform 0.42s cubic-bezier(0.4, 0, 0.2, 1),
    filter 0.42s cubic-bezier(0.4, 0, 0.2, 1);
  transform-origin: center center;
}

.page-center-enter-from {
  opacity: 0;
  transform: scale(0.94) translateY(12px);
  filter: blur(4px);
}

.page-center-leave-to {
  opacity: 0;
  transform: scale(1.04) translateY(-8px);
  filter: blur(3px);
}

@media (prefers-reduced-motion: reduce) {
  .page-center-enter-active,
  .page-center-leave-active {
    transition: opacity 0.2s ease;
  }

  .page-center-enter-from,
  .page-center-leave-to {
    transform: none;
    filter: none;
  }
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 22px;
  border: none;
  border-radius: var(--radius-sm);
  font-family: var(--font-ui);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background var(--transition), color var(--transition);
  text-decoration: none;
}

.btn-primary {
  background: linear-gradient(145deg, #5c4a38 0%, #4a3d30 100%);
  color: #f5ebe0;
  box-shadow:
    0 4px 14px rgba(74, 61, 48, 0.22),
    inset 0 1px 0 rgba(255, 255, 255, 0.12);
  transition:
    background var(--transition),
    transform var(--transition),
    box-shadow var(--transition);
}
.btn-primary:hover {
  background: linear-gradient(145deg, #4a3d30 0%, #3d3228 100%);
  box-shadow: 0 6px 20px rgba(74, 61, 48, 0.28);
  transform: translateY(-1px);
}
.btn-primary:active { transform: translateY(0); }
.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-ghost {
  background: rgba(255, 252, 248, 0.5);
  color: var(--c-text-dim);
  border: 1px solid var(--c-border);
  backdrop-filter: blur(8px);
}
.btn-ghost:hover {
  background: rgba(255, 252, 248, 0.85);
  color: var(--c-text);
  border-color: rgba(184, 137, 94, 0.35);
}

.btn-block { width: 100%; padding: 12px; }

.input-heal,
.textarea-heal {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid var(--c-border);
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.88);
  font-family: var(--font-display);
  font-size: 0.9375rem;
  color: var(--c-text);
  outline: none;
  transition: border-color var(--transition), box-shadow var(--transition), background var(--transition);
}

.textarea-heal { line-height: 1.85; resize: vertical; }

.input-heal:focus,
.textarea-heal:focus {
  border-color: var(--c-primary);
  background: #fff;
  box-shadow: 0 0 0 3px rgba(90, 122, 98, 0.12);
}

.input-heal::placeholder,
.textarea-heal::placeholder { color: var(--c-text-muted); }

.el-input__wrapper {
  border-radius: var(--radius-sm) !important;
  background: #fff !important;
  border: 1px solid var(--c-border) !important;
  box-shadow: none !important;
}

.el-input__wrapper.is-focus {
  border-color: var(--c-primary) !important;
  box-shadow: none !important;
}

.el-input__inner,
.el-range-input { color: var(--c-text) !important; background: transparent !important; }
.el-range-separator { color: var(--c-text-dim) !important; }

.el-pagination button,
.el-pager li {
  background: #fff !important;
  color: var(--c-text-dim) !important;
  border: 1px solid var(--c-border) !important;
}

.el-pager li.is-active {
  background: rgba(255, 252, 248, 0.95) !important;
  color: var(--c-wood-deep) !important;
  border-color: var(--c-wood) !important;
}

.el-message-box {
  background: var(--c-surface) !important;
  border: 1px solid var(--c-border) !important;
  border-radius: var(--radius-lg) !important;
}

.el-message-box__title,
.el-message-box__message { color: var(--c-text) !important; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-thumb { background: var(--c-border); border-radius: 3px; }
::selection { background: var(--c-primary-soft); }
</style>
