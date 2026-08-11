import axios from 'axios'

// Instância única do axios apontando para o backend FastAPI.
// withCredentials: true é essencial para o cookie de sessão
// (login de usuário/ONG) ser enviado e aceito entre localhost:5173 e :8000.
const http = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  withCredentials: true,
})

// Interceptor de resposta para tratamento global de erros
http.interceptors.response.use(
  response => response,
  error => {
    // Log do erro para debugging
    console.error('Erro na requisição:', error)
    
    // Se for erro de autenticação (401), redirecionar para login
    if (error.response?.status === 401) {
      // Verificar se não estamos já na página de login para evitar loops
      if (!window.location.pathname.includes('/login')) {
        window.location.href = '/login'
      }
    }
    
    // Se for erro 404, redirecionar para página não encontrada
    if (error.response?.status === 404) {
      window.location.href = '/'
    }
    
    return Promise.reject(error)
  }
)

// Interceptor de requisição para log
http.interceptors.request.use(
  config => {
    // Log para debugging em desenvolvimento
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