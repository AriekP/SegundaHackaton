<template>
  <div>
    <h1>Detalle de Pago</h1>
    <div v-if="loading">Cargando...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="payment">
      <p>Referencia: {{ payment.referencia }}</p>
      <p>Monto: {{ payment.monto }}</p>
      <p>Estado: {{ payment.estado }}</p>
      <p>Código de Confirmación: {{ payment.codigo_confirmacion }}</p>
    </div>
  </div>
</template>

<script>
import { usePaymentStore } from '../stores/payments'
import { onMounted } from 'vue'

export default {
  props: ['id'],
  setup(props) {
    const paymentStore = usePaymentStore()
    
    onMounted(async () => {
      await paymentStore.fetchPayment(props.id)
    })

    return {
      payment: paymentStore.currentPayment,
      loading: paymentStore.loading,
      error: paymentStore.error
    }
  }
}
</script>