<template>
  <li
    class="bg-zinc-800 border border-zinc-700 p-6 rounded-lg shadow-md flex flex-col justify-between h-52 hover:shadow-lg hover:scale-[1.02] transition-all"
  >
    <RouterLink :to="`/prompts/${prompt.id}`" class="block">
      <div>
        <h3 class="text-white text-lg font-semibold mb-2">{{ prompt.title }}</h3>
        <p class="text-sm text-gray-400 mb-4 line-clamp-2">{{ prompt.content }}</p>
        <!-- Tags -->
        <div v-if="prompt.tags?.length" class="flex flex-wrap gap-2 mt-2">
          <span
            v-for="tag in prompt.tags"
            :key="tag.id"
            class="bg-teal-700 text-white text-xs font-medium px-3 py-1 rounded-full"
          >
            #{{ tag }}
          </span>
        </div>
      </div>
    </RouterLink>
    <div class="flex justify-between items-center text-l text-gray-400">
      <div class="flex gap-4">
        <span @click="$emit('like', prompt)" class="cursor-pointer select-none hover:text-teal-400">
          {{ prompt.is_liked ? '❤️' : '🤍' }} {{ prompt.like_count }}
        </span>
        <span @click="$emit('bookmark', prompt)" class="cursor-pointer select-none hover:text-amber-400">
          {{ prompt.is_bookmarked ? '📌' : '📎' }} {{ prompt.bookmark_count }}
        </span>
      </div>
    </div>
  </li>
</template>

<script setup>
defineProps({
  prompt: Object,
})
defineEmits(['like', 'bookmark'])
</script>