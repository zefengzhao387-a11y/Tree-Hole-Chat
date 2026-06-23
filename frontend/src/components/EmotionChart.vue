<template>
  <div class="chart-wrap">
    <div v-if="!points.length" class="chart-empty">
      <p>写几篇日记后，这里会显示你的心情轨迹</p>
    </div>
    <v-chart v-else :option="opt" style="height:320px" autoresize />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { LineChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, GridComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

use([LineChart, TitleComponent, TooltipComponent, GridComponent, CanvasRenderer])

const props = defineProps({ points: { type: Array, default: () => [] } })

const opt = computed(() => {
  const dates = props.points.map(p => (p.date || '').split(' ')[0])
  const vals = props.points.map(p => p.intensity || 0)
  const emos = props.points.map(p => p.primary_emotion || '')

  return {
    tooltip: {
      trigger: 'axis',
      backgroundColor: '#fffcf8',
      borderColor: '#e8e0d6',
      textStyle: { color: '#3a342e', fontSize: 12, fontFamily: 'Noto Serif SC' },
      formatter: (p) => {
        const i = p[0].dataIndex
        return `<b>${dates[i]}</b><br/>强度 ${vals[i]} · ${emos[i]}`
      },
    },
    grid: { left: 8, right: 16, top: 16, bottom: 28 },
    xAxis: {
      type: 'category',
      data: dates,
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { fontSize: 10, color: '#a89f94', rotate: 30 },
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 10,
      interval: 2,
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { fontSize: 10, color: '#a89f94' },
      splitLine: { lineStyle: { color: '#efeae3', type: 'dashed' } },
    },
    series: [{
      type: 'line',
      data: vals,
      smooth: true,
      symbol: 'circle',
      symbolSize: 5,
      lineStyle: { width: 2, color: '#5a7a62' },
      itemStyle: { color: '#5a7a62', borderColor: '#fff', borderWidth: 2 },
      areaStyle: {
        color: {
          type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(90, 122, 98, 0.15)' },
            { offset: 1, color: 'rgba(90, 122, 98, 0)' },
          ],
        },
      },
    }],
  }
})
</script>

<style scoped>
.chart-wrap { width: 100%; }

.chart-empty {
  text-align: center;
  padding: 48px 20px;
  color: var(--c-text-muted);
  font-size: 0.875rem;
}
</style>
