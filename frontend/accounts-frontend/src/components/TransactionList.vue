<template>
  <div class="transaction-list-view">
    <RouterLink :to="{ name: 'account-detail', params: { id: accountId } }" class="back-link">
      ← Volver al detalle de la cuenta
    </RouterLink>

    <div class="header">
      <h2>Transacciones de la Cuenta</h2>
      <button @click="showForm = true" class="btn btn-primary">
        Nueva Transacción
      </button>
    </div>

    <AppAlert 
      v-if="error"
      :message="error"
      type="error"
      dismissible
      @dismiss="error = null"
    />

    <div v-if="loading" class="loading">Cargando transacciones...</div>

    <div v-else-if="transactions.length === 0" class="empty-state">
      No hay transacciones registradas para esta cuenta
    </div>

    <div v-else class="transactions-list">
      <TransactionCard 
        v-for="transaction in transactions"
        :key="transaction.id"
        :transaction="transaction"
        :currency="currency"
      />
    </div>

    <div v-if="showForm" class="modal-overlay">
      <div class="modal">
        <h3>Nueva Transacción</h3>
        <TransactionForm
          :account-id="accountId"
          @submit="handleCreateTransaction"
          @cancel="showForm = false"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAccountsStore } from '@/stores/accounts'
import TransactionCard from '@/components/TransactionCard.vue'
import TransactionForm from '@/components/TransactionForm.vue'
import AppAlert from '@/components/AppAlert.vue'

const route = useRoute()
const accountsStore = useAccountsStore()
const { currentAccount, transactions, loading, error, fetchTransactions, makeDeposit, makeWithdrawal } = accountsStore

const accountId = computed(() => parseInt(route.params.id))
const currency = computed(() => currentAccount.value?.moneda || 'BOB')
const showForm = ref(false)

watch(accountId, (newId) => {
  if (newId) {
    fetchTransactions(newId)
  }
}, { immediate: true })

const handleCreateTransaction = async (transactionData) => {
  try {
    if (transactionData.tipo === 'DEPOSITO') {
      await makeDeposit({
        accountId: accountId.value,
        amount: transactionData.monto
      })
    } else {
      await makeWithdrawal({
        accountId: accountId.value,
        amount: transactionData.monto
      })
    }
    showForm.value = false
  } catch (err) {
    console.error('Error creating transaction:', err)
  }
}
</script>

<style scoped>
.transaction-list-view {
  padding: 1rem;
}

.back-link {
  display: inline-block;
  margin-bottom: 1rem;
  color: #3498db;
  text-decoration: none;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.transactions-list {
  max-width: 800px;
  margin: 0 auto;
}

.empty-state, .loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-primary {
  background-color: #3498db;
  color: white;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
}
</style>