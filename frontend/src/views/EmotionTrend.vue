<template>
  <div class="page">
    <header class="page-header stack">
      <div style="width:100%;display:flex;justify-content:space-between;align-items:flex-end;flex-wrap:wrap;gap:12px">
        <div>
          <h1 class="page-title">心情轨迹</h1>
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
      <div v-if="loading" class="chart-loading">加载中…</div>
      <EmotionChart v-else :points="points" />
    </div>

    <div v-if="!loading && report" class="card pad report">
      <div class="report-head">
        <h2 class="section-label" style="margin:0">心情报告</h2>
        <time>{{ report.start_date }} ~ {{ report.end_date }}</time>
      </div>

      <div class="stats">
        <div class="stat"><b>{{ report.total_diaries }}</b><span>篇日记</span></div>
        <div class="stat pos"><b>{{ report.sentiment_distribution?.positive || 0 }}</b><span>积极</span></div>
        <div class="stat neu"><b>{{ report.sentiment_distribution?.neutral || 0 }}</b><span>平静</span></div>
        <div class="stat neg"><b>{{ report.sentiment_distribution?.negative || 0 }}</b><span>低落</span></div>
        <div class="stat"><b>{{ report.average_intensity }}</b><span>平均强度</span></div>
      </div>

      <p v-if="report.trend_summary" class="summary">{{ report.trend_summary }}</p>

      <div v-if="report.suggestions?.length" class="tips">
        <p class="tips-title">小树的建议</p>
        <ul>
          <li v-for="(s, i) in report.suggestions" :key="i">{{ s }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { analysisAPI } from '../api/analysis'
import EmotionChart from '../components/EmotionChart.vue'

const points = ref([])
const report = ref(null)
const loading = ref(true)

function defaultRange() {
  const e = new Date()
  const s = new Date()
  s.setDate(s.getDate() - 30)
  return [s.toISOString().split('T')[0], e.toISOString().split('T')[0]]
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
  padding: 14px 8px;
  background: var(--c-bg);
  border-radius: var(--radius-sm);
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
