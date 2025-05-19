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

        <!-- Stats -->
        <div class="flex justify-end items-center gap-10 pt-6 border-t border-zinc-700 text-pink-300 text-xl">
          <span @click="togglePromptLike" class="cursor-pointer">
            {{ prompt.is_liked ? '❤️' : '🤍' }} {{ prompt.like_count }}
          </span>
          <span @click="togglePromptBookmark" class="cursor-pointer">
            {{ prompt.is_bookmarked ? '📌' : '📎' }} {{ prompt.bookmark_count }}
          </span>
        </div>

        <!-- Update Button -->
        <div class="mt-6 flex justify-end gap-2" v-if="isOwner">
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

      <!-- Comments -->
      <div class="mt-12 pt-6 border-t border-zinc-700">
        <h2 class="text-2xl text-white font-bold mb-4">💬 댓글</h2>

        <!-- New comment form -->
        <div v-if="auth.isLoggedIn" class="mb-6">
          <textarea v-model="commentContent" class="w-full p-4 rounded bg-zinc-800 text-white" rows="3" placeholder="댓글을 입력하세요"></textarea>
          <button @click="submitComment" class="mt-2 bg-cyan-600 hover:bg-cyan-700 text-white px-4 py-2 rounded">댓글 작성</button>
        </div>
        <div v-else class="text-gray-400 text-sm">댓글을 작성하려면 로그인하세요.</div>

        <!-- Comments list -->
        <ul class="space-y-4">
          <li v-for="comment in comments" :key="comment.id" class="p-4 bg-zinc-800 rounded text-white">
            <div class="flex justify-between items-start">
              <p class="text-sm text-gray-400">작성자: {{ comment.user.username }}</p>
              <button
                v-if="auth.user?.id === comment.user.id"
                @click="deleteComment(comment.id)"
                class="text-sm text-red-400 hover:underline"
              >
                🗑️ 삭제
              </button>
            </div>
            <p>{{ comment.content }}</p>
            <div class="mt-2 flex items-center gap-4 text-sm text-gray-300">
              <span
                class="cursor-pointer"
                @click="toggleLike(comment)"
                :class="{ 'text-red-500': comment.is_liked, 'text-white': !comment.is_liked }"
              >
                {{ comment.is_liked ? '❤️' : '🤍' }} {{ comment.like_count ?? 0 }}
              </span>
            </div>
          </li>
        </ul>
      </div>
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

// Comments state
const comments = ref([])
const commentContent = ref('')

// Deleting state
const isDeleting = ref(false)

// Fetch comments
const fetchComments = async () => {
  try {
    const res = await axios.get(`prompts/${route.params.id}/comments/`)
    comments.value = res.data
  } catch (err) {
    console.error('댓글 불러오기 실패:', err)
  }
}

// Submit new comment
const submitComment = async () => {
  if (!commentContent.value.trim()) return
  try {
    const res = await axios.post(`prompts/${route.params.id}/comments/`, {
      content: commentContent.value,
    })
    comments.value.push(res.data)
    commentContent.value = ''
  } catch (err) {
    console.error('댓글 작성 실패:', err)
  }
}

// Delete comment
const deleteComment = async (commentId) => {
  if (!confirm('댓글을 삭제하시겠습니까?')) return
  try {
    await axios.delete(`/comments/${commentId}/delete/`)
    comments.value = comments.value.filter(c => c.id !== commentId)
  } catch (err) {
    console.error('댓글 삭제 실패:', err)
  }
}

// Toggle like on comment
const toggleLike = async (comment) => {
  try {
    const res = await axios.post(`/comments/${comment.id}/like/`)
    const updated = {
      ...comment,
      like_count: res.data.likes,
      is_liked: res.data.is_liked
    }
    const idx = comments.value.findIndex(c => c.id === comment.id)
    console.log(updated)
    if (idx !== -1) {
      comments.value[idx] = updated
      comments.value = [...comments.value]  // force Vue to detect reactivity
    }
  } catch (err) {
    console.error('댓글 좋아요 실패:', err)
  }
}

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

onMounted(async () => {
  try {
    const res = await axios.get(`prompts/${route.params.id}/`)
    prompt.value = res.data
  } catch (err) {
    console.error('프롬프트 상세 조회 실패:', err)
  }
  await fetchComments()
})

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