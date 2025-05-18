<template>
  <div class="w-full px-4 sm:px-8 flex flex-col items-center gap-6">
    <h1 class="text-2xl font-semibold text-white">📝 회원가입</h1>
    <form @submit.prevent="signup" class="bg-zinc-900 p-12 rounded-xl shadow-lg w-full max-w-xl flex flex-col gap-6 text-lg">
      <div>
        <label class="block text-sm text-gray-300 mb-1">아이디</label>
        <input v-model="username" placeholder="아이디" required
          class="w-full p-3 rounded-md bg-zinc-800 text-white border border-zinc-700 focus:outline-none focus:ring focus:border-teal-400" />
      </div>
      <div>
        <label class="block text-sm text-gray-300 mb-1">이메일</label>
        <input v-model="email" type="email" placeholder="이메일" required
          class="w-full p-3 rounded-md bg-zinc-800 text-white border border-zinc-700 focus:outline-none focus:ring focus:border-teal-400" />
      </div>
      <div>
        <label class="block text-sm text-gray-300 mb-1">비밀번호</label>
        <input v-model="password" type="password" placeholder="비밀번호" required
          class="w-full p-3 rounded-md bg-zinc-800 text-white border border-zinc-700 focus:outline-none focus:ring focus:border-teal-400" />
      </div>
      <button type="submit"
        class="mt-2 bg-teal-500 hover:bg-teal-600 text-white font-semibold py-2 px-4 rounded transition">
        회원가입
      </button>
    </form>
    <p v-if="success" class="text-green-400">회원가입이 완료되었습니다! 로그인해주세요.</p>
    <p v-if="error" class="text-red-400">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from '@/api/axios'
import { useRouter } from 'vue-router'

const username = ref('')
const email = ref('')
const password = ref('')
const error = ref('')
const success = ref(false)
const router = useRouter()

const signup = async () => {
  try {
    await axios.post('accounts/signup/', {
      username: username.value,
      password: password.value,
      email: email.value,
    })
    success.value = true
    error.value = ''
    setTimeout(() => {
      router.push('/login')
    }, 1000)
  } catch (err) {
    error.value = '회원가입에 실패했습니다.'
    success.value = false
  }
}
</script>