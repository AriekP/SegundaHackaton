import { createRouter, createWebHistory } from 'vue-router'
import PaymentList from './views/PaymentList.vue'
import PaymentDetail from './views/PaymentDetail.vue'
import CreatePayment from './views/CreatePayment.vue'
import ServiceProviders from './views/ServiceProviders.vue'

const routes = [
  {
    path: '/',
    name: 'payments',
    component: PaymentList
  },
  {
    path: '/payment/:id',
    name: 'payment-detail',
    component: PaymentDetail,
    props: true
  },
  {
    path: '/create',
    name: 'create-payment',
    component: CreatePayment
  },
  {
    path: '/providers',
    name: 'service-providers',
    component: ServiceProviders
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router