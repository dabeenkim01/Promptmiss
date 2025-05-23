<template>
  <div>
    <!-- Hero Section -->
    <section
      class="w-full h-[560px] bg-no-repeat bg-cover bg-center flex flex-col items-center justify-between py-12"
      style="background-image: url('/fromis9.png'); background-position: center top;"
    >
      <div class="flex flex-col items-center mt-8">
        <h1 class="text-4xl sm:text-6xl font-extrabold font-heading mb-3">My Prompt Promise</h1>
        <p class="text-lg sm:text-2xl text-gray-100 font-light">AI 프롬프트의 모든 것, 지금 함께해요</p>
      </div>
      <RouterLink
        to="/prompts/create"
        class="bg-teal-500 hover:bg-teal-400 text-white font-semibold px-8 py-3 rounded-lg shadow-xl transition mb-6"
      >
        + 프롬프트 생성
      </RouterLink>
    </section>

    <!-- Popular Prompts -->
    <section class="max-w-6xl w-full mx-auto pt-8 px-2">
      <p class="text-xl text-white font-semibold mt-2 mb-6">🔥 가장 인기 있는 프롬프트</p>
      <Swiper
        :modules="[Autoplay, Navigation, Pagination]"
        :space-between="20"
        :slides-per-view="1"
        :breakpoints="{
          640: { slidesPerView: 1 },
          768: { slidesPerView: 2 },
          1024: { slidesPerView: 3 }
        }"
        :autoplay="{ delay: 3000, disableOnInteraction: false }"
        navigation
        pagination
        class="pb-8"
      >
        <SwiperSlide v-for="prompt in bestPrompts" :key="prompt.id">
          <PromptCard
            :prompt="prompt"
            @like="promptStore.handleLike"
            @bookmark="promptStore.handleBookmark"
          />
        </SwiperSlide>
      </Swiper>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Autoplay, Navigation, Pagination } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/navigation'
import 'swiper/css/pagination'

import { usePromptStore } from '@/stores/prompt'
import PromptCard from '@/components/PromptCard.vue'
import { RouterLink } from 'vue-router'

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
