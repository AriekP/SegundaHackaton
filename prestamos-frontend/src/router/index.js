import { createRouter, createWebHistory } from 'vue-router'
import Prestamos from '../views/Prestamos.vue'

const routes = [
  { path: '/', component: Prestamos }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
