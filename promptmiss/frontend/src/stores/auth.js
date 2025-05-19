import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref(localStorage.getItem('access'))
  const refreshToken = ref(localStorage.getItem('refresh'))
  const router = useRouter()

  const isLoggedIn = computed(() => !!accessToken.value)
  const userId = computed(() => localStorage.getItem('userId'))
  const username = computed(() => localStorage.getItem('username'))

  const login = (access, refresh, user) => {
    accessToken.value = access
    refreshToken.value = refresh
    localStorage.setItem('access', access)
    localStorage.setItem('refresh', refresh)
    localStorage.setItem('userId', user.id)
    localStorage.setItem('username', user.username)
  }

  const logout = () => {
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
    localStorage.removeItem('userId')
    localStorage.removeItem('username')
    router.push('/login')
  }

  return { accessToken, refreshToken, isLoggedIn, userId, username, login, logout }
}, {
  persist: true
})
