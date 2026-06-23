import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI } from '../api/auth'

const TOKEN_KEY = 'access_token'
const USER_KEY = 'user_info'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem(TOKEN_KEY) || '')
  const user = ref(JSON.parse(localStorage.getItem(USER_KEY) || 'null'))

  const isLoggedIn = computed(() => !!token.value)

  function setSession(accessToken, userInfo) {
    token.value = accessToken
    user.value = userInfo
    localStorage.setItem(TOKEN_KEY, accessToken)
    localStorage.setItem(USER_KEY, JSON.stringify(userInfo))
  }

  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
  }

  async function register(payload) {
    const { data } = await authAPI.register(payload)
    setSession(data.access_token, data.user)
    return data
  }

  async function login(payload) {
    const { data } = await authAPI.login(payload)
    setSession(data.access_token, data.user)
    return data
  }

  async function fetchMe() {
    if (!token.value) return null
    try {
      const { data } = await authAPI.me()
      user.value = data
      localStorage.setItem(USER_KEY, JSON.stringify(data))
      return data
    } catch {
      logout()
      return null
    }
  }

  return { token, user, isLoggedIn, setSession, logout, register, login, fetchMe }
})
