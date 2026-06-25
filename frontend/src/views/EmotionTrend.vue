<template>
  <div class="page">
    <header class="page-header stack">
      <div style="width:100%;display:flex;justify-content:space-between;align-items:flex-end;flex-wrap:wrap;gap:12px">
        <div>
          <BlurText tag="h1" class="page-title" text="心情轨迹" animate-by="chars" :delay="80" />
          <p class="page-desc">看见情绪的流动</p>
        </div>
        <el-date-picker
          v-model="range"
          type="daterange"
          range-separator="~"
          start-placeholder="开始"
          end-placeholder="结束"
          value-format="YYYY-MM-DD"
          size="default"
          @change="load"
        />
      </div>
    </header>

    <div class="card pad chart-wrap">
      <div v-if="loading" class="chart-loading">
        <span class="loading-dot" /><span class="loading-dot" /><span class="loading-dot" />
        <p>正在绘制心情轨迹…</p>
      </div>
      <EmotionChart v-else :points="points" />
    </div>

    <FadeContent v-if="!loading && report" direction="up" :blur="true">
    <div class="card pad report">
      <div class="report-head">
        <h2 class="section-label" style="margin:0">心情报告</h2>
        <time>{{ report.start_date }} ~ {{ report.end_date }}</time>
      </div>

      <div class="stats">
        <div class="stat"><b><CountUp :value="report.total_diaries" /></b><span>篇日记</span></div>
        <div class="stat pos"><b><CountUp :value="report.sentiment_distribution?.positive || 0" /></b><span>积极</span></div>
        <div class="stat neu"><b><CountUp :value="report.sentiment_distribution?.neutral || 0" /></b><span>平静</span></div>
        <div class="stat neg"><b><CountUp :value="report.sentiment_distribution?.negative || 0" /></b><span>低落</span></div>
        <div class="stat"><b><CountUp :value="report.average_intensity" :decimals="1" /></b><span>平均强度</span></div>
      </div>

      <p v-if="report.trend_summary" class="summary">{{ report.trend_summary }}</p>

      <div v-if="report.suggestions?.length" class="tips">
        <p class="tips-title">小树的建议</p>
        <ul>
          <li v-for="(s, i) in report.suggestions" :key="i">{{ s }}</li>
        </ul>
      </div>
    </div>
    </FadeContent>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { analysisAPI } from '../api/analysis'
import EmotionChart from '../components/EmotionChart.vue'
import BlurText from '../components/animate/BlurText.vue'
import FadeContent from '../components/animate/FadeContent.vue'
import CountUp from '../components/animate/CountUp.vue'

const points = ref([])
const report = ref(null)
const loading = ref(true)

function formatLocalDate(date) {
  const y = date.getFullYear()
  const m = String(date.getMonth() + 1).padStart(2, '0')
  const d = String(date.getDate()).padStart(2, '0')
  return `${y}-${m}-${d}`
}

function defaultRange() {
  const e = new Date()
  const s = new Date()
  s.setDate(s.getDate() - 30)
  return [formatLocalDate(s), formatLocalDate(e)]
}

const range = ref(defaultRange())

async function load() {
  if (!range.value || range.value.length !== 2) return
  const [s, e] = range.value
  loading.value = true
  try {
    const [t, r] = await Promise.all([
      analysisAPI.getTrend({ start_date: s, end_date: e }),
      analysisAPI.getReport({ start_date: s, end_date: e }),
    ])
    points.value = t.data.points || []
    report.value = r.data
  } catch {
    points.value = []
    report.value = null
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.chart-wrap { margin-bottom: 16px; }

.chart-loading {
  text-align: center;
  padding: 48px 20px;
  font-family: var(--font-ui);
  font-size: 0.875rem;
  color: var(--c-text-dim);
}

.loading-dot {
  display: inline-block;
  width: 7px;
  height: 7px;
  margin: 0 3px 12px;
  border-radius: 50%;
  background: var(--c-primary);
  animation: dot-bounce 1.2s ease-in-out infinite;
}

.loading-dot:nth-child(2) { animation-delay: 0.15s; }
.loading-dot:nth-child(3) { animation-delay: 0.3s; }

@keyframes dot-bounce {
  0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
  40% { transform: scale(1); opacity: 1; }
}

.report-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.report-head time {
  font-family: var(--font-ui);
  font-size: 0.75rem;
  color: var(--c-text-muted);
}

.stats {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 10px;
  margin-bottom: 20px;
}

.stat {
  text-align: center;
  padding: 16px 10px;
  background: rgba(255, 252, 248, 0.65);
  border-radius: var(--radius-sm);
  border: 1px solid rgba(228, 220, 208, 0.6);
  transition: transform var(--transition), box-shadow var(--transition);
}

.stat:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(58, 52, 46, 0.06);
}

.stat b {
  display: block;
  font-family: var(--font-handwrite);
  font-size: 1.5rem;
  font-weight: 400;
  color: var(--c-wood-deep);
}

.stat span {
  font-family: var(--font-ui);
  font-size: 0.6875rem;
  color: var(--c-text-muted);
}

.stat.pos b { color: var(--c-positive); }
.stat.neg b { color: var(--c-negative); }
.stat.neu b { color: var(--c-neutral); }

.summary {
  font-size: 0.9375rem;
  color: var(--c-text-dim);
  line-height: 1.75;
  padding: 16px;
  background: var(--c-bg);
  border-radius: var(--radius-sm);
  margin-bottom: 16px;
}

.tips {
  padding: 16px;
  background: rgba(238, 244, 239, 0.65);
  border-radius: var(--radius-sm);
  border-left: 3px solid var(--c-primary);
}

.tips-title {
  font-family: var(--font-ui);
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--c-primary);
  margin-bottom: 8px;
}

.tips ul {
  padding-left: 18px;
  font-family: var(--font-ui);
  font-size: 0.875rem;
  color: var(--c-text-dim);
  line-height: 1.85;
}

@media (max-width: 520px) {
  .stats { grid-template-columns: repeat(3, 1fr); }
  .stats .stat:nth-child(4),
  .stats .stat:nth-child(5) { grid-column: span 1; }
}
</style>
