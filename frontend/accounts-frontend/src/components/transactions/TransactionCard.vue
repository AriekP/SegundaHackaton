<template>
  <div class="transaction-card" :class="transaction.tipo.toLowerCase()">
    <div class="transaction-icon">
      <i v-if="transaction.tipo === 'DEPOSITO'" class="fas fa-arrow-down"></i>
      <i v-else class="fas fa-arrow-up"></i>
    </div>
    
    <div class="transaction-details">
      <div class="transaction-header">
        <h4>{{ transaction.descripcion || 'Transacción sin descripción' }}</h4>
        <span class="amount" :class="transaction.tipo.toLowerCase()">
          {{ amountSign }}{{ formatCurrency(transaction.monto) }}
        </span>
      </div>
      
      <div class="transaction-meta">
        <span class="date">{{ formatDate(transaction.fecha) }}</span>
        <span v-if="transaction.referencia" class="reference">
          Ref: {{ transaction.referencia }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  transaction: {
    type: Object,
    required: true
  },
  currency: {
    type: String,
    default: 'BOB'
  }
});

const amountSign = computed(() => {
  return props.transaction.tipo === 'DEPOSITO' ? '+' : '-';
});

const formatCurrency = (value) => {
  return new Intl.NumberFormat('es-BO', {
    style: 'currency',
    currency: props.currency
  }).format(value);
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString('es-BO', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};
</script>

<style scoped>
.transaction-card {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s;
}

.transaction-card:hover {
  transform: translateY(-2px);
}

.transaction-card.deposito {
  border-left: 4px solid var(--success-color);
}

.transaction-card.retiro {
  border-left: 4px solid var(--warning-color);
}

.transaction-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--background-light);
}

.transaction-icon i {
  font-size: 1rem;
}

.transaction-card.deposito .transaction-icon {
  color: var(--success-color);
}

.transaction-card.retiro .transaction-icon {
  color: var(--warning-color);
}

.transaction-details {
  flex: 1;
}

.transaction-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.transaction-header h4 {
  margin: 0;
  font-size: 1rem;
  font-weight: 500;
}

.amount {
  font-weight: bold;
}

.amount.deposito {
  color: var(--success-color);
}

.amount.retiro {
  color: var(--warning-color);
}

.transaction-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.reference {
  padding: 0.1rem 0.5rem;
  background: var(--background-light);
  border-radius: 4px;
}
</style>