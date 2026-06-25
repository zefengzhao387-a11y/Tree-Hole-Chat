<template>
  <GlareHover border-radius="var(--radius-lg)" :glare-opacity="0.32">
    <article
      class="diary-card card clickable"
      :class="accentClass"
      @click="$emit('click')"
    >
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
        <span v-if="diary.mood_label" class="mood">
          <span class="mood-dot" aria-hidden="true" />
          {{ diary.mood_label }}
        </span>
        <button class="del" @click.stop="$emit('delete')">删除</button>
      </div>
    </article>
  </GlareHover>
</template>

<script setup>
import { computed } from 'vue'
import EmotionBadge from './EmotionBadge.vue'
import GlareHover from './animate/GlareHover.vue'

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

const accentClass = computed(() => {
  const s = props.diary.emotion_analysis?.sentiment
  if (s === 'positive') return 'accent-positive'
  if (s === 'negative') return 'accent-negative'
  return 'accent-neutral'
})
</script>

<style scoped>
.diary-card {
  padding: 20px 22px 20px 26px;
  margin-bottom: 12px;
  border-left: 3px solid transparent;
}

.diary-card.accent-positive { border-left-color: rgba(90, 122, 98, 0.55); }
.diary-card.accent-negative { border-left-color: rgba(176, 112, 112, 0.55); }
.diary-card.accent-neutral  { border-left-color: rgba(138, 154, 170, 0.45); }

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
  padding: 2px 8px;
  border-radius: 100px;
  background: rgba(255, 252, 248, 0.6);
}

.title {
  font-family: var(--font-handwrite);
  font-size: 1.3125rem;
  font-weight: 400;
  text-shadow: var(--grass-shadow);
  color: var(--c-wood-deep);
  letter-spacing: 0.06em;
  margin-bottom: 8px;
  transition: color var(--transition);
}

.diary-card:hover .title {
  color: var(--c-primary-hover);
}

.excerpt {
  font-size: 0.875rem;
  color: var(--c-text-dim);
  line-height: 1.7;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px dashed rgba(228, 220, 208, 0.85);
}

.mood {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-family: var(--font-ui);
  font-size: 0.75rem;
  color: var(--c-text-muted);
}

.mood-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--c-warm);
  opacity: 0.7;
}

.del {
  background: none;
  border: none;
  font-family: var(--font-ui);
  font-size: 0.75rem;
  color: var(--c-text-muted);
  cursor: pointer;
  opacity: 0;
  padding: 4px 8px;
  border-radius: 6px;
  transition: opacity var(--transition), color var(--transition), background var(--transition);
}

.diary-card:hover .del { opacity: 1; }
.del:hover {
  color: var(--c-negative);
  background: rgba(176, 112, 112, 0.08);
}
</style>
