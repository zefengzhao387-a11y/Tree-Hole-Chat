import { defineStore } from 'pinia'
import { ref } from 'vue'
import { diaryAPI } from '../api/diary'

export const useDiaryStore = defineStore('diary', () => {
  const diaries = ref([])
  const total = ref(0)
  const loading = ref(false)

  async function fetchDiaries(params = {}) {
    loading.value = true
    try {
      const res = await diaryAPI.list(params)
      diaries.value = res.data.items
      total.value = res.data.total
    } catch (e) {
      console.error('获取日记列表失败:', e)
    } finally {
      loading.value = false
    }
  }

  async function deleteDiary(id) {
    await diaryAPI.delete(id)
    diaries.value = diaries.value.filter(d => d.id !== id)
    total.value--
  }

  return {
    diaries,
    total,
    loading,
    fetchDiaries,
    deleteDiary,
  }
})
