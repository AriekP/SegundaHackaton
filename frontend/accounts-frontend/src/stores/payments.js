import { defineStore } from 'pinia'
import { 
  getPayments, 
  getPayment, 
  createPayment, 
  getServiceProviders
} from '@/api/payments'

export const usePaymentStore = defineStore('payments', {
  state: () => ({
    payments: [],
    currentPayment: null,
    serviceProviders: [],
    loading: false,
    error: null
  }),
  actions: {
    async fetchPayments(accountId) {
      this.loading = true
      try {
        this.payments = await getPayments(accountId)
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },
    async fetchPayment(id) {
      this.loading = true
      try {
        this.currentPayment = await getPayment(id)
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },
    async fetchServiceProviders() {
      this.loading = true
      try {
        this.serviceProviders = await getServiceProviders()
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    }
  }
})