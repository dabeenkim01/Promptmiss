<template>
  <div>
    <section
      class="w-full h-[450px] bg-no-repeat bg-cover bg-top flex items-center justify-center text-white text-4xl font-bold"
      style="background-image: url('/fromis9.png');"
    >
    PROMPTMISS
    </section>
    <section class="max-w-6xl w-full mx-auto pt-2 px-2">
      <p class="text-xl text-white font-semibold mt-4 mb-6">🔥 가장 인기 있는 프롬프트</p>
      <ul class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <li
          v-for="prompt in bestPrompts"
          :key="prompt.id"
          class="bg-zinc-800 border border-zinc-700 p-6 rounded-lg shadow-md flex flex-col justify-between h-52"
        >
          <div>
            <h3 class="text-white text-lg font-semibold mb-2">{{ prompt.title }}</h3>
            <p class="text-sm text-gray-400 mb-4 line-clamp-2">{{ prompt.content }}</p>
          </div>
          <div class="flex justify-between items-center text-sm text-gray-400">
            <div class="flex gap-4">
              <span @click="promptStore.handleLike(prompt)" class="cursor-pointer select-none hover:text-teal-400">
                ❤️ {{ prompt.like_count }}
              </span>
              <span @click="promptStore.handleBookmark(prompt)" class="cursor-pointer select-none hover:text-amber-400">
                🔖 {{ prompt.bookmark_count }}
              </span>
            </div>
          </div>
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { usePromptStore } from '@/stores/prompt'

const promptStore = usePromptStore()
const bestPrompts = ref([])

onMounted(async () => {
  try {
    await promptStore.fetchPrompts('all')
    bestPrompts.value = [...promptStore.prompts]
      .sort((a, b) => b.like_count - a.like_count)
      .slice(0, 5)
  } catch (err) {
    console.error('실시간 인기 프롬프트 불러오기 실패:', err)
  }
})
</script>

<style scoped>
  
</style>