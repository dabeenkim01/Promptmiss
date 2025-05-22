<template>
  <div class="max-w-4xl mx-auto px-4 py-6 text-white">
    <h1 class="text-2xl font-bold mb-4">👤 마이페이지</h1>

    <section v-if="user" class="mb-6 bg-zinc-800 p-4 rounded-lg">
      <h2 class="text-lg font-semibold mb-2">내 정보</h2>
      <p><strong>사용자명:</strong> {{ user.username }}</p>
      <p><strong>이메일:</strong> {{ user.email }}</p>
    </section>

    <section class="mb-6 bg-zinc-800 p-4 rounded-lg">
      <h2 class="text-lg font-semibold mb-2">내 프롬프트</h2>
      <ul>
        <li v-for="prompt in myPrompts" :key="prompt.id">
          📌 {{ prompt.title }}
        </li>
      </ul>
    </section>

    <section class="bg-zinc-800 p-4 rounded-lg">
      <h2 class="text-lg font-semibold mb-2">좋아요한 프롬프트</h2>
      <ul>
        <li v-for="prompt in likedPrompts" :key="prompt.id">
          ❤️ {{ prompt.title }}
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { usePromptStore } from '@/stores/prompt'
import { useRoute } from 'vue-router'

const userStore = useUserStore()
const promptStore = usePromptStore()

const user = ref({})
const myPrompts = ref([])
const likedPrompts = ref([])

onMounted(async () => {
  const route = useRoute()
  await userStore.fetchUserProfile(route.params.id)
  user.value = userStore.profile

  await promptStore.fetchPrompts('mine')
  myPrompts.value = promptStore.prompts

  await promptStore.fetchPrompts('liked')
  likedPrompts.value = promptStore.prompts
})
</script>