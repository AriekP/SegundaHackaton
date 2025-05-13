<template>
  <div class="account-detail-view">
    <RouterLink to="/" class="back-link">← Volver a la lista</RouterLink>

    <AppAlert 
      v-if="error"
      :message="error"
      type="error"
      dismissible
      @dismiss="error = null"
    />

    <div v-if="loading" class="loading">Cargando cuenta...</div>

    <div v-else-if="!account" class="not-found">
      Cuenta no encontrada
    </div>

    <div v-else class="account-detail">
      <div class="account-info">
        <h2>Cuenta: {{ account.numero_cuenta }}</h2>
        <p><strong>Tipo:</strong> {{ account.tipo }}</p>
        <p><strong>Moneda:</strong> {{ account.moneda }}</p>
        <p><strong>Saldo:</strong> {{ account.saldo }} {{ account.moneda }}</p>
        <p><strong>Estado:</strong> <span :class="account.estado.toLowerCase()">{{ account.estado }}</span></p>
      </div>

      <div class="account-actions">
        <button @click="showEditForm = true" class="btn btn-primary">
          Editar Cuenta
        </button>
        <button @click="showTransactionForm = true" class="btn btn-secondary">
          Nueva Transacción
        </button>
        <button @click="handleDelete" class="btn btn-danger">
          Eliminar Cuenta
        </button>
      </div>

      <RouterLink 
        :to="{ name: 'account-transactions', params: { id: account.id } }" 
        class="transactions-link"
      >
        Ver historial de transacciones →
      </RouterLink>
    </div>

    <div v-if="showEditForm" class="modal-overlay">
      <div class="modal">
        <h3>Editar Cuenta</h3>
        <AccountForm
          :account="account"
          @submit="handleUpdateAccount"
          @cancel="showEditForm = false"
          submit-text="Actualizar Cuenta"
        />
      </div>
    </div>

    <div v-if="showTransactionForm" class="modal-overlay">
      <div class="modal">
        <h3>Nueva Transacción</h3>
        <TransactionForm
          :account-id="account.id"
          @submit="handleCreateTransaction"
          @cancel="showTransactionForm = false"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAccountsStore } from '@/stores/accounts'
import AccountForm from '@/components/AccountForm.vue'
import TransactionForm from '@/components/TransactionForm.vue'
import AppAlert from '@/components/AppAlert.vue'

const route = useRoute()
const router = useRouter()
const accountsStore = useAccountsStore()
const { currentAccount: account, loading, error, fetchAccount, updateAccount, removeAccount, makeDeposit, makeWithdrawal } = accountsStore

const showEditForm = ref(false)
const showTransactionForm = ref(false)

watch(() => route.params.id, (newId) => {
  if (newId) {
    fetchAccount(parseInt(newId))
  }
}, { immediate: true })

const handleUpdateAccount = async (accountData) => {
  try {
    await updateAccount({ 
      id: parseInt(route.params.id), 
      accountData 
    })
    showEditForm.value = false
  } catch (err) {
    console.error('Error updating account:', err)
  }
}

const handleCreateTransaction = async (transactionData) => {
  try {
    if (transactionData.tipo === 'DEPOSITO') {
      await makeDeposit({
        accountId: parseInt(route.params.id),
        amount: transactionData.monto
      })
    } else {
      await makeWithdrawal({
        accountId: parseInt(route.params.id),
        amount: transactionData.monto
      })
    }
    showTransactionForm.value = false
  } catch (err) {
    console.error('Error creating transaction:', err)
  }
}

const handleDelete = async () => {
  if (confirm('¿Estás seguro de que deseas eliminar esta cuenta?')) {
    try {
      await removeAccount(parseInt(route.params.id))
      router.push({ name: 'accounts' })
    } catch (err) {
      console.error('Error deleting account:', err)
    }
  }
}
</script>

<style scoped>
.account-detail-view {
  padding: 1rem;
}

.back-link {
  display: inline-block;
  margin-bottom: 1rem;
  color: #3498db;
  text-decoration: none;
}

.account-detail {
  max-width: 800px;
  margin: 0 auto;
}

.account-info {
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.account-info h2 {
  margin-top: 0;
}

.account-actions {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.transactions-link {
  display: inline-block;
  margin-top: 1rem;
  color: #3498db;
  text-decoration: none;
}

.activa {
  color: green;
  font-weight: bold;
}

.bloqueada {
  color: red;
  font-weight: bold;
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

.btn-secondary {
  background-color: #95a5a6;
  color: white;
}

.btn-danger {
  background-color: #e74c3c;
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

.loading, .not-found {
  text-align: center;
  padding: 2rem;
  color: #666;
}
</style>