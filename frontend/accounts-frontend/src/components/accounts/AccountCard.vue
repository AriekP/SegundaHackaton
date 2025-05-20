<template>
  <div class="account-card" :class="account.estado.toLowerCase()">
    <div class="account-header">
      <h3>{{ account.numero_cuenta }}</h3>
      <span class="account-type">{{ account.tipo }}</span>
    </div>
    
    <div class="account-body">
      <div class="balance">
        <span class="currency">{{ account.moneda }}</span>
        <span class="amount">{{ formatCurrency(account.saldo) }}</span>
      </div>
    </div>
    
    <div class="account-footer">
      <AppButton variant="outline" size="sm" @click="$emit('edit', account)">
        <i class="fas fa-edit"></i> Editar
      </AppButton>
      <AppButton 
        variant="outline" 
        size="sm" 
        @click="$emit('view-transactions', account.id)"
      >
        <i class="fas fa-list"></i> Movimientos
      </AppButton>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import AppButton from '@/components/ui/AppButton.vue';

const props = defineProps({
  account: {
    type: Object,
    required: true
  }
});

const formatCurrency = (value) => {
  return new Intl.NumberFormat('es-BO', {
    style: 'currency',
    currency: props.account.moneda
  }).format(value);
};
</script>

<style scoped>
.account-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s, box-shadow 0.2s;
  border-left: 4px solid var(--primary-color);
}

.account-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.account-card.bloqueada {
  opacity: 0.7;
  border-left-color: var(--danger-color);
}

.account-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.account-header h3 {
  margin: 0;
  font-size: 1.1rem;
}

.account-type {
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.8rem;
  background: var(--background-light);
  color: var(--text-secondary);
}

.account-body {
  margin-bottom: 1.5rem;
}

.balance {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.currency {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.amount {
  font-size: 1.5rem;
  font-weight: bold;
}

.account-footer {
  display: flex;
  gap: 0.5rem;
}
</style>