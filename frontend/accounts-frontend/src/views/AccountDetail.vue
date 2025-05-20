<template>
  <div class="account-detail-view">
    <router-link to="/accounts" class="back-link">
      <i class="fas fa-arrow-left"></i> Volver a cuentas
    </router-link>

    <div v-if="loading" class="loading-state">
      <i class="fas fa-spinner fa-spin"></i> Cargando cuenta...
    </div>

    <div v-else-if="!account" class="not-found">
      <i class="fas fa-exclamation-circle"></i>
      <p>Cuenta no encontrada</p>
    </div>

    <div v-else>
      <div class="account-header">
        <div>
          <h2>Cuenta: {{ account.numero_cuenta }}</h2>
          <p class="account-meta">
            <span :class="['account-type', account.tipo.toLowerCase()]">{{ account.tipo }}</span>
            <span class="account-currency">{{ account.moneda }}</span>
          </p>
        </div>
        <span :class="['account-status', account.estado.toLowerCase()]">
          {{ account.estado }}
        </span>
      </div>

      <div class="account-balance">
        <h3>Saldo disponible</h3>
        <p class="balance-amount">{{ formatCurrency(account.saldo) }}</p>
      </div>

      <div class="quick-actions">
        <AppButton @click="showTransactionForm('DEPOSITO')" variant="success">
          <i class="fas fa-plus-circle"></i> Depositar
        </AppButton>
        <AppButton @click="showTransactionForm('RETIRO')" variant="warning">
          <i class="fas fa-minus-circle"></i> Retirar
        </AppButton>
        <router-link 
          :to="`/accounts/${account.id}/transactions`" 
          class="btn btn-info"
        >
          <i class="fas fa-list"></i> Ver historial
        </router-link>
      </div>
    </div>

    <AppModal v-if="showTransactionModal" @close="showTransactionModal = false">
      <template #header>
        {{ transactionType === 'DEPOSITO' ? 'Depositar fondos' : 'Retirar fondos' }}
      </template>
      <TransactionForm
        :account-id="account.id"
        :type="transactionType"
        @submit="handleTransactionSubmit"
        @cancel="showTransactionModal = false"
      />
    </AppModal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useAccountsStore } from '@/stores/accounts';
import TransactionForm from '@/components/transactions/TransactionForm.vue';
import AppButton from '@/components/ui/AppButton.vue';
import AppModal from '@/components/ui/AppModal.vue';

const route = useRoute();
const accountsStore = useAccountsStore();
const { currentAccount: account, loading, fetchAccount } = accountsStore;

const showTransactionModal = ref(false);
const transactionType = ref('DEPOSITO');

onMounted(() => {
  fetchAccount(route.params.id);
});

const formatCurrency = (value) => {
  return new Intl.NumberFormat('es-BO', {
    style: 'currency',
    currency: account.value?.moneda || 'BOB'
  }).format(value);
};

const showTransactionForm = (type) => {
  transactionType.value = type;
  showTransactionModal.value = true;
};

const handleTransactionSubmit = async () => {
  showTransactionModal.value = false;
  await fetchAccount(route.params.id);
};
</script>

<style scoped>
.account-detail-view {
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

.account-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.account-meta {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
  color: var(--text-secondary);
}

.account-type {
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.85rem;
}

.account-type.ahorro {
  background-color: #e8f4fd;
  color: #2980b9;
}

.account-type.corriente {
  background-color: #e8f8f0;
  color: #27ae60;
}

.account-currency {
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  background-color: #f5f5f5;
  font-size: 0.85rem;
}

.account-status {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.9rem;
}

.account-status.activa {
  background-color: #e8f8f0;
  color: #2ecc71;
}

.account-status.bloqueada {
  background-color: #fdecea;
  color: #e74c3c;
}

.account-balance {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: var(--background-light);
  border-radius: 8px;
}

.balance-amount {
  font-size: 2rem;
  font-weight: bold;
  margin-top: 0.5rem;
}

.quick-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 2rem;
}

.loading-state, .not-found {
  text-align: center;
  padding: 3rem;
}

.not-found i {
  font-size: 3rem;
  color: var(--danger-color);
  margin-bottom: 1rem;
}
</style>