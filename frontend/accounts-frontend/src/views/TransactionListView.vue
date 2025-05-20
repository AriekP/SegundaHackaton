
<template>
  <div class="transaction-list-view">
    <router-link :to="`/accounts/${accountId}`" class="back-link">
      <i class="fas fa-arrow-left"></i> Volver a la cuenta
    </router-link>

    <div class="header">
      <h2><i class="fas fa-exchange-alt"></i> Historial de Transacciones</h2>
      <div class="balance-info">
        <span>Saldo actual:</span>
        <strong>{{ formatCurrency(account?.saldo || 0) }}</strong>
      </div>
    </div>

    <AppAlert v-if="error" :message="error" type="error" @dismiss="error = null" />

    <div class="controls">
      <div class="filters">
        <select v-model="filterType" class="filter-select">
          <option value="">Todas las transacciones</option>
          <option value="DEPOSITO">Depósitos</option>
          <option value="RETIRO">Retiros</option>
        </select>
        <input
          type="date"
          v-model="filterDate"
          class="date-filter"
          @change="applyDateFilter"
        >
      </div>
      <AppButton @click="showTransactionForm = true" variant="primary">
        <i class="fas fa-plus"></i> Nueva Transacción
      </AppButton>
    </div>

    <div v-if="loading" class="loading-state">
      <i class="fas fa-spinner fa-spin"></i> Cargando transacciones...
    </div>

    <div v-else-if="filteredTransactions.length === 0" class="empty-state">
      <i class="fas fa-exchange-alt"></i>
      <p>No hay transacciones registradas</p>
      <AppButton @click="showTransactionForm = true" variant="outline">
        Realizar primera transacción
      </AppButton>
    </div>

    <div v-else class="transactions">
      <TransactionCard
        v-for="transaction in filteredTransactions"
        :key="transaction.id"
        :transaction="transaction"
        :currency="account?.moneda || 'BOB'"
      />
    </div>

    <AppModal v-if="showTransactionForm" @close="showTransactionForm = false">
      <template #header>
        Nueva Transacción
      </template>
      <TransactionForm
        :account-id="accountId"
        @submit="handleTransactionSubmit"
        @cancel="showTransactionForm = false"
      />
    </AppModal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useAccountsStore } from '@/stores/accounts';
import TransactionCard from '@/components/transactions/TransactionCard.vue';
import TransactionForm from '@/components/transactions/TransactionForm.vue';
import AppAlert from '@/components/ui/AppAlert.vue';
import AppButton from '@/components/ui/AppButton.vue';
import AppModal from '@/components/ui/AppModal.vue';

const route = useRoute();
const accountsStore = useAccountsStore();
const { 
  currentAccount: account, 
  transactions, 
  loading, 
  error, 
  fetchAccount, 
  fetchTransactions 
} = accountsStore;

const accountId = computed(() => route.params.id);
const filterType = ref('');
const filterDate = ref('');
const showTransactionForm = ref(false);

onMounted(() => {
  fetchAccount(accountId.value);
  fetchTransactions(accountId.value);
});

const filteredTransactions = computed(() => {
  let result = [...transactions];
  
  if (filterType.value) {
    result = result.filter(t => t.tipo === filterType.value);
  }
  
  if (filterDate.value) {
    const selectedDate = new Date(filterDate.value).toISOString().split('T')[0];
    result = result.filter(t => {
      const transactionDate = new Date(t.fecha).toISOString().split('T')[0];
      return transactionDate === selectedDate;
    });
  }
  
  return result.sort((a, b) => new Date(b.fecha) - new Date(a.fecha));
});

const formatCurrency = (value) => {
  return new Intl.NumberFormat('es-BO', {
    style: 'currency',
    currency: account.value?.moneda || 'BOB'
  }).format(value);
};

const handleTransactionSubmit = async () => {
  showTransactionForm.value = false;
  await fetchTransactions(accountId.value);
  await fetchAccount(accountId.value);
};

const applyDateFilter = () => {
  if (!filterDate.value) return;
  fetchTransactions(accountId.value, filterDate.value);
};
</script>

<style scoped>
.transaction-list-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  color: var(--primary-color);
  text-decoration: none;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.balance-info {
  background: var(--background-light);
  padding: 0.5rem 1rem;
  border-radius: 4px;
}

.balance-info strong {
  color: var(--success-color);
  margin-left: 0.5rem;
}

.controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.filters {
  display: flex;
  gap: 1rem;
}

.filter-select, .date-filter {
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid var(--border-color);
  background: white;
}

.transactions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: var(--text-secondary);
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: var(--primary-color);
}

.loading-state {
  text-align: center;
  padding: 2rem;
  color: var(--text-secondary);
}
</style>