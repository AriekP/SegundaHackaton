<template>
  <div class="providers">
    <h2>Proveedores de Servicio</h2>
    <div v-if="loading">Cargando...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div v-for="provider in serviceProviders" :key="provider.id">
        <h3>{{ provider.nombre }}</h3>
        <p>Tipo: {{ provider.tipo_servicio }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { usePaymentStore } from '@/stores/payments'

const paymentStore = usePaymentStore()

onMounted(() => {
  paymentStore.fetchServiceProviders()
})
</script>