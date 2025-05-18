<template>
  <button @click="toggleBookmark">
    {{ isBookmarked ? '🔖' : '📑' }} {{ bookmarkCount }}
  </button>
</template>

<script setup>
import { ref, watch } from 'vue'
import axios from '@/api/axios'
import { useAuthStore } from '@/stores/auth'

const emit = defineEmits(['toggled'])

const props = defineProps({
  prompt: Object,
})

const auth = useAuthStore()
const isBookmarked = ref(props.prompt.is_bookmarked || false)
const bookmarkCount = ref(props.prompt.bookmark_count || 0)

watch(
  () => props.prompt.bookmark_count,
  (newVal) => {
    bookmarkCount.value = newVal
  }
)

watch(
  () => props.prompt.is_bookmarked,
  (newVal) => {
    isBookmarked.value = newVal
  }
)

const toggleBookmark = async () => {
  if (!auth.isLoggedIn) {
    alert('로그인이 필요합니다.')
    return
  }

  try {
    const res = await axios.post(`prompts/${props.prompt.id}/bookmark/`)
    isBookmarked.value = res.data.is_bookmarked
    bookmarkCount.value = res.data.bookmark_count
    emit('toggled')
  } catch (err) {
    console.error('북마크 실패:', err)
  }
}
</script>