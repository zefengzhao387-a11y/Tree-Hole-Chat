import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: () => import('../views/Landing.vue'),
    meta: { public: true, title: '首页' },
  },
  {
    path: '/auth',
    name: 'Auth',
    component: () => import('../views/Auth.vue'),
    meta: { public: true, title: '登录' },
  },
  {
    path: '/',
    component: () => import('../layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: 'diary', name: 'DiaryList', component: () => import('../views/DiaryList.vue'), meta: { title: '日记' } },
      { path: 'diary/new', name: 'DiaryNew', component: () => import('../views/DiaryEdit.vue'), meta: { title: '写日记' } },
      { path: 'diary/:id/edit', name: 'DiaryEdit', component: () => import('../views/DiaryEdit.vue'), meta: { title: '编辑日记' } },
      { path: 'chat', name: 'TreeHoleChat', component: () => import('../views/TreeHoleChat.vue'), meta: { title: '树洞' } },
      { path: 'trend', name: 'EmotionTrend', component: () => import('../views/EmotionTrend.vue'), meta: { title: '心情' } },
      { path: 'settings', name: 'Settings', component: () => import('../views/Settings.vue'), meta: { title: '设置' } },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return { path: '/auth', query: { redirect: to.fullPath } }
  }

  if (auth.isLoggedIn && to.name === 'Auth') {
    return { path: '/diary' }
  }

  return true
})

router.afterEach((to) => {
  document.title = `${to.meta.title || '解忧树洞'} · 解忧树洞`
})

export default router
