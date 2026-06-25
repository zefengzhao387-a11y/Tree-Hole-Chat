<template>
  <div class="layout">
    <div class="layout-bg" aria-hidden="true">
      <div class="layout-bg-image" />
      <div class="layout-bg-scrim" />
      <TreeHoleAmbient />
    </div>
    <NavBar />
    <main class="main" :class="{ 'main-chat': isChat }">
      <router-view />
    </main>
  </div>
</template>
<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from '../components/NavBar.vue'
import TreeHoleAmbient from '../components/effects/TreeHoleAmbient.vue'

const route = useRoute()
const isChat = computed(() => route.name === 'TreeHoleChat')
</script>

<style scoped>
.layout {
  position: relative;
  min-height: 100vh;
  isolation: isolate;
}

.layout-bg {
  position: fixed;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  background-color: #efe8dc;
}

.layout-bg-image {
  position: absolute;
  inset: 0;
  background: url('/bg/tree-hole-interior.png') center / cover no-repeat;
}

.layout-bg-scrim {
  position: absolute;
  inset: 0;
  background: rgba(247, 242, 234, 0.24);
  pointer-events: none;
}

.main {
  position: relative;
  z-index: 1;
  max-width: 720px;
  margin: 0 auto;
  padding: 92px 24px 48px;
}

.main-chat {
  max-width: 680px;
  padding-bottom: 24px;
}
</style>
