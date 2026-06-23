import api from './index'

export const analysisAPI = {
  /** 对指定日记执行情感分析 */
  analyze(diaryId) {
    return api.post(`/analysis/${diaryId}`)
  },

  /** 获取情感趋势 */
  getTrend(params = {}) {
    return api.get('/analysis/trend', { params })
  },

  /** 获取情感报告 */
  getReport(params = {}) {
    return api.get('/analysis/report', { params })
  },
}
