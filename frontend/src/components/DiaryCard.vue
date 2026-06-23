<template>
  <article class="diary-card card clickable" @click="$emit('click')">
    <div class="card-top">
      <time>{{ dateStr }}</time>
      <EmotionBadge
        v-if="diary.emotion_analysis"
        :emotion="diary.emotion_analysis.primary_emotion"
        :sentiment="diary.emotion_analysis.sentiment"
      />
    </div>
    <h3 class="title">{{ diary.title }}</h3>
    <p class="excerpt">{{ excerpt }}</p>
    <div class="card-bottom">
      <span v-if="diary.mood_label" class="mood">{{ diary.mood_label }}</span>
      <button class="del" @click.stop="$emit('delete')">删除</button>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'
import EmotionBadge from './EmotionBadge.vue'

const props = defineProps({ diary: { type: Object, required: true } })
defineEmits(['click', 'delete'])

const excerpt = computed(() => {
  const t = props.diary.content || ''
  return t.length > 100 ? t.slice(0, 100) + '…' : t
})

const dateStr = computed(() => {
  const d = new Date(props.diary.created_at)
  return `${d.getFullYear()}.${String(d.getMonth() + 1).padStart(2, '0')}.${String(d.getDate()).padStart(2, '0')}`
})
</script>

<style scoped>
.diary-card { padding: 20px 22px; margin-bottom: 12px; }

.card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

time {
  font-family: var(--font-ui);
  font-size: 0.75rem;
  color: var(--c-text-muted);
}

.title {
  font-family: var(--font-handwrite);
  font-size: 1.25rem;
  font-weight: 400;
  text-shadow: var(--grass-shadow);
  color: var(--c-wood-deep);
  letter-spacing: 0.06em;
  margin-bottom: 6px;
}

.excerpt {
  font-size: 0.875rem;
  color: var(--c-text-dim);
  line-height: 1.65;
}

.card-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px solid var(--c-border-light);
}

.mood {
  font-family: var(--font-ui);
  font-size: 0.75rem;
  color: var(--c-text-muted);
}

.del {
  background: none;
  border: none;
  font-family: var(--font-ui);
  font-size: 0.75rem;
  color: var(--c-text-muted);
  cursor: pointer;
  opacity: 0;
  transition: opacity var(--transition), color var(--transition);
}

.diary-card:hover .del { opacity: 1; }
.del:hover { color: var(--c-negative); }
</style>
