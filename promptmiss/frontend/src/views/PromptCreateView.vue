<template>
  <div class="w-full px-4 sm:px-8 flex flex-col items-center gap-6">
    <h1 class="text-2xl font-semibold text-white">✏️ 프롬프트 생성</h1>
    <form @submit.prevent="createPrompt" class="bg-zinc-900 p-12 rounded-xl shadow-lg w-full max-w-[90rem] flex flex-col gap-8 text-xl">
      <div>
        <label class="block text-sm text-gray-300 mb-1">제목</label>
        <input v-model="title" placeholder="제목" required
          class="w-full p-3 rounded-md bg-zinc-800 text-white border border-zinc-700 focus:outline-none focus:ring focus:border-teal-400" />
      </div>
      <div>
        <label class="block text-sm text-gray-300 mb-1">내용</label>
        <textarea v-model="content" placeholder="내용" required rows="6"
          class="w-full p-3 rounded-md bg-zinc-800 text-white border border-zinc-700 focus:outline-none focus:ring focus:border-teal-400" />
      </div>
      <div>
        <label class="block text-sm text-gray-300 mb-1">태그 (쉼표로 구분)</label>
        <input v-model="tags" placeholder="예: 개발, GPT, 디자인"
          class="w-full p-3 rounded-md bg-zinc-800 text-white border border-zinc-700 focus:outline-none focus:ring focus:border-teal-400" />
      </div>
      <button type="submit"
        class="mt-2 bg-teal-500 hover:bg-teal-600 text-white font-semibold py-2 px-4 rounded transition">
        생성하기
      </button>
    </form>
    <p v-if="error" style="color: red">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from '@/api/axios'
import { useRouter } from 'vue-router'

const title = ref('')
const content = ref('')
const tags = ref('')
const error = ref('')
const router = useRouter()

const createPrompt = async () => {
  try {
    await axios.post('prompts/', {
      title: title.value,
      content: content.value,
      tags: tags.value,
    })
    router.push('/prompts')
  } catch (err) {
    error.value = '프롬프트 생성에 실패했습니다.'
  }
}
</script>