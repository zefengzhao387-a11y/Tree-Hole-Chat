import { defineStore } from 'pinia'
import { ref } from 'vue'
import { ElNotification } from 'element-plus'
import { friendsAPI } from '../api/friends'
import router from '../router'

export const useFriendNotifyStore = defineStore('friendNotify', () => {
  const unreadTotal = ref(0)
  const unreadByFriend = ref({})

  let pollTimer = null
  let initialized = false
  const seenMessageIds = new Set()

  function preview(text, max = 48) {
    if (!text) return ''
    return text.length > max ? `${text.slice(0, max)}…` : text
  }

  function displayName(friend) {
    return friend?.nickname || friend?.username || '好友'
  }

  function notifyIncoming(item) {
    const name = displayName(item.friend)
    ElNotification({
      title: `${name} 发来消息`,
      message: preview(item.last_content),
      type: 'info',
      duration: 5000,
      position: 'top-right',
      onClick: () => {
        router.push({
          name: 'FriendChat',
          params: { friendId: item.friend_id },
          query: { name },
        })
      },
    })
  }

  async function poll(getRoute) {
    try {
      const { data } = await friendsAPI.getUnreadSummary()
      unreadTotal.value = data.total || 0

      const map = {}
      for (const item of data.items || []) {
        map[item.friend_id] = item.unread_count
      }
      unreadByFriend.value = map

      if (!initialized) {
        for (const item of data.items || []) {
          seenMessageIds.add(item.last_message_id)
        }
        initialized = true
        return
      }

      const route = getRoute?.() || router.currentRoute.value
      const inFriendChat = route.name === 'FriendChat'
      const activeFriendId = inFriendChat ? Number(route.params.friendId) : null

      for (const item of data.items || []) {
        if (seenMessageIds.has(item.last_message_id)) continue
        seenMessageIds.add(item.last_message_id)

        if (inFriendChat && activeFriendId === item.friend_id) continue
        notifyIncoming(item)
      }
    } catch {
      /* ignore polling errors */
    }
  }

  function startPolling(getRoute) {
    stopPolling()
    poll(getRoute)
    pollTimer = setInterval(() => poll(getRoute), 5000)
  }

  function stopPolling() {
    if (pollTimer) {
      clearInterval(pollTimer)
      pollTimer = null
    }
    initialized = false
    seenMessageIds.clear()
    unreadTotal.value = 0
    unreadByFriend.value = {}
  }

  function markInitialized(messageIds = []) {
    for (const id of messageIds) seenMessageIds.add(id)
    initialized = true
  }

  return {
    unreadTotal,
    unreadByFriend,
    poll,
    startPolling,
    stopPolling,
    markInitialized,
    notifyIncoming,
    preview,
    displayName,
  }
})
