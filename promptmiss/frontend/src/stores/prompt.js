import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from '@/api/axios'

export const usePromptStore = defineStore('prompt', () => {
  const prompts = ref([])

  const fetchPrompts = async (filter = 'all') => {
    let endpoint = 'prompts/'
    if (filter === 'mine') endpoint += '?mine=true'
    else if (filter === 'liked') endpoint += '?liked=true'
    else if (filter === 'bookmarked') endpoint += '?bookmarked=true'

    try {
      const res = await axios.get(endpoint)
      prompts.value = res.data.results || res.data
    } catch (err) {
      console.error('[fetchPrompts] 실패:', err)
    }
  }

  const toggleLike = async (promptId) => {
    try {
      const res = await axios.post(`prompts/${promptId}/like/`)
      const { is_liked, like_count } = res.data
      const prompt = prompts.value.find((p) => p.id === promptId)
      if (prompt) {
        prompt.is_liked = is_liked
        prompt.like_count = like_count

        // 필터가 liked인데 좋아요 취소한 경우 목록에서 제거
        if (!is_liked && window.location.search.includes('liked')) {
          prompts.value = prompts.value.filter((p) => p.id !== promptId)
        }
      }
      return res.data
    } catch (err) {
      console.error('[toggleLike] 실패:', err)
      throw err
    }
  }

  const toggleBookmark = async (promptId) => {
    try {
      const res = await axios.post(`prompts/${promptId}/bookmark/`)
      const { is_bookmarked, bookmark_count } = res.data
      const prompt = prompts.value.find((p) => p.id === promptId)
      if (prompt) {
        prompt.is_bookmarked = is_bookmarked
        prompt.bookmark_count = bookmark_count

        // 필터가 bookmarked인데 북마크 취소한 경우 목록에서 제거
        if (!is_bookmarked && window.location.search.includes('bookmarked')) {
          prompts.value = prompts.value.filter((p) => p.id !== promptId)
        }
      }
      return res.data
    } catch (err) {
      console.error('[toggleBookmark] 실패:', err)
      throw err
    }
  }

  const handleLike = async (prompt) => {
    try {
      const res = await toggleLike(prompt.id)
      prompt.is_liked = res.is_liked
      prompt.like_count = res.like_count

      if (!res.is_liked && window.location.search.includes('liked')) {
        prompts.value = prompts.value.filter((p) => p.id !== prompt.id)
      }
    } catch (err) {
      console.error('[handleLike] 실패:', err)
    }
  }

  const handleBookmark = async (prompt) => {
    try {
      const res = await toggleBookmark(prompt.id)
      prompt.is_bookmarked = res.is_bookmarked
      prompt.bookmark_count = res.bookmark_count

      if (!res.is_bookmarked && window.location.search.includes('bookmarked')) {
        prompts.value = prompts.value.filter((p) => p.id !== prompt.id)
      }
    } catch (err) {
      console.error('[handleBookmark] 실패:', err)
    }
  }

  return {
    prompts,
    fetchPrompts,
    toggleLike,
    toggleBookmark,
    handleLike,
    handleBookmark,
  }
})
