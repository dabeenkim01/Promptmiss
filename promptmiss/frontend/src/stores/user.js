import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from '@/api/axios'

export const useUserStore = defineStore('user', () => {
  const profile = ref(null)
  const myProfile = ref(null)

  const fetchUserProfile = async (userId) => {
    try {
      const res = await axios.get(`/accounts/${Number(userId)}/`)
      profile.value = res.data
    } catch (err) {
      console.error('프로필 로드 실패', err)
    }
  }

  const fetchMyProfile = async () => {
    try {
      const res = await axios.get(`/accounts/me/`)
      myProfile.value = res.data
    } catch (err) {
      console.error('내 프로필 로드 실패', err)
    }
  }

  return { profile, myProfile, fetchUserProfile, fetchMyProfile }
})