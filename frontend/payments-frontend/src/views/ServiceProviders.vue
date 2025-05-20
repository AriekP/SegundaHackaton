<template>
  <div>
    <h1>Proveedores de Servicio</h1>
    <div v-if="loading">Cargando...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div v-for="provider in serviceProviders" :key="provider.id" class="provider-item">
        <h3>{{ provider.nombre }}</h3>
        <p>Tipo: {{ provider.tipo_servicio }}</p>
        <p>Código: {{ provider.codigo_servicio }}</p>
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
      await paymentStore.fetchServiceProviders()
    })

    return {
      serviceProviders: paymentStore.serviceProviders,
      loading: paymentStore.loading,
      error: paymentStore.error
    }
  }
}
</script>

<style>
.provider-item {
  padding: 15px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.error {
  color: red;
}
</style>