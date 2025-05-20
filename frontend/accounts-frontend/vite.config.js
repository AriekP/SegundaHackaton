import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/accounts': {  // ← Cambiado de '/api' a '/accounts'
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false  // ← Añadido para desarrollo local
        // rewrite: (path) => path.replace(/^\/accounts/, '') ← Solo si quieres eliminar el prefijo
      }
    }
  }
})