<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <h2 class="text-2xl font-bold text-white mb-6 border-b border-gray-700 pb-2">
      {{ isEditable ? '마이페이지' : (userData?.nickname || '사용자') + '의 프로필' }}
    </h2>

    <div v-if="userData">
      <div class="flex flex-col items-center mb-6">
        <img
          :src="previewUrl || userData.profile_image || '/src/assets/default-profile.png'"
          class="w-24 h-24 rounded-full object-cover border border-white mb-2"
          alt="프로필 이미지"
        />
        <h3 class="text-lg font-semibold text-white">{{ userData.nickname }}</h3>
        <p class="text-sm text-gray-300">{{ userData.bio }}</p>
      </div>

      <div v-if="isEditable" class="flex flex-col sm:flex-row items-center gap-4 mb-6">
        <button
          v-if="userData.profile_image"
          @click="handleDeleteImage"
          class="px-4 py-2 text-sm border border-red-400 text-red-400 rounded hover:bg-red-500 hover:text-white transition"
        >
          프로필 이미지 삭제
        </button>

        <label class="px-4 py-2 bg-gray-700 text-white rounded cursor-pointer hover:bg-gray-600 transition">
          이미지 선택
          <input type="file" accept="image/*" class="hidden" @change="handleFileChange" />
        </label>

        <span v-if="selectedFile" class="text-sm text-gray-300">{{ selectedFile.name }}</span>
      </div>

      <form v-if="isEditable" @submit.prevent="handleSubmit" class="space-y-4 mt-6">
        <div>
          <label class="block text-sm text-gray-300">닉네임</label>
          <input v-model="userData.nickname" type="text" class="w-full px-3 py-2 rounded bg-zinc-800 text-white border border-zinc-600" />
        </div>
        <div>
          <label class="block text-sm text-gray-300">자기소개</label>
          <textarea v-model="userData.bio" rows="3" class="w-full px-3 py-2 rounded bg-zinc-800 text-white border border-zinc-600" />
        </div>
        <button type="submit" class="bg-teal-500 px-4 py-2 text-white rounded w-full">저장하기</button>
      </form>
      <p v-else class="text-gray-400 text-sm">이 프로필은 수정할 수 없습니다.</p>

      <div class="mt-10">
        <h3 class="text-xl font-semibold text-white mb-4 border-b border-gray-700 pb-1">작성한 프롬프트</h3>
        <ul class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <PromptCard
            v-for="prompt in userPrompts"
            :key="prompt.id"
            :prompt="prompt"
            @like="() => {}"
            @bookmark="() => {}"
          />
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import PromptCard from '@/components/PromptCard.vue'

const router = useRouter()
const userStore = useUserStore()
const authStore = useAuthStore()
const userData = ref(null)
const selectedFile = ref(null)
const previewUrl = ref(null)
const userPrompts = ref([])
const route = useRoute()
const isMyPage = ref(false)

const isEditable = computed(() => {
  return String(userData.value?.id) === String(authStore.userId)
})

const fetchUserPrompts = async (userId) => {
  try {
    const res = await fetch(`/api/prompts/?user_id=${userId}`)
    const data = await res.json()
    userPrompts.value = data.results || data
  } catch (err) {
    console.error('프롬프트 불러오기 실패:', err)
  }
}

onMounted(async () => {
  const id = String(route.params.id)
  const isMyProfile = id === String(authStore.userId)
  isMyPage.value = isMyProfile

  await userStore.fetchUserProfile(id)
  userData.value = userStore.profile
  await fetchUserPrompts(id)

  if (!userData.value.nickname) {
    userData.value.nickname = userData.value.username
  }
})

const handleFileChange = (e) => {
  selectedFile.value = e.target.files[0]
  if (selectedFile.value) {
    previewUrl.value = URL.createObjectURL(selectedFile.value)
  }
}

const handleSubmit = async () => {
  if (!isEditable.value) return
  const formData = new FormData()
  if (selectedFile.value) {
    formData.append('profile_image', selectedFile.value)
  }
  formData.append('nickname', userData.value.nickname || '')
  formData.append('bio', userData.value.bio || '')

  try {
    const res = await fetch('/api/accounts/me/', {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access')}`,
      },
      body: formData,
    })
    const data = await res.json()
    userData.value = data
    alert('프로필 정보가 업데이트되었습니다!')
  } catch (err) {
    console.error(err)
    alert('업로드 실패')
  }
}

const handleDeleteImage = async () => {
  try {
    const res = await fetch('/api/accounts/me/', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('access')}`,
      },
      body: JSON.stringify({ profile_image: null }),
    })
    const data = await res.json()
    userData.value = data
    previewUrl.value = null
    alert('이미지가 삭제되었습니다!')
  } catch (err) {
    console.error(err)
    alert('삭제 실패')
  }
}
</script>