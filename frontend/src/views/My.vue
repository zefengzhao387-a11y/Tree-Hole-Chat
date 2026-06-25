<template>
  <div class="page">
    <header class="page-header stack">
      <BlurText tag="h1" class="page-title" text="我的" animate-by="chars" :delay="80" />
      <p class="page-desc">账号、好友与陪伴</p>
    </header>

    <div v-if="pageLoading" class="state-loading" aria-busy="true" aria-label="加载中">
      <div class="card pad section sk-profile">
        <div class="sk-avatar" />
        <div class="sk-profile-lines">
          <div class="sk-line sk-name" />
          <div class="sk-line sk-meta" />
        </div>
      </div>
      <SkeletonList :count="3" />
    </div>

    <template v-else>
      <!-- 个人名片 -->
      <FadeContent direction="up">
        <div class="card pad section profile-hero">
          <div class="hero-top">
            <div class="profile-row">
              <span class="avatar">{{ avatarChar }}</span>
              <div>
                <p class="greeting">{{ greeting }}，{{ auth.user?.nickname || auth.user?.username }}</p>
                <p class="profile-meta">@{{ auth.user?.username }} · 陪伴 {{ memberDays }} 天</p>
                <div v-if="stats?.latest_emotion" class="mood-row">
                  <span class="mood-label">最近心情</span>
                  <EmotionBadge
                    :emotion="stats.latest_emotion"
                    :sentiment="stats.latest_sentiment || 'neutral'"
                    :intensity="stats.latest_intensity"
                  />
                </div>
              </div>
            </div>
            <button class="btn btn-ghost logout-btn" @click="logout">退出</button>
          </div>
          <p class="daily-quote">「{{ dailyQuote }}」</p>
        </div>
      </FadeContent>

      <!-- 快捷入口 -->
      <FadeContent direction="up" :delay="60">
        <div class="card pad section">
          <h2 class="section-label">快捷入口</h2>
          <div class="shortcut-grid">
            <router-link
              v-for="item in shortcuts"
              :key="item.label"
              :to="item.to"
              class="shortcut"
            >
              <span class="shortcut-icon" aria-hidden="true">
                <svg v-if="item.icon === 'write'" class="retro-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M6 3h12v18H6z" />
                  <path d="M9 7h6M9 11h5M9 15h3" />
                  <path d="M14 16l4 4M17 16l1-3" />
                </svg>
                <svg v-else-if="item.icon === 'hole'" class="retro-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 21V13" />
                  <path d="M8 21h8" />
                  <path d="M12 13c-3.5-2.5-5-6-3.5-8.5C9.5 2.5 12 2 12 2s2.5.5 3.5 2.5C17 7 15.5 10.5 12 13z" />
                  <circle cx="12" cy="15.5" r="1.25" fill="currentColor" stroke="none" />
                </svg>
                <svg v-else-if="item.icon === 'mood'" class="retro-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M4 19V5" />
                  <path d="M4 19h16" />
                  <path d="M7 15l3-5 3 3 4-7" />
                </svg>
                <svg v-else class="retro-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M5 4h14v16H5z" />
                  <path d="M9 4v16" />
                  <path d="M5 8h4M5 12h4M5 16h4" />
                </svg>
              </span>
              <span class="shortcut-label">{{ item.label }}</span>
              <span class="shortcut-desc">{{ item.desc }}</span>
            </router-link>
          </div>
        </div>
      </FadeContent>

      <!-- 消息提醒 -->
      <FadeContent v-if="unreadItems.length" direction="up" :delay="100">
        <div class="card pad section">
          <h2 class="section-label">新消息</h2>
          <ul class="msg-preview-list">
            <li
              v-for="item in unreadItems"
              :key="item.last_message_id"
              class="msg-preview"
              @click="openChat(item.friend)"
            >
              <span class="mini-avatar">{{ nameChar(item.friend) }}</span>
              <div class="msg-preview-body">
                <div class="msg-preview-head">
                  <b>{{ item.friend.nickname || item.friend.username }}</b>
                  <span class="msg-count">{{ item.unread_count }} 条未读</span>
                </div>
                <p class="msg-preview-text">{{ item.last_content }}</p>
              </div>
            </li>
          </ul>
        </div>
      </FadeContent>

      <!-- 添加好友 -->
      <FadeContent direction="up" :delay="120">
        <div class="card pad section">
          <h2 class="section-label">添加好友</h2>
          <p class="hint">输入对方用户名搜索并发送好友请求</p>
          <div class="add-row">
            <input
              v-model="searchQ"
              class="input-heal"
              placeholder="搜索用户名…"
              @keydown.enter.prevent="searchUsers"
            />
            <button class="btn btn-primary" :disabled="searchQ.trim().length < 2" @click="searchUsers">
              搜索
            </button>
          </div>
          <ul v-if="searchResults.length" class="search-list">
            <li v-for="u in searchResults" :key="u.id" class="search-item">
              <div>
                <b>{{ u.nickname || u.username }}</b>
                <span class="muted">@{{ u.username }}</span>
              </div>
              <button class="btn btn-ghost btn-sm" @click="addFriend(u.username)">加好友</button>
            </li>
          </ul>
        </div>
      </FadeContent>

      <FadeContent v-if="pending.length" direction="up" :delay="140">
        <div class="card pad section">
          <h2 class="section-label">好友请求</h2>
          <ul class="friend-list">
            <li v-for="item in pending" :key="item.id" class="friend-item">
              <div class="friend-info">
                <span class="mini-avatar">{{ nameChar(item.user) }}</span>
                <div>
                  <b>{{ item.user.nickname || item.user.username }}</b>
                  <span class="muted">@{{ item.user.username }}</span>
                </div>
              </div>
              <div v-if="item.is_incoming" class="friend-actions">
                <button class="btn btn-primary btn-sm" @click="accept(item.id)">接受</button>
                <button class="btn btn-ghost btn-sm" @click="reject(item.id)">拒绝</button>
              </div>
              <span v-else class="tag">等待确认</span>
            </li>
          </ul>
        </div>
      </FadeContent>

      <FadeContent direction="up" :delay="160">
        <div class="card pad section">
          <h2 class="section-label">我的好友</h2>
          <div v-if="loading" class="list-loading">
            <span class="loading-dot" /><span class="loading-dot" /><span class="loading-dot" />
          </div>
          <div v-else-if="!friends.length" class="empty-card">
            <span class="empty-icon">🌿</span>
            <p class="empty-title">还没有树洞伙伴</p>
            <p class="empty-desc">找一位好友，一起分享心情、互相倾听</p>
            <ol class="empty-steps">
              <li>在上方搜索对方的用户名</li>
              <li>发送好友请求并等待确认</li>
              <li>通过后即可开始私信聊天</li>
            </ol>
          </div>
          <ul v-else class="friend-list">
            <li v-for="item in friends" :key="item.id" class="friend-item">
              <div class="friend-info">
                <span class="mini-avatar">{{ nameChar(item.user) }}</span>
                <div>
                  <b>{{ item.user.nickname || item.user.username }}</b>
                  <span class="muted">@{{ item.user.username }}</span>
                </div>
              </div>
              <div class="friend-actions">
                <button class="btn btn-primary btn-sm chat-btn" @click="openChat(item.user)">
                  聊天
                  <span v-if="unreadCount(item.user.id)" class="friend-badge">
                    {{ unreadCount(item.user.id) > 99 ? '99+' : unreadCount(item.user.id) }}
                  </span>
                </button>
                <button class="btn btn-ghost btn-sm" @click="removeFriend(item)">删除</button>
              </div>
            </li>
          </ul>
        </div>
      </FadeContent>

      <FadeContent v-if="stats" direction="up" :delay="200">
        <div class="card pad section">
          <h2 class="section-label">我的足迹</h2>
          <div class="stats">
            <div class="stat"><b>{{ stats.diary_count }}</b><span>日记</span></div>
            <div class="stat"><b>{{ stats.analysis_count }}</b><span>分析</span></div>
            <div class="stat"><b>{{ stats.conversation_count }}</b><span>树洞对话</span></div>
            <div class="stat"><b>{{ stats.friend_count || 0 }}</b><span>好友</span></div>
          </div>
        </div>
      </FadeContent>

      <FadeContent direction="up" :delay="240">
        <div class="card pad section about">
          <h2 class="section-label">关于解忧树洞</h2>
          <p>在这里，日记被读懂、烦忧有人听、朋友彼此陪伴。</p>
          <p class="muted">Vue 3 · FastAPI · LangChain · Chroma · DeepSeek</p>
        </div>
      </FadeContent>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '../api'
import { friendsAPI } from '../api/friends'
import { useAuthStore } from '../stores/auth'
import { useFriendNotifyStore } from '../stores/friendNotify'
import BlurText from '../components/animate/BlurText.vue'
import FadeContent from '../components/animate/FadeContent.vue'
import SkeletonList from '../components/ui/SkeletonList.vue'
import EmotionBadge from '../components/EmotionBadge.vue'

const QUOTES = [
  '每一份心情，都值得被温柔以待',
  '把烦忧交给树洞，把真实留给自己',
  '记录今天，是为了更好地遇见明天',
  '有人倾听，心事便轻了一半',
  '情绪没有对错，它只是来过',
  '在文字里安顿自己，在对话里找到光',
  '你不必一直坚强，树洞一直都在',
]

const shortcuts = [
  { icon: 'write', label: '写日记', desc: '记录此刻', to: '/diary/new' },
  { icon: 'hole', label: '树洞', desc: '和小树聊聊', to: '/chat' },
  { icon: 'mood', label: '心情', desc: '看情绪轨迹', to: '/trend' },
  { icon: 'book', label: '日记本', desc: '翻阅过往', to: '/diary' },
]

const router = useRouter()
const auth = useAuthStore()
const friendNotify = useFriendNotifyStore()
const { unreadByFriend } = storeToRefs(friendNotify)

const pageLoading = ref(true)
const loading = ref(false)
const stats = ref(null)
const friends = ref([])
const pending = ref([])
const unreadItems = ref([])
const searchQ = ref('')
const searchResults = ref([])

const avatarChar = computed(() => {
  const name = auth.user?.nickname || auth.user?.username || '?'
  return name.charAt(0)
})

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 6) return '夜深了'
  if (h < 12) return '早安'
  if (h < 18) return '午安'
  return '晚安'
})

const dailyQuote = computed(() => QUOTES[new Date().getDate() % QUOTES.length])

const memberDays = computed(() => {
  if (!stats.value?.member_since) return 1
  const start = new Date(stats.value.member_since)
  const diff = Date.now() - start.getTime()
  return Math.max(1, Math.ceil(diff / (1000 * 60 * 60 * 24)))
})

function nameChar(user) {
  return (user?.nickname || user?.username || '?').charAt(0)
}

function unreadCount(friendId) {
  return unreadByFriend.value[friendId] || 0
}

async function loadUnread() {
  try {
    const { data } = await friendsAPI.getUnreadSummary()
    unreadItems.value = data.items || []
  } catch { /* ignore */ }
}

async function loadFriends() {
  loading.value = true
  try {
    const { data } = await friendsAPI.list()
    friends.value = data.friends || []
    pending.value = data.pending || []
  } catch {
    ElMessage.error('加载好友列表失败')
  } finally {
    loading.value = false
  }
}

async function searchUsers() {
  const q = searchQ.value.trim()
  if (q.length < 2) return
  try {
    const { data } = await friendsAPI.search(q)
    searchResults.value = data || []
    if (!searchResults.value.length) ElMessage.info('未找到匹配用户')
  } catch {
    ElMessage.error('搜索失败')
  }
}

async function addFriend(username) {
  try {
    await friendsAPI.sendRequest(username)
    ElMessage.success('好友请求已发送')
    searchResults.value = []
    searchQ.value = ''
    await loadFriends()
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '发送失败')
  }
}

async function accept(id) {
  try {
    await friendsAPI.accept(id)
    ElMessage.success('已添加好友')
    await loadFriends()
    await loadUnread()
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '操作失败')
  }
}

async function reject(id) {
  try {
    await friendsAPI.reject(id)
    await loadFriends()
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '操作失败')
  }
}

async function removeFriend(item) {
  try {
    await ElMessageBox.confirm(
      `确定删除好友「${item.user.nickname || item.user.username}」吗？`,
      '确认',
      { confirmButtonText: '删除', cancelButtonText: '取消' },
    )
    await friendsAPI.remove(item.id)
    ElMessage.success('已删除好友')
    await loadFriends()
    await loadUnread()
  } catch { /* cancelled */ }
}

function openChat(user) {
  router.push({
    name: 'FriendChat',
    params: { friendId: user.id },
    query: { name: user.nickname || user.username },
  })
}

function logout() {
  auth.logout()
  router.replace('/')
}

onMounted(async () => {
  try {
    await Promise.all([
      loadFriends(),
      loadUnread(),
      api.get('/system/stats').then(({ data }) => { stats.value = data }).catch(() => {}),
    ])
  } finally {
    pageLoading.value = false
  }
})
</script>

<style scoped>
.section { margin-bottom: 12px; }

.state-loading {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.sk-profile {
  display: flex;
  align-items: center;
  gap: 14px;
}

.sk-avatar {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  flex-shrink: 0;
  background: linear-gradient(90deg, rgba(228, 220, 208, 0.45) 0%, rgba(255, 252, 248, 0.9) 50%, rgba(228, 220, 208, 0.45) 100%);
  background-size: 200% 100%;
  animation: shimmer-load 1.4s ease-in-out infinite;
}

.sk-profile-lines { flex: 1; display: flex; flex-direction: column; gap: 10px; }

.sk-line {
  height: 12px;
  border-radius: 6px;
  background: linear-gradient(90deg, rgba(228, 220, 208, 0.45) 0%, rgba(255, 252, 248, 0.9) 50%, rgba(228, 220, 208, 0.45) 100%);
  background-size: 200% 100%;
  animation: shimmer-load 1.4s ease-in-out infinite;
}

.sk-name { width: 120px; height: 16px; }
.sk-meta { width: 80px; height: 10px; animation-delay: 0.12s; }

@keyframes shimmer-load {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.list-loading {
  display: flex;
  justify-content: center;
  gap: 6px;
  padding: 20px 0;
}

.loading-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--c-primary);
  opacity: 0.35;
  animation: dot-bounce 0.9s ease-in-out infinite;
}

.loading-dot:nth-child(2) { animation-delay: 0.15s; }
.loading-dot:nth-child(3) { animation-delay: 0.3s; }

@keyframes dot-bounce {
  0%, 80%, 100% { transform: translateY(0); opacity: 0.35; }
  40% { transform: translateY(-6px); opacity: 1; }
}

@media (prefers-reduced-motion: reduce) {
  .sk-avatar, .sk-line { animation: none; background: rgba(228, 220, 208, 0.5); }
  .loading-dot { animation: none; opacity: 0.6; }
}

.profile-hero {
  background:
    linear-gradient(135deg, rgba(238, 244, 239, 0.55) 0%, rgba(255, 252, 248, 0.95) 60%),
    rgba(255, 252, 248, 0.9);
  border-color: rgba(90, 122, 98, 0.12);
}

.hero-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.profile-row {
  display: flex;
  align-items: center;
  gap: 14px;
}

.avatar {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-handwrite);
  font-size: 1.5rem;
  color: var(--c-wood-deep);
  background: linear-gradient(145deg, rgba(255, 248, 240, 0.95), rgba(238, 244, 239, 0.85));
  border: 1px solid rgba(90, 122, 98, 0.25);
  border-radius: 50%;
  box-shadow: 0 4px 14px rgba(90, 122, 98, 0.1);
}

.greeting {
  font-family: var(--font-handwrite);
  font-size: 1.375rem;
  color: var(--c-wood-deep);
  letter-spacing: 0.04em;
  margin-bottom: 4px;
}

.profile-meta {
  font-family: var(--font-ui);
  font-size: 0.8125rem;
  color: var(--c-text-muted);
}

.mood-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
}

.mood-label {
  font-family: var(--font-ui);
  font-size: 0.75rem;
  color: var(--c-text-muted);
}

.daily-quote {
  margin-top: 16px;
  padding-top: 14px;
  border-top: 1px dashed rgba(228, 220, 208, 0.8);
  font-family: var(--font-ui);
  font-size: 0.875rem;
  color: var(--c-warm);
  font-style: italic;
  letter-spacing: 0.04em;
  line-height: 1.6;
}

.logout-btn { flex-shrink: 0; }

.shortcut-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}

.shortcut {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 14px 8px;
  border-radius: var(--radius-sm);
  background: rgba(255, 252, 248, 0.7);
  border: 1px solid rgba(228, 220, 208, 0.6);
  text-decoration: none;
  transition: transform var(--transition), box-shadow var(--transition), border-color var(--transition);
}

.shortcut:hover {
  transform: translateY(-2px);
  border-color: rgba(90, 122, 98, 0.2);
  box-shadow: 0 6px 18px rgba(58, 52, 46, 0.08);
}

.shortcut-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: rgba(244, 237, 228, 0.65);
  border: 1px solid rgba(139, 115, 85, 0.2);
  color: var(--c-wood-deep);
  box-shadow: inset 0 1px 0 rgba(255, 252, 248, 0.8);
}

.retro-icon {
  width: 18px;
  height: 18px;
}

.shortcut-label {
  font-family: var(--font-ui);
  font-size: 0.8125rem;
  font-weight: 500;
  color: var(--c-text);
}

.shortcut-desc {
  font-family: var(--font-ui);
  font-size: 0.6875rem;
  color: var(--c-text-muted);
}

.msg-preview-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.msg-preview {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 14px;
  border-radius: var(--radius-sm);
  background: rgba(238, 244, 239, 0.45);
  border: 1px solid rgba(90, 122, 98, 0.12);
  cursor: pointer;
  transition: background var(--transition), transform var(--transition);
}

.msg-preview:hover {
  background: rgba(238, 244, 239, 0.75);
  transform: translateX(2px);
}

.msg-preview-body { flex: 1; min-width: 0; }

.msg-preview-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 4px;
}

.msg-preview-head b {
  font-family: var(--font-ui);
  font-size: 0.875rem;
  color: var(--c-text);
}

.msg-count {
  font-family: var(--font-ui);
  font-size: 0.6875rem;
  color: var(--c-negative);
  flex-shrink: 0;
}

.msg-preview-text {
  font-family: var(--font-ui);
  font-size: 0.8125rem;
  color: var(--c-text-dim);
  line-height: 1.5;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.hint {
  font-family: var(--font-ui);
  font-size: 0.8125rem;
  color: var(--c-text-muted);
  margin-bottom: 12px;
}

.add-row { display: flex; gap: 10px; }
.add-row .input-heal { flex: 1; }

.search-list,
.friend-list {
  list-style: none;
  padding: 0;
  margin: 12px 0 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.search-item,
.friend-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 12px 14px;
  border-radius: var(--radius-sm);
  background: rgba(255, 252, 248, 0.65);
  border: 1px solid rgba(228, 220, 208, 0.6);
}

.friend-info {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.mini-avatar {
  width: 36px;
  height: 36px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-handwrite);
  font-size: 0.9375rem;
  color: var(--c-wood-deep);
  background: rgba(238, 244, 239, 0.9);
  border-radius: 50%;
  border: 1px solid rgba(90, 122, 98, 0.15);
}

.search-item b,
.friend-item b {
  display: block;
  font-family: var(--font-ui);
  font-size: 0.875rem;
  color: var(--c-text);
}

.muted {
  font-family: var(--font-ui);
  font-size: 0.75rem;
  color: var(--c-text-muted);
}

.friend-actions { display: flex; gap: 8px; flex-shrink: 0; }
.btn-sm { padding: 6px 12px; font-size: 0.8125rem; }
.chat-btn { position: relative; }

.friend-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  margin-left: 4px;
  border-radius: 999px;
  font-size: 0.625rem;
  font-weight: 600;
  color: #fff;
  background: var(--c-negative);
}

.tag {
  font-family: var(--font-ui);
  font-size: 0.75rem;
  color: var(--c-warm);
}

.empty-card {
  text-align: center;
  padding: 24px 16px 12px;
}

.empty-icon { font-size: 2rem; display: block; margin-bottom: 8px; }

.empty-title {
  font-family: var(--font-handwrite);
  font-size: 1.125rem;
  color: var(--c-wood-deep);
  margin-bottom: 6px;
}

.empty-desc {
  font-family: var(--font-ui);
  font-size: 0.8125rem;
  color: var(--c-text-muted);
  margin-bottom: 14px;
}

.empty-steps {
  text-align: left;
  max-width: 280px;
  margin: 0 auto;
  padding-left: 20px;
  font-family: var(--font-ui);
  font-size: 0.8125rem;
  color: var(--c-text-dim);
  line-height: 1.8;
}

.stats {
  display: flex;
  gap: 12px;
  margin-top: 4px;
}

.stat {
  flex: 1;
  text-align: center;
  padding: 18px 12px;
  background: rgba(255, 252, 248, 0.65);
  border-radius: var(--radius-sm);
  border: 1px solid rgba(228, 220, 208, 0.6);
  transition: transform var(--transition);
}

.stat:hover { transform: translateY(-2px); }

.stat b {
  display: block;
  font-family: var(--font-handwrite);
  font-size: 1.625rem;
  font-weight: 400;
  color: var(--c-wood-deep);
}

.stat span {
  font-family: var(--font-ui);
  font-size: 0.75rem;
  color: var(--c-text-muted);
}

.about p {
  font-family: var(--font-ui);
  font-size: 0.875rem;
  color: var(--c-text-dim);
  line-height: 1.75;
}

.about .muted {
  font-size: 0.8125rem;
  margin-top: 4px;
}

@media (max-width: 520px) {
  .shortcut-grid { grid-template-columns: repeat(2, 1fr); }
  .stats { flex-wrap: wrap; }
  .stat { flex: 1 1 calc(50% - 6px); min-width: calc(50% - 6px); }
  .add-row { flex-direction: column; }
  .friend-item { flex-direction: column; align-items: stretch; }
  .friend-actions { justify-content: flex-end; }
  .hero-top { flex-direction: column; }
}
</style>
