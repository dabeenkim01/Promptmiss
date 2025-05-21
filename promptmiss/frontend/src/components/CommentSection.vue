<template>
  <div class="mb-4 flex items-start gap-2">
    <input
      v-model="newComment"
      placeholder="댓글을 입력하세요..."
      class="flex-1 px-3 py-2 rounded bg-zinc-800 text-white border border-zinc-600"
      @keyup.enter="submitComment"
    />
    <button
      @click="submitComment"
      class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
    >작성</button>
  </div>
  <ul>
    <li v-for="comment in comments.filter(c => !c.parent)" :key="comment.id">
      <CommentItem :comment="comment" :prompt-id="promptId" @refresh="emit('refresh')" />
    </li>
  </ul>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import CommentItem from './CommentItem.vue'

const props = defineProps({
  comments: Array,
  promptId: [String, Number],
})

const emit = defineEmits(['refresh'])

const newComment = ref('')

const submitComment = async () => {
  if (!newComment.value.trim()) return
  await axios.post(`/api/prompts/${props.promptId}/comments/`, {
    content: newComment.value,
  })
  newComment.value = ''
  emit('refresh')
}
</script>