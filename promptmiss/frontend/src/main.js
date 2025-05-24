import axios from 'axios'

import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import Toastify from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

axios.defaults.baseURL = 'http://localhost:8000'
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('access')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

const app = createApp(App)

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia)
app.use(router)

app.use(Toastify, {
  autoClose: 3000,
  position: 'top-right',
})

app.mount('#app')
