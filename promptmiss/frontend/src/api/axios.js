// src/api/axios.js
import axios from 'axios'

const instance = axios.create({
  baseURL: 'http://localhost:8000/api/',
})

// JWT access 토큰 자동 첨부
instance.interceptors.request.use(
  function (config) {
    const access = localStorage.getItem('access')
    if (access) {
      config.headers.Authorization = `Bearer ${access}`
    }
    return config
  },
  function (error) {
    return Promise.reject(error)
  }
)

// 자동 토큰 재발급 인터셉터
instance.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      try {
        const refresh = localStorage.getItem('refresh')
        const res = await axios.post('http://localhost:8000/api/token/refresh/', { refresh })
        const newAccess = res.data.access

        localStorage.setItem('access', newAccess)
        originalRequest.headers.Authorization = `Bearer ${newAccess}`

        return instance(originalRequest)
      } catch (refreshError) {
        console.error('🔒 Refresh 실패:', refreshError)
        localStorage.removeItem('access')
        localStorage.removeItem('refresh')
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  }
)

export default instance