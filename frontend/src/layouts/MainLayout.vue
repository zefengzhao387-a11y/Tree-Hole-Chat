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
import { computed, watch, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from '../components/NavBar.vue'
import TreeHoleAmbient from '../components/effects/TreeHoleAmbient.vue'
import { useAuthStore } from '../stores/auth'
import { useFriendNotifyStore } from '../stores/friendNotify'

const route = useRoute()
const auth = useAuthStore()
const friendNotify = useFriendNotifyStore()
const isChat = computed(() => route.name === 'TreeHoleChat' || route.name === 'FriendChat')

function syncNotifyPolling() {
  if (auth.isLoggedIn) {
    friendNotify.startPolling(() => route)
  } else {
    friendNotify.stopPolling()
  }
}

watch(() => auth.isLoggedIn, syncNotifyPolling)
watch(() => route.fullPath, () => friendNotify.poll(() => route))

onMounted(syncNotifyPolling)
onUnmounted(() => friendNotify.stopPolling())
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
  background:
    radial-gradient(ellipse 80% 60% at 50% 40%, rgba(247, 242, 234, 0.08), transparent 55%),
    linear-gradient(180deg, rgba(247, 242, 234, 0.28) 0%, rgba(239, 232, 220, 0.38) 100%);
  pointer-events: none;
}

.layout-bg::after {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  box-shadow: inset 0 0 120px rgba(58, 52, 46, 0.08);
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
