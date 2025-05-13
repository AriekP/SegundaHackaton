import { createRouter, createWebHistory } from 'vue-router'
import AccountListView from '@/views/AccountListView.vue'
import AccountDetail from '@/views/AccountDetail.vue'
import TransactionList from '@/views/TransactionList.vue'
import NotFound from '@/views/NotFound.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'accounts',
      component: AccountListView
    },
    {
      path: '/accounts/:id',
      name: 'account-detail',
      component: AccountDetail,
      props: true
    },
    {
      path: '/accounts/:id/transactions',
      name: 'account-transactions',
      component: TransactionList,
      props: true
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: NotFound
    }
  ]
})

export default router