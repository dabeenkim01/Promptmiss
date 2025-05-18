<template>
  <div class="min-h-screen flex justify-center items-start pt-24 px-4">
    <div class="w-full max-w-3xl bg-zinc-900 text-white p-8 rounded-lg shadow-lg">
      <div v-if="!loading && isOwner">
        <h2 class="text-2xl font-bold mb-6 text-cyan-400">프롬프트 수정</h2>
        <form @submit.prevent="submitForm" class="space-y-6">
          <div>
            <label class="block mb-2 text-gray-300">제목</label>
            <input
              v-model="form.title"
              type="text"
              class="w-full p-2 rounded bg-zinc-800 text-white border border-gray-600"
              required
            />
          </div>
          <div>
            <label class="block mb-2 text-gray-300">내용</label>
            <textarea
              v-model="form.content"
              rows="6"
              class="w-full p-2 rounded bg-zinc-800 text-white border border-gray-600"
              required
            ></textarea>
          </div>
          <div>
            <label class="block mb-2 text-gray-300">태그</label>
            <input
              v-model="form.tags"
              type="text"
              class="w-full p-2 rounded bg-zinc-800 text-white border border-gray-600"
            />
          </div>
          <button
            type="submit"
            :disabled="submitting"
            class="bg-cyan-600 hover:bg-cyan-700 text-white font-bold py-2 px-4 rounded"
          >
            {{ submitting ? '수정 중...' : '수정 완료' }}
          </button>
          <button
            @click="deletePrompt"
            :disabled="deleting"
            class="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded"
          >
            {{ deleting ? '삭제 중...' : '🗑️ 삭제하기' }}
          </button>
        </form>
      </div>
      <p v-else-if="loading" class="text-center text-gray-400">프롬프트 불러오는 중...</p>
      <p v-else class="text-center text-red-400">접근 권한이 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const submitting = ref(false)
const deleting = ref(false)

const route = useRoute()
const router = useRouter()
const promptId = route.params.id

const form = reactive({
  title: '',
  content: '',
  tags: ''
})

const loading = ref(true)
const isOwner = ref(false)
const currentUserId = Number(localStorage.getItem('userId'))  // ensure it's a number

onMounted(async () => {
  try {
    const { data } = await axios.get(`/api/prompts/${promptId}/`)
    form.title = data.title
    form.content = data.content
    form.tags = data.tags

    // 작성자 확인 (data.user가 사용자 id인 경우)
    isOwner.value = Number(currentUserId) === Number(data.user)
  } catch (error) {
    console.error('프롬프트 불러오기 실패:', error)
  } finally {
    loading.value = false
  }
})

const submitForm = async () => {
  submitting.value = true
  try {
    const token = localStorage.getItem('access')
    await axios.put(`/api/prompts/${promptId}/`, form, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
    router.push(`/prompts/${promptId}`)
  } catch (error) {
    console.error('프롬프트 수정 실패:', error)
  } finally {
    submitting.value = false
  }
}

const deletePrompt = async () => {
  if (deleting.value) return

  deleting.value = true
  const confirmed = confirm('정말 삭제하시겠습니까?')
  if (!confirmed) {
    deleting.value = false
    return
  }

  try {
    await axios.delete(`prompts/${route.params.id}/`)
    router.push('/prompts')
  } catch (error) {
    console.error('삭제 실패:', error)
    alert('삭제에 실패했습니다.')
  } finally {
    deleting.value = false
  }
}
</script>