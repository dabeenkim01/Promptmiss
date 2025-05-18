<template>
  <div class="w-full px-4 sm:px-8 flex flex-col items-center gap-6">
    <h1 class="text-2xl font-semibold text-white">🔐 로그인</h1>
    <form @submit.prevent="login" class="bg-zinc-900 p-12 rounded-xl shadow-lg w-full max-w-xl flex flex-col gap-6 text-lg">
      <div>
        <label class="block text-sm text-gray-300 mb-1">아이디</label>
        <input v-model="username" placeholder="아이디" required
          class="w-full p-3 rounded-md bg-zinc-800 text-white border border-zinc-700 focus:outline-none focus:ring focus:border-teal-400" />
      </div>
      <div>
        <label class="block text-sm text-gray-300 mb-1">비밀번호</label>
        <input v-model="password" placeholder="비밀번호" type="password" required
          class="w-full p-3 rounded-md bg-zinc-800 text-white border border-zinc-700 focus:outline-none focus:ring focus:border-teal-400" />
      </div>
      <button type="submit"
        class="mt-2 bg-teal-500 hover:bg-teal-600 text-white font-semibold py-2 px-4 rounded transition">
        로그인
      </button>
    </form>
    <p v-if="error" class="text-red-400">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from '@/api/axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()
const auth = useAuthStore()

const login = async () => {
  try {
    // 로그인 요청
    const res = await axios.post('token/', {
      username: username.value,
      password: password.value,
    })

    // 사용자 정보 조회
    const me = await axios.get('/accounts/me/', {
      headers: {
        Authorization: `Bearer ${res.data.access}`,
      },
    })

    // 로그인 성공 시 토큰 저장 및 사용자 정보 설정
    auth.login(res.data.access, res.data.refresh, { id: me.data.id })

    // 사용자 정보 저장
    localStorage.setItem('userId', me.data.id)
    localStorage.setItem('username', me.data.username)

    // 에러 초기화 및 페이지 이동
    error.value = ''
    router.push('/prompts')
  } catch (err) {
    console.error('로그인 실패:', err.response?.data || err.message)
    error.value = err.response?.data?.detail || '아이디 또는 비밀번호가 올바르지 않습니다.'
  }
}
</script>