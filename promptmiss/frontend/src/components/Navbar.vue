<template>
  <nav class="navbar">
    <RouterLink to="/" class="brand">PROMPTMISS</RouterLink>
    <div class="nav-right">
      <RouterLink to="/prompts" class="nav-link">📚 프롬프트</RouterLink>
      <template v-if="!auth.isLoggedIn">
        <span class="separator"> | </span>
        <RouterLink to="/signup" class="nav-link">📝 회원가입</RouterLink>
        <span class="separator"> | </span>
        <RouterLink to="/login" class="nav-link">🔐 로그인</RouterLink>
      </template>
      <template v-else>
        <span class="separator"> | </span>
        <RouterLink to="/mypage" class="nav-link">👤 마이페이지</RouterLink>
        <span class="separator"> | </span>
        <span @click="logout" class="nav-link cursor-pointer">🚪 로그아웃</span>
      </template>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const logout = () => {
  auth.logout()
}
</script>

<style scoped>
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem;
    background-color: #1e1e1e;
    border-bottom: 1px solid #333;
    font-size: 1.1rem;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
}

.nav-link {
    color: #ffffff;
    text-decoration: none;
    margin: 0 0.5rem;
}

.nav-link:hover {
    color: #4fc3f7;
}

.separator {
    color: #888;
    margin: 0 0.5rem;
}

.brand {
    font-weight: bold;
    font-size: 1.2rem;
    color: hsla(160, 100%, 37%, 1);
    text-decoration: none;
    margin-right: auto;
}

.nav-right {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
</style>