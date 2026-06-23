import api, { getAuthToken } from './index'

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
    return fetch('/api/chat/send', {
      method: 'POST',
      headers,
      body: JSON.stringify({ message }),
    })
  },
}
