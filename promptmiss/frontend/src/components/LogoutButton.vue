<template>
  <RouterLink to="/" class="nav-link logout-link" @click.prevent="handleLogout">🚪 로그아웃</RouterLink>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
const auth = useAuthStore()

const handleLogout = () => {
  auth.logout()
}
</script>

<style scoped>
.logout-link {
  display: inline-block;
  line-height: 1.5;
  vertical-align: middle;
  color: #ffffff;
  text-decoration: none;
  font-size: 1.1rem;
  margin: 0 0.5rem;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s;
}

.logout-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}
.nav-link {
  color: #ffffff;
  text-decoration: none;
  margin: 0 0.5rem;
}

.nav-link:hover {
  color: #4fc3f7;
}
</style>