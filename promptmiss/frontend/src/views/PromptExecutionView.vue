<template>
  <div class="min-h-screen flex items-center justify-center px-4 py-20">
    <div class="w-full max-w-2xl bg-zinc-900 p-10 rounded-xl shadow-2xl">
      <h1 class="text-3xl font-bold text-white mb-6">🎯 프롬프트 실행</h1>

      <div class="mb-4">
        <label class="block text-white mb-2">입력값</label>
        <textarea
          v-model="userInput"
          rows="4"
          class="w-full p-3 rounded bg-zinc-800 text-white"
          placeholder="프롬프트에 넣을 입력값을 작성하세요"
        ></textarea>
      </div>

      <button
        @click="executePrompt"
        :disabled="isLoading"
        class="bg-cyan-600 hover:bg-cyan-700 text-white px-4 py-2 rounded disabled:opacity-50"
      >
        <span v-if="isLoading">실행 중...</span>
        <span v-else>⚡ 실행하기</span>
      </button>

      <div v-if="result" class="mt-8">
        <h2 class="text-xl text-white font-bold mb-2">🧠 실행 결과</h2>
        <pre class="bg-zinc-800 text-white p-4 rounded whitespace-pre-wrap">{{ result }}</pre>
      </div>

      <div v-if="executions.length" class="mt-12 pt-6 border-t border-zinc-700">
        <h2 class="text-xl text-white font-bold mb-4">📜 실행 이력</h2>
        <ul class="space-y-4">
          <li v-for="exec in executions" :key="exec.id" class="bg-zinc-800 p-4 rounded text-white">
            <p class="text-sm text-gray-400 mb-1">입력값: {{ exec.user_input }}</p>
            <p>{{ exec.result }}</p>
          </li>
        </ul>
      </div>

      <p v-if="error" class="text-red-500 mt-4">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from '@/api/axios'

const route = useRoute()
const promptId = route.params.id

const userInput = ref('')
const result = ref('')
const error = ref('')
const isLoading = ref(false)
const executions = ref([])

const fetchExecutions = async () => {
  try {
    const res = await axios.get(`prompts/${promptId}/executions/`)
    executions.value = res.data
  } catch (err) {
    console.error('실행 이력 불러오기 실패:', err)
  }
}

const executePrompt = async () => {
  if (!userInput.value.trim()) return

  isLoading.value = true
  result.value = ''
  error.value = ''

  try {
    const res = await axios.post(`prompts/${promptId}/execute/`, {
      user_input: userInput.value,
    })
    result.value = res.data.result
    await fetchExecutions()
  } catch (err) {
    error.value = '실행에 실패했습니다.'
  } finally {
    isLoading.value = false
  }
}

onMounted(async () => {
  await fetchExecutions()
})
</script>
