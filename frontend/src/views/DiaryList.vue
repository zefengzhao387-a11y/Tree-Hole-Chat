<template>
  <div class="page">
    <header class="page-header">
      <div>
        <h1 class="page-title">{{ greeting }}</h1>
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

    <div v-if="store.loading" class="state">加载中…</div>

    <div v-else-if="!store.diaries.length" class="state card pad">
      <p class="state-title">还没有日记</p>
      <p class="state-desc">把今天的故事写下来吧</p>
      <button class="btn btn-primary" style="margin-top:16px" @click="$router.push('/diary/new')">开始写</button>
    </div>

    <div v-else>
      <DiaryCard
        v-for="d in store.diaries"
        :key="d.id"
        :diary="d"
        @click="$router.push(`/diary/${d.id}/edit`)"
        @delete="remove(d.id)"
      />
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
  padding: 6px 14px;
  border: 1px solid var(--c-border);
  border-radius: 100px;
  background: var(--c-surface);
  font-family: var(--font-ui);
  font-size: 0.8125rem;
  color: var(--c-text-dim);
  cursor: pointer;
  transition: all var(--transition);
}

.filter-btn:hover { border-color: #ddd5cb; color: var(--c-text); }

.filter-btn.active {
  background: rgba(255, 252, 248, 0.95);
  border-color: var(--c-wood);
  color: var(--c-wood-deep);
  font-weight: 500;
}

.state-title {
  font-family: var(--font-handwrite);
  font-size: 1.125rem;
  font-weight: 400;
  color: var(--c-wood-deep);
  letter-spacing: 0.08em;
  margin-bottom: 4px;
}

.state {
  text-align: center;
  padding: 48px 24px;
  color: var(--c-text-dim);
}

.state-desc { font-size: 0.875rem; }

.pager { display: flex; justify-content: center; margin-top: 24px; }
</style>
