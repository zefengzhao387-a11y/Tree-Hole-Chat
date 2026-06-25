<template>
  <div class="page">
    <header class="page-header">
      <div>
        <BlurText tag="h1" class="page-title" :text="greeting" animate-by="words" :delay="60" />
        <p class="page-desc">{{ store.total ? `共 ${store.total} 篇日记` : '写下第一篇，开始记录' }}</p>
      </div>
      <button class="btn btn-primary" @click="$router.push('/diary/new')">写日记</button>
    </header>

    <div class="filters">
      <button
        v-for="m in moodFilters"
        :key="m.v"
        class="filter-btn"
        :class="{ active: filter === m.v }"
        @click="filter = filter === m.v ? '' : m.v"
      >{{ m.l }}</button>
    </div>

    <div v-if="store.loading" class="state-loading">
      <SkeletonList :count="3" />
    </div>

    <FadeContent v-else-if="!store.diaries.length" direction="up" :blur="true">
      <div class="state card pad empty-state">
        <div class="empty-icon" aria-hidden="true">📝</div>
        <p class="state-title">还没有日记</p>
        <p class="state-desc">把今天的故事写下来，小树会记住你的心情</p>
        <button class="btn btn-primary" @click="$router.push('/diary/new')">开始写第一篇</button>
      </div>
    </FadeContent>

    <div v-else>
      <FadeContent
        v-for="(d, i) in store.diaries"
        :key="d.id"
        :delay="i * 80"
        direction="up"
      >
        <DiaryCard
          :diary="d"
          @click="$router.push(`/diary/${d.id}/edit`)"
          @delete="remove(d.id)"
        />
      </FadeContent>
    </div>

    <div v-if="store.total > 20" class="pager">
      <el-pagination
        v-model:current-page="page"
        :page-size="20"
        :total="store.total"
        layout="prev, pager, next"
        @current-change="load"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useDiaryStore } from '../stores/diary'
import { ElMessageBox, ElMessage } from 'element-plus'
import DiaryCard from '../components/DiaryCard.vue'
import BlurText from '../components/animate/BlurText.vue'
import FadeContent from '../components/animate/FadeContent.vue'
import SkeletonList from '../components/ui/SkeletonList.vue'

const store = useDiaryStore()
const page = ref(1)
const filter = ref('')

const moodFilters = [
  { v: '', l: '全部' },
  { v: '开心', l: '开心' },
  { v: '难过', l: '难过' },
  { v: '焦虑', l: '焦虑' },
  { v: '平静', l: '平静' },
  { v: '生气', l: '生气' },
]

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return '早安，今天好吗'
  if (h < 18) return '我的日记'
  return '今日心事'
})

async function load() {
  const p = { page: page.value, page_size: 20 }
  if (filter.value) p.mood_label = filter.value
  await store.fetchDiaries(p)
}

async function remove(id) {
  try {
    await ElMessageBox.confirm('确定删除这篇日记吗？', '确认', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await store.deleteDiary(id)
    ElMessage.success('已删除')
  } catch { /* cancelled */ }
}

watch(filter, () => { page.value = 1; load() })
onMounted(load)
</script>

<style scoped>
.filters {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

.filter-btn {
  padding: 7px 16px;
  border: 1px solid rgba(228, 220, 208, 0.8);
  border-radius: 100px;
  background: var(--glass-bg);
  backdrop-filter: blur(8px);
  font-family: var(--font-ui);
  font-size: 0.8125rem;
  color: var(--c-text-dim);
  cursor: pointer;
  transition: all var(--transition);
}

.filter-btn:hover {
  border-color: rgba(184, 137, 94, 0.35);
  color: var(--c-text);
  transform: translateY(-1px);
}

.filter-btn.active {
  background: rgba(255, 252, 248, 0.95);
  border-color: var(--c-primary);
  color: var(--c-wood-deep);
  font-weight: 500;
  box-shadow: 0 2px 10px rgba(90, 122, 98, 0.12);
}

.empty-state {
  text-align: center;
  padding: 56px 28px;
}

.empty-icon {
  font-size: 2.5rem;
  margin-bottom: 12px;
  filter: grayscale(0.2);
}

.state-title {
  font-family: var(--font-handwrite);
  font-size: 1.375rem;
  font-weight: 400;
  color: var(--c-wood-deep);
  letter-spacing: 0.08em;
  margin-bottom: 8px;
}

.state-loading { margin-bottom: 8px; }

.state-desc {
  font-size: 0.875rem;
  color: var(--c-text-dim);
  margin-bottom: 20px;
  line-height: 1.6;
}

.pager { display: flex; justify-content: center; margin-top: 28px; }
</style>
