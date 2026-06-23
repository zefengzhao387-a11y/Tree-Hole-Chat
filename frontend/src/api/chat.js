import api, { getAuthToken } from './index'
import { API_BASE } from './base'

export const chatAPI = {
  getHistory() {
    return api.get('/chat/history')
  },
  clearHistory() {
    return api.delete('/chat/history')
  },
  sendMessage(message) {
    const headers = { 'Content-Type': 'application/json' }
    const token = getAuthToken()
    if (token) headers.Authorization = `Bearer ${token}`
    return fetch(`${API_BASE}/chat/send`, {
      method: 'POST',
      headers,
      body: JSON.stringify({ message }),
    })
  },
}
