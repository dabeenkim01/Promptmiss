<template>
  <Navbar />
  <div class="min-h-screen pt-[62px] bg-zinc-900 text-white">
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
</script>