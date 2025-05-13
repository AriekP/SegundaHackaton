import { defineStore } from 'pinia'
import { 
  getPayments, getPayment, createPayment,
  getServiceProviders, getServiceProvider, getProvidersByType
} from '@/api/payments'

export const usePaymentsStore = defineStore('payments', {
  state: () => ({
    payments: [],
    currentPayment: null,
    serviceProviders: [],
    currentProvider: null,
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
    async addPayment(paymentData) {
      this.loading = true
      try {
        const newPayment = await createPayment(paymentData)
        this.payments.push(newPayment)
        return newPayment
      } catch (error) {
        this.error = error.message
        throw error
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
    },
    async fetchServiceProvider(id) {
      this.loading = true
      try {
        this.currentProvider = await getServiceProvider(id)
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },
    async fetchProvidersByType(type) {
      this.loading = true
      try {
        this.serviceProviders = await getProvidersByType(type)
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    }
  }
})