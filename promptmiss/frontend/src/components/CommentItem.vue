<template>
  <div class="mb-4">
    <div class="flex justify-between items-start">
      <div class="flex-1">
        <p class="text-white">
          <strong class="text-cyan-400">@{{ comment.user.username }}</strong> {{ comment.content }}
        </p>
        <div class="flex gap-4 text-sm text-gray-500 ml-1">
          <span>{{ formatDate(comment.created_at) }}</span>
          <span>{{ comment.like_count }}개</span>
          <span
            v-if="comment.user.username === currentUser"
            @click="deleteComment(comment.id)"
            class="cursor-pointer hover:underline"
          >삭제</span>
          <span @click="showReplyInput = !showReplyInput" class="cursor-pointer hover:underline">답글 달기</span>
        </div>
        <div v-if="showReplyInput" class="mt-2">
          <input
            v-model="replyText"
            @keyup.enter="submitReply"
            placeholder="답글을 입력하세요"
            class="w-full px-3 py-2 rounded bg-zinc-800 text-white border border-zinc-600"
          />
        </div>
        <div v-if="comment.replies && comment.replies.length" class="ml-4 mt-2 space-y-2">
          <button @click="showReplies = !showReplies" class="text-sm text-cyan-400 hover:underline">
            <span v-if="!showReplies">답글 보기 {{ comment.replies.length }}개</span>
            <span v-else>답글 숨기기</span>
          </button>
          <ul v-if="showReplies" class="ml-4 mt-2 space-y-2 text-sm opacity-90">
            <li v-for="reply in comment.replies" :key="reply.id">
              <div class="bg-zinc-800 border border-zinc-700 rounded px-3 py-2">
                <div class="text-white">
                  <strong class="text-cyan-400">@{{ reply.user.username }}</strong> {{ reply.content }}
                </div>
                <div class="text-xs text-gray-500 ml-1">
                  <span>{{ formatDate(reply.created_at) }}</span>
                </div>
                <div class="flex gap-4 text-xs text-gray-500 ml-1">
                  <span
                    @click="handleToggleReplyInput(reply.id)"
                    class="cursor-pointer hover:underline"
                  >답글 달기</span>
                  <span class="cursor-pointer" @click="toggleLike(reply)">
                    <span v-if="reply.is_liked">❤️</span>
                    <span v-else>🤍</span> {{ reply.like_count || 0 }}
                  </span>
                  <span
                    v-if="reply.user.username === currentUser"
                    @click="deleteComment(reply.id)"
                    class="cursor-pointer hover:underline"
                  >삭제</span>
                </div>
                <div v-if="replyStates[reply.id] && replyStates[reply.id].showReplyInput" class="mt-2">
                  <input
                    :value="replyStates[reply.id].replyText"
                    @input="event => replyStates[reply.id].replyText = event.target.value"
                    @keyup.enter="onEnter(reply)"
                    @compositionstart="isComposing = true"
                    @compositionend="isComposing = false"
                    placeholder="답글을 입력하세요"
                    class="w-full px-3 py-2 rounded bg-zinc-800 text-white border border-zinc-600"
                  />
                  <button
                    @click="submitReplyToReply(reply)"
                    class="mt-1 text-xs text-cyan-400 hover:underline"
                  >등록</button>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
      <div class="cursor-pointer pt-1" @click="toggleLike(comment)">
        <span v-if="comment.is_liked">❤️</span>
        <span v-else>🤍</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, toRefs, reactive, watch } from 'vue'
import axios from 'axios'

const isSubmitting = ref(false)
const isComposing = ref(false)

const replyText = ref('')
const showReplyInput = ref(false)

const props = defineProps({
  comment: Object,
  promptId: Number
})
const { comment, promptId } = toRefs(props)

const emit = defineEmits(['refresh'])

const showReplies = ref(false)

const replyStates = reactive({})

const currentUser = localStorage.getItem('username')

watch(showReplies, (val) => {
  if (val && comment.value.replies) {
    comment.value.replies.forEach(reply => {
      if (!replyStates[reply.id]) {
        replyStates[reply.id] = {
          replyText: '',
          showReplyInput: false
        }
      }
    })
  }
})

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('ko-KR', { year: 'numeric', month: 'short', day: 'numeric' })
}

const toggleLike = async (target) => {
  const res = await axios.post(`/api/comments/${target.id}/like/`)
  target.is_liked = res.data.is_liked
  target.like_count = res.data.like_count
}

const deleteComment = async (id) => {
  try {
    await axios.delete(`/api/comments/${id}/delete/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access')}`
      }
    })
    emit('refresh')
  } catch (err) {
    console.error('댓글 삭제 실패:', err)
  }
}

const submitReply = async () => {
  if (!replyText.value.trim()) return
  try {
    await axios.post(`/api/prompts/${promptId.value}/comments/`, {
      content: replyText.value,
      parent: comment.value.id,
    })
    replyText.value = ''
    showReplyInput.value = false
    emit('refresh')
  } catch (err) {
    console.error('답글 등록 실패:', err)
  }
}

const submitReplyToReply = async (replyTarget) => {
  const state = replyStates[replyTarget.id]
  if (!state?.replyText?.trim() || isSubmitting.value) return

  isSubmitting.value = true

  try {
    const res = await axios.post(`/api/comments/${replyTarget.id}/replies/`, {
      content: state.replyText,
    })

    const newReply = {
      ...res.data,
      user: { username: currentUser },
      like_count: 0,
      is_liked: false,
    }

    if (!comment.value.replies) {
      comment.value.replies = [newReply]
    } else {
      comment.value.replies = [...comment.value.replies, newReply]
    }

    showReplies.value = true

    for (const key in replyStates) {
      replyStates[key].replyText = ''
      replyStates[key].showReplyInput = false
    }
  } catch (err) {
    console.error('대댓글 답글 등록 실패:', err)
  } finally {
    isSubmitting.value = false
  }
}

const onEnter = (replyTarget) => {
  if (!isComposing.value) {
    submitReplyToReply(replyTarget)
  }
}
</script>