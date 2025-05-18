<template>
  <div class="min-h-screen bg-zinc-900 text-white">
    <Navbar />
    <main class="max-w-6xl w-full mx-auto pt-20 px-4">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
</script>