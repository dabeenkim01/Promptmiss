<template>
  <div class="min-h-screen flex items-start justify-center px-4 py-12">
    <div class="w-full max-w-4xl bg-zinc-900 p-10 rounded-xl shadow-2xl">
      <div v-if="prompt" class="space-y-10">
        <!-- Title -->
        <div>
          <h1 class="text-4xl font-extrabold text-cyan-400 border-b border-zinc-700 pb-4">
            {{ prompt.title }}
          </h1>
        </div>

        <!-- Content -->
        <div>
          <p class="text-lg text-gray-200 whitespace-pre-line leading-loose">
            {{ prompt.content }}
          </p>
        </div>

        <!-- Tags -->
        <div class="pt-4 border-t border-zinc-700">
          <p class="text-base text-gray-400">
            <strong class="text-gray-300">태그:</strong> {{ prompt.tags }}
          </p>
        </div>

        <!-- Stats -->
        <div class="flex justify-end items-center gap-10 pt-6 border-t border-zinc-700 text-pink-300 text-xl">
          <span>❤️ {{ prompt.like_count }}</span>
          <span>🔖 {{ prompt.bookmark_count }}</span>
        </div>

        <!-- Edit Button -->
        <div class="mt-6 flex justify-end gap-2" v-if="isOwner">
          <RouterLink
            :to="`/prompts/${prompt.id}/edit`"
            class="bg-emerald-600 hover:bg-emerald-700 text-white font-semibold py-2 px-4 rounded"
          >
            ✏️ 수정하기
          </RouterLink>
          <button
            @click="deletePrompt"
            class="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded"
          >
            🗑️ 삭제하기
          </button>
        </div>
      </div>

      <p v-else class="text-gray-400 text-center">로딩 중...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import axios from '@/api/axios'
import { useAuthStore } from '@/stores/auth'

const prompt = ref(null)
const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

// Check if the logged-in user is the owner of the prompt
const isOwner = computed(() => {
  if (!prompt.value || localStorage.getItem('userId') === null) return false
  const promptUser = typeof prompt.value.user === 'object' ? prompt.value.user.id : prompt.value.user
  return Number(promptUser) === Number(localStorage.getItem('userId'))
})

onMounted(async () => {
  try {
    const res = await axios.get(`prompts/${route.params.id}/`)
    prompt.value = res.data
  } catch (err) {
    console.error('프롬프트 상세 조회 실패:', err)
  }
})

const deletePrompt = async () => {
  if (!confirm('정말 삭제하시겠습니까?')) return
  try {
    await axios.delete(`prompts/${route.params.id}/`)
    router.push('/prompts')
  } catch (error) {
    console.error('삭제 실패:', error)
    alert('삭제에 실패했습니다.')
  }
}
</script>