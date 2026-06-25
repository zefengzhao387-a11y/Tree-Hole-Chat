import api from './index'

export const friendsAPI = {
  search(q) {
    return api.get('/friends/search', { params: { q } })
  },

  list() {
    return api.get('/friends')
  },

  sendRequest(username) {
    return api.post('/friends/request', { username })
  },

  accept(friendshipId) {
    return api.post(`/friends/${friendshipId}/accept`)
  },

  reject(friendshipId) {
    return api.post(`/friends/${friendshipId}/reject`)
  },

  remove(friendshipId) {
    return api.delete(`/friends/${friendshipId}`)
  },

  getMessages(friendId, afterId = 0) {
    return api.get(`/friends/${friendId}/messages`, { params: { after_id: afterId } })
  },

  sendMessage(friendId, content) {
    return api.post(`/friends/${friendId}/messages`, { content })
  },

  getUnreadSummary() {
    return api.get('/friends/unread/summary')
  },
}
