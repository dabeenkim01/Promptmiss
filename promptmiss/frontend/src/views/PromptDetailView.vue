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
            <strong class="text-gray-300">태그: </strong>
            <span v-for="(tag, index) in prompt.tags" :key="index" class="mr-2">#{{ tag }}</span>
          </p>
        </div>

        <!-- Actions -->
        <div class="flex justify-between items-center gap-4 pt-6 border-t border-zinc-700 text-l">
          <div class="flex items-center gap-8 text-gray-400">
            <span @click="togglePromptLike" class="cursor-pointer">
              {{ prompt.is_liked ? '❤️' : '🤍' }} {{ prompt.like_count }}
            </span>
            <span @click="togglePromptBookmark" class="cursor-pointer">
              {{ prompt.is_bookmarked ? '📌' : '📎' }} {{ prompt.bookmark_count }}
            </span>
          </div>

          <div class="flex gap-2" v-if="isOwner">
            <RouterLink
              :to="`/prompts/${prompt.id}/update`"
              class="bg-emerald-600 hover:bg-emerald-700 text-white font-semibold py-2 px-4 rounded"
            >
              ✏️ 수정하기
            </RouterLink>
            <button
              @click="deletePrompt"
              :disabled="isDeleting"
              class="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded disabled:opacity-60"
            >
              <span v-if="isDeleting">⏳ 삭제 중...</span>
              <span v-else>🗑️ 삭제하기</span>
            </button>
          </div>
        </div>
      </div>
      <br>
      <CommentSection
        class="mt-12"
        :prompt-id="prompt.id"
        :comments="prompt.comments"
        @refresh="fetchPromptDetail"
        v-if="prompt"
      />
    </div>
  </div>
</template>

<script setup>
import CommentSection from '@/components/CommentSection.vue'
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import axios from '@/api/axios'
import { useAuthStore } from '@/stores/auth'

const prompt = ref(null)
const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

// Deleting state
const isDeleting = ref(false)

// Check if the logged-in user is the owner of the prompt
const isOwner = computed(() => {
  if (!prompt.value || localStorage.getItem('userId') === null) return false
  const promptUser = typeof prompt.value.user === 'object' ? prompt.value.user.id : prompt.value.user
  return Number(promptUser) === Number(localStorage.getItem('userId'))
})

// Toggle like on prompt
const togglePromptLike = async () => {
  try {
    const res = await axios.post(`/prompts/${prompt.value.id}/like/`)
    prompt.value.like_count = res.data.like_count
    prompt.value.is_liked = res.data.is_liked
  } catch (err) {
    console.error('프롬프트 좋아요 실패:', err)
  }
}

// Toggle bookmark on prompt
const togglePromptBookmark = async () => {
  try {
    const res = await axios.post(`/prompts/${prompt.value.id}/bookmark/`)
    prompt.value.bookmark_count = res.data.bookmark_count
    prompt.value.is_bookmarked = res.data.is_bookmarked
  } catch (err) {
    console.error('프롬프트 북마크 실패:', err)
  }
}

const fetchPromptDetail = async () => {
  try {
    const res = await axios.get(`prompts/${route.params.id}/`)
    prompt.value = res.data
  } catch (err) {
    console.error('프롬프트 상세 조회 실패:', err)
  }
}

onMounted(fetchPromptDetail)

const deletePrompt = async () => {
  if (!confirm('정말 삭제하시겠습니까?')) return
  isDeleting.value = true
  try {
    await axios.delete(`prompts/${route.params.id}/`)
    router.push('/prompts')
  } catch (error) {
    console.error('삭제 실패:', error)
    alert('삭제에 실패했습니다.')
  } finally {
    isDeleting.value = false
  }
}
</script>