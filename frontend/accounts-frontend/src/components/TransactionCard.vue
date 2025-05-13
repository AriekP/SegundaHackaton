<template>
  <div class="transaction-card" :class="transaction.tipo.toLowerCase()">
    <div class="transaction-header">
      <h4>{{ transaction.descripcion || 'Transacción sin descripción' }}</h4>
      <span class="transaction-amount" :class="amountClass">
        {{ amountSign }}{{ transaction.monto }} {{ currency }}
      </span>
    </div>
    <div class="transaction-body">
      <p>Fecha: {{ formattedDate }}</p>
      <p v-if="transaction.referencia">Referencia: {{ transaction.referencia }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  transaction: {
    type: Object,
    required: true
  },
  currency: {
    type: String,
    default: 'BOB'
  }
})

const formattedDate = computed(() => {
  return new Date(props.transaction.fecha).toLocaleString()
})

const amountSign = computed(() => {
  return props.transaction.tipo === 'DEPOSITO' ? '+' : '-'
})

const amountClass = computed(() => {
  return props.transaction.tipo === 'DEPOSITO' ? 'positive' : 'negative'
})
</script>

<style scoped>
.transaction-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.transaction-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.transaction-amount {
  font-weight: bold;
}

.positive {
  color: green;
}

.negative {
  color: red;
}

.transaction-body {
  font-size: 0.9rem;
  color: #555;
}

.deposito {
  border-left: 4px solid green;
}

.retiro {
  border-left: 4px solid red;
}
</style>