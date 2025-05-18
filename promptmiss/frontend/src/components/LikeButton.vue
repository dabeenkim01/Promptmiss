<template>
  <button @click="toggleLike">
    {{ isLiked ? '❤️' : '🤍' }} {{ likeCount }}
  </button>
</template>

<script setup>
const emit = defineEmits(['toggled'])

import { ref, watch } from 'vue'
import axios from '@/api/axios'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  prompt: Object,
})

const auth = useAuthStore()
const isLiked = ref(props.prompt.is_liked || false)
const likeCount = ref(props.prompt.like_count || 0)

watch(
  () => props.prompt.like_count,
  (newVal) => {
    likeCount.value = newVal
  }
)

watch(
  () => props.prompt.is_liked,
  (newVal) => {
    isLiked.value = newVal
  }
)

const toggleLike = async () => {
  if (!auth.isLoggedIn) {
    alert('로그인이 필요합니다.')
    return
  }

  try {
    const res = await axios.post(`prompts/${props.prompt.id}/like/`)
    isLiked.value = res.data.is_liked
    likeCount.value = res.data.like_count
    emit('toggled')
  } catch (err) {
    console.error('좋아요 실패:', err)
  }
}
</script>