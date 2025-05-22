import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from '@/api/axios'

export const useUserStore = defineStore('user', () => {
  const profile = ref(null)

  const fetchUserProfile = async (userId) => {
    try {
      const res = await axios.get(`/accounts/${userId}/`)
      profile.value = res.data
    } catch (err) {
      console.error('프로필 로드 실패', err)
    }
  }

  return { profile, fetchUserProfile }
})