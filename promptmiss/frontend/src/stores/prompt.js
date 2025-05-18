import { defineStore } from 'pinia'
import { ref } from 'vue'

export const usePromptStore = defineStore('prompt', () => {
  const prompts = ref([])

  return { prompts }
}, {
  persist: true
})