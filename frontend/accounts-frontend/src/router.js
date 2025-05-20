import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'accounts',
    component: () => import('@/views/AccountListView.vue'),
    meta: { title: 'Mis Cuentas' }
  },
  {
    path: '/accounts/:id',
    name: 'account-detail',
    component: () => import('@/views/AccountDetail.vue'),
    props: true,
    meta: { title: 'Detalle de Cuenta' }
  },
  {
    path: '/accounts/:id/transactions',
    name: 'account-transactions',
    component: () => import('@/views/TransactionListView.vue'),
    props: true,
    meta: { title: 'Historial de Transacciones' }
  },
  {
    path: '/payments',
    name: 'payments',
    component: () => import('@/views/payments/PaymentListView.vue'),
    meta: { title: 'Mis Pagos' }
  },
  {
    path: '/payments/:id',
    name: 'payment-detail',
    component: () => import('@/views/payments/PaymentDetail.vue'),
    props: true,
    meta: { title: 'Detalle de Pago' }
  },
  {
    path: '/providers',
    name: 'providers',
    component: () => import('@/views/payments/ServiceProviders.vue'),
    meta: { title: 'Proveedores' }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFound.vue'),
    meta: { title: 'Página no encontrada' }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0 }
  }
})

router.beforeEach((to) => {
  const title = to.meta.title || 'Banca en Línea'
  document.title = `${title} | Tu Banco`
  window.scrollTo(0, 0)
})

export default router