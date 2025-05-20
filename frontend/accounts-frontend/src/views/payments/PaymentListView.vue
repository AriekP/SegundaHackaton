<template>
  <div class="payment-list">
    <h2>Historial de Pagos</h2>
    <div v-if="loading">Cargando...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div v-for="payment in payments" :key="payment.id" class="payment-item">
        <RouterLink :to="{ name: 'payment-detail', params: { id: payment.id } }">
          {{ payment.referencia }} - {{ payment.monto }}
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { usePaymentStore } from '@/stores/payments'

const paymentStore = usePaymentStore()

onMounted(() => {
  paymentStore.fetchPayments(1) // Asume accountId=1 para el MVP
})
</script>

<style scoped>
.payment-item {
  padding: 10px;
  border-bottom: 1px solid #eee;
}
</style>