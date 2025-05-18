import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref(localStorage.getItem('access'))
  const refreshToken = ref(localStorage.getItem('refresh'))
  const router = useRouter()

  const isLoggedIn = computed(() => !!accessToken.value)
  const userId = computed(() => localStorage.getItem('userId'))

  const login = (access, refresh, user) => {
    accessToken.value = access
    refreshToken.value = refresh
    localStorage.setItem('access', access)
    localStorage.setItem('refresh', refresh)
    localStorage.setItem('userId', user.id)
  }

  const logout = () => {
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
    router.push('/login')
  }

  return { accessToken, refreshToken, isLoggedIn, userId, login, logout }
}, {
  persist: true
})
