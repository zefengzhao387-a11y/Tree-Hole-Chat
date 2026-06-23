<template>
  <div class="layout">
    <NavBar />
    <main class="main" :class="{ 'main-chat': isChat }">
      <router-view v-slot="{ Component }">
        <Suspense>
          <component :is="Component" />
          <template #fallback>
            <div class="route-loading">加载中…</div>
          </template>
        </Suspense>
      </router-view>
    </main>
  </div>
</template>
<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from '../components/NavBar.vue'

const route = useRoute()
const isChat = computed(() => route.name === 'TreeHoleChat')
</script>

<style scoped>
.layout {
  position: relative;
  min-height: 100vh;
}

.main {
  position: relative;
  z-index: 1;
  max-width: 720px;
  margin: 0 auto;
  padding: 88px 24px 48px;
}

.main-chat {
  max-width: 680px;
  padding-bottom: 24px;
}

.route-loading {
  padding: 48px 0;
  text-align: center;
  font-family: var(--font-ui);
  font-size: 0.875rem;
  color: var(--c-text-muted);
}
</style>