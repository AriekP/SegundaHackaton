// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'   // 👈 Importa el router

import './style.css'

createApp(App)
  .use(router)                 // 👈 Usa el router
  .mount('#app')
