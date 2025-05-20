<template>
  <div>
    <h1>Historial de Pagos</h1>
    <div v-if="loading">Cargando...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div v-for="payment in payments" :key="payment.id" class="payment-item">
        <router-link :to="{ name: 'payment-detail', params: { id: payment.id } }">
          {{ payment.referencia }} - {{ payment.monto }}
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { usePaymentStore } from '../stores/payments'
import { onMounted } from 'vue'

export default {
  setup() {
    const paymentStore = usePaymentStore()
    
    onMounted(async () => {
      // Asumimos que accountId viene de la autenticación o parámetro
      await paymentStore.fetchPayments(1) // Cambiar por el accountId real
    })

    return {
      payments: paymentStore.payments,
      loading: paymentStore.loading,
      error: paymentStore.error
    }
  }
}
</script>

<style>
.payment-item {
  padding: 10px;
  border-bottom: 1px solid #eee;
}
.error {
  color: red;
}
</style>