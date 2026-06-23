import api from './index'

export const diaryAPI = {
  /** 获取日记列表 */
  list(params = {}) {
    return api.get('/diary', { params })
  },

  /** 获取单篇日记 */
  get(id) {
    return api.get(`/diary/${id}`)
  },

  /** 创建日记 */
  create(data) {
    return api.post('/diary', data)
  },

  /** 更新日记 */
  update(id, data) {
    return api.put(`/diary/${id}`, data)
  },

  /** 删除日记 */
  delete(id) {
    return api.delete(`/diary/${id}`)
  },
}
