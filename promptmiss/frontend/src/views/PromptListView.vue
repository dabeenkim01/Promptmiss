<template>
  <div class="max-w-6xl mx-auto px-4 py-6 flex flex-col items-start space-y-4">
    <div class="w-full flex justify-between items-center">
      <h1 class="text-xl">📚 전체 프롬프트 목록</h1>
      <RouterLink to="/prompts/create">
        <button class="create-button">+ 프롬프트 생성</button>
      </RouterLink>
    </div>

    <div class="w-full">
      <div class="min-h-[3.5rem] flex items-center gap-2 mb-4">
        <button :class="{ active: filterType === 'all' }" @click="setFilter('all')">전체</button>
        <button :class="{ active: filterType === 'mine' }" @click="setFilter('mine')">내 프롬프트</button>
        <button :class="{ active: filterType === 'liked' }" @click="setFilter('liked')">좋아요한</button>
        <button :class="{ active: filterType === 'bookmarked' }" @click="setFilter('bookmarked')">북마크한</button>
      </div>

      <ul v-if="prompts.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <li v-for="prompt in prompts" :key="prompt.id" class="bg-zinc-800 text-white p-4 rounded-xl shadow hover:shadow-lg hover:scale-[1.02] transition-all h-52 flex flex-col justify-between">
          <RouterLink :to="`/prompts/${prompt.id}`" class="block">
            <h3 class="text-lg font-bold text-teal-400 mb-1">{{ prompt.title }}</h3>
            <p class="text-sm text-gray-300 line-clamp-3">{{ prompt.content }}</p>
          </RouterLink>
          <div class="flex justify-end items-center gap-3 text-sm text-gray-400 mt-3">
            <LikeButton :prompt="prompt" @toggled="onToggle(prompt.id, 'like')" />
            <BookmarkButton :prompt="prompt" @toggled="onToggle(prompt.id, 'bookmark')" />
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
import LikeButton from '@/components/LikeButton.vue'
import BookmarkButton from '@/components/BookmarkButton.vue'
import { ref, onMounted } from 'vue'
import axios from '@/api/axios'
import { useRoute, useRouter } from 'vue-router'

const prompts = ref([])
const filterType = ref('all')
const route = useRoute()
const router = useRouter()

const fetchPrompts = async () => {
  let endpoint = 'prompts/'

  if (filterType.value === 'mine') {
    endpoint += '?mine=true'
  } else if (filterType.value === 'liked') {
    endpoint += '?liked=true'
  } else if (filterType.value === 'bookmarked') {
    endpoint += '?bookmarked=true'
  }

  try {
    const response = await axios.get(endpoint)
    prompts.value = response.data
  } catch (error) {
    console.error('프롬프트 불러오기 실패:', error)
  }
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
const onToggle = (id, type) => {
  const prompt = prompts.value.find(p => p.id === id)
  if (!prompt) return

  // 눌린 버튼의 상태만 토글
  if (type === 'like') {
    prompt.is_liked = !prompt.is_liked
  } else if (type === 'bookmark') {
    prompt.is_bookmarked = !prompt.is_bookmarked
  }

  // 필터 조건 만족하지 않으면 제거
  if (filterType.value === 'liked' && !prompt.is_liked) {
    prompts.value = prompts.value.filter(p => p.id !== id)
  } else if (filterType.value === 'bookmarked' && !prompt.is_bookmarked) {
    prompts.value = prompts.value.filter(p => p.id !== id)
  }
}
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