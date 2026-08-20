import axios from 'axios'

const http = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  withCredentials: true,
})

http.interceptors.response.use(
  response => response,
  error => {
    console.error('Erro na requisição:', error)
    
    if (error.response?.status === 401) {
      if (!window.location.pathname.includes('/login')) {
        window.location.href = '/login'
      }
    }
    
    if (error.response?.status === 404) {
      window.location.href = '/'
    }
    
    return Promise.reject(error)
  }
)

http.interceptors.request.use(
  config => {
    if (import.meta.env.DEV) {
      console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`)
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

export default http
