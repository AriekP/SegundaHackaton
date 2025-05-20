import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3001, // Puerto diferente al accounts-frontend
    proxy: {
      '/payments': {
        target: 'http://localhost:8001',
        changeOrigin: true
      },
      '/services': {
        target: 'http://localhost:8001',
        changeOrigin: true
      }
    }
  }
})