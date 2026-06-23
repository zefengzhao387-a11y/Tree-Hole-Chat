<template>
  <div class="page">
    <header class="page-header">
      <button class="btn btn-ghost" @click="$router.back()">返回</button>
      <h1 class="page-title" style="flex:1;text-align:center">{{ isEdit ? '编辑日记' : '新日记' }}</h1>
      <span style="width:52px"></span>
    </header>

    <div class="card pad form">
      <div class="field">
        <label class="label">标题</label>
        <input v-model="form.title" class="input-heal" placeholder="给今天起个名字…" maxlength="200" />
      </div>

      <div class="field">
        <label class="label">此刻心情</label>
        <div class="moods">
          <button
            v-for="m in moods"
            :key="m.v"
            class="mood-btn"
            :class="{ sel: form.mood_label === m.v }"
            @click="form.mood_label = m.v"
          >{{ m.l }}</button>
        </div>
      </div>

      <div class="field">
        <label class="label">内容</label>
        <textarea
          v-model="form.content"
          class="textarea-heal"
          placeholder="此刻，你的感受是什么…"
          rows="14"
          maxlength="5000"
        ></textarea>
        <span class="count">{{ form.content.length }} / 5000</span>
      </div>

      <button class="btn btn-primary btn-block" :disabled="saving" @click="save">
        {{ saving ? '保存中…' : '保存' }}
      </button>
    </div>

    <div v-if="analysis" class="card pad analysis">
      <p class="section-label">AI 情感分析</p>
      <EmotionBadge
        :emotion="analysis.primary_emotion"
        :sentiment="analysis.sentiment"
        :intensity="analysis.intensity"
      />
      <p class="summary">"{{ analysis.summary }}"</p>
      <div class="tip">
        <p>{{ analysis.suggestion }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { diaryAPI } from '../api/diary'
import EmotionBadge from '../components/EmotionBadge.vue'

const route = useRoute()
const router = useRouter()
const saving = ref(false)
const analysis = ref(null)
const isEdit = computed(() => !!route.params.id)
const form = ref({ title: '', content: '', mood_label: '' })

const moods = [
  { v: '开心', l: '开心' },
  { v: '难过', l: '难过' },
  { v: '焦虑', l: '焦虑' },
  { v: '平静', l: '平静' },
  { v: '生气', l: '生气' },
]

onMounted(async () => {
  if (isEdit.value) {
    try {
      const { data } = await diaryAPI.get(route.params.id)
      form.value = { title: data.title, content: data.content, mood_label: data.mood_label || '' }
      if (data.emotion_analysis) analysis.value = data.emotion_analysis
    } catch {
      ElMessage.error('加载失败')
      router.push('/diary')
    }
  }
})

async function save() {
  if (!form.value.title.trim() || !form.value.content.trim()) {
    ElMessage.warning('标题和内容不能为空')
    return
  }
  saving.value = true
  try {
    if (isEdit.value) {
      await diaryAPI.update(route.params.id, form.value)
      ElMessage.success('更新成功')
    } else {
      const { data } = await diaryAPI.create(form.value)
      ElMessage.success('保存成功')
      if (data.emotion_analysis) analysis.value = data.emotion_analysis
      router.replace(`/diary/${data.id}/edit`)
    }
  } catch {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.page-header { align-items: center; }

.form { margin-bottom: 16px; }

.field { margin-bottom: 22px; }

.moods { display: flex; gap: 8px; flex-wrap: wrap; }

.mood-btn {
  padding: 8px 16px;
  border: 1px solid var(--c-border);
  border-radius: var(--radius-sm);
  background: #fff;
  font-family: var(--font-ui);
  font-size: 0.8125rem;
  color: var(--c-text-dim);
  cursor: pointer;
  transition: all var(--transition);
}

.mood-btn:hover { border-color: #ddd5cb; }

.mood-btn.sel {
  background: rgba(255, 252, 248, 0.95);
  border-color: var(--c-wood);
  color: var(--c-wood-deep);
  font-weight: 500;
}

.count {
  display: block;
  text-align: right;
  font-family: var(--font-ui);
  font-size: 0.75rem;
  color: var(--c-text-muted);
  margin-top: 6px;
}

.analysis { margin-top: 16px; }

.summary {
  font-style: italic;
  color: var(--c-text-dim);
  font-size: 0.9375rem;
  line-height: 1.7;
  margin: 12px 0;
}

.tip {
  padding: 14px 16px;
  background: var(--c-warm-soft);
  border-radius: var(--radius-sm);
  border-left: 3px solid var(--c-warm);
}

.tip p {
  font-family: var(--font-ui);
  font-size: 0.875rem;
  color: var(--c-text-dim);
  line-height: 1.6;
}
</style>
