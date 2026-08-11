import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// Frontend Vue.js (consome a API FastAPI em backend/).
// Roda em http://localhost:5173 por padrão.
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
  },
})
