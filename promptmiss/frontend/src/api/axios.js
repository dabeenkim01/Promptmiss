// src/api/axios.js
import axios from 'axios'

const instance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/',
})

instance.interceptors.request.use(
  (config) => {
    const access = localStorage.getItem('access')
    if (access) {
      config.headers.Authorization = `Bearer ${access}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

instance.interceptors.response.use(
  response => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      try {
        const refresh = localStorage.getItem('refresh')
        const res = await axios.post(`${instance.defaults.baseURL}token/refresh/`, { refresh })
        const newAccess = res.data.access

        localStorage.setItem('access', newAccess)
        originalRequest.headers.Authorization = `Bearer ${newAccess}`

        return instance(originalRequest)
      } catch {
        localStorage.removeItem('access')
        localStorage.removeItem('refresh')
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  }
)

export default instance