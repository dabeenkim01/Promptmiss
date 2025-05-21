<template>
  <div class="max-w-6xl mx-auto px-4 py-6 flex flex-col items-start space-y-4">
    <div class="w-full flex justify-between items-center">
      <h1 class="text-xl">📚 전체 프롬프트 목록</h1>
      <RouterLink to="/prompts/create">
        <button class="create-button">+ 프롬프트 생성</button>
      </RouterLink>
    </div>

    <div class="w-full">
      <div class="min-h-[3.5rem] flex items-center gap-4 mb-4">
        <button :class="{ active: filterType === 'all' }" @click="setFilter('all')">전체</button>
        <button :class="{ active: filterType === 'mine' }" @click="setFilter('mine')">내 프롬프트</button>
        <button :class="{ active: filterType === 'liked' }" @click="setFilter('liked')">좋아요한</button>
        <button :class="{ active: filterType === 'bookmarked' }" @click="setFilter('bookmarked')">북마크한</button>
      </div>

      <div v-if="isLoading" class="text-gray-400">불러오는 중...</div>

      <ul v-else-if="prompts.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <li v-for="prompt in prompts" :key="prompt.id" class="bg-zinc-800 text-white p-4 rounded-xl shadow hover:shadow-lg hover:scale-[1.02] transition-all h-52 flex flex-col justify-between">
          <RouterLink :to="`/prompts/${prompt.id}`" class="block">
            <h3 class="text-lg font-bold text-teal-400 mb-1">{{ prompt.title }}</h3>
            <p class="text-xs text-gray-400">작성자: {{ prompt.user.username }}</p>
            <p class="text-sm text-gray-300 line-clamp-3">{{ prompt.content }}</p>
          </RouterLink>
          <div class="flex justify-end items-center gap-3 text-sm text-gray-400 mt-3">
            <span @click="promptStore.handleLike(prompt)" class="cursor-pointer">
              {{ prompt.is_liked ? '❤️' : '🤍' }} {{ prompt.like_count }}
            </span>
            <span @click="promptStore.handleBookmark(prompt)" class="cursor-pointer">
              {{ prompt.is_bookmarked ? '📌' : '📎' }} {{ prompt.bookmark_count }}
            </span>
          </div>
        </li>
      </ul>
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div class="col-span-full h-52 bg-zinc-800 text-gray-400 flex items-center justify-center rounded-xl shadow">
          표시할 프롬프트가 없습니다.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { usePromptStore } from '@/stores/prompt'
import { useRoute, useRouter } from 'vue-router'

const filterType = ref('all')
const promptStore = usePromptStore()
const prompts = computed(() => promptStore.prompts)
const isLoading = ref(false)
const route = useRoute()
const router = useRouter()

const fetchPrompts = () => {
  promptStore.fetchPrompts(filterType.value)
}

const setFilter = (type) => {
  filterType.value = type
  if (type === 'all') {
    router.replace({ query: {} })
  } else {
    router.replace({ query: { filter: type } })
  }
  fetchPrompts()
}

onMounted(() => {
  const initial = route.query.filter || 'all'
  filterType.value = initial
  fetchPrompts()
})
</script>

<style scoped>
  .create-button {
    background-color: #4CAF50;
    color: white;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  .create-button:hover {
    background-color: #45a049;
  }
</style>