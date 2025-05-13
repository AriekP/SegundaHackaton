<template>
  <div class="account-list-view">
    <div class="header-actions">
      <h2>Lista de Cuentas</h2>
      <button @click="showForm = true" class="btn btn-primary">
        Crear Nueva Cuenta
      </button>
    </div>

    <AppAlert 
      v-if="error"
      :message="error"
      type="error"
      dismissible
      @dismiss="error = null"
    />

    <div v-if="loading" class="loading">Cargando cuentas...</div>

    <div v-else-if="accounts.length === 0" class="empty-state">
      No hay cuentas registradas
    </div>

    <div v-else class="accounts-grid">
      <AccountCard 
        v-for="account in accounts"
        :key="account.id"
        :account="account"
      />
    </div>

    <div v-if="showForm" class="modal-overlay">
      <div class="modal">
        <h3>Crear Nueva Cuenta</h3>
        <AccountForm
          @submit="handleCreateAccount"
          @cancel="showForm = false"
          submit-text="Crear Cuenta"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAccountsStore } from '@/stores/accounts'
import AccountCard from '@/components/AccountCard.vue'
import AccountForm from '@/components/AccountForm.vue'
import AppAlert from '@/components/AppAlert.vue'

const accountsStore = useAccountsStore()
const { accounts, loading, error, fetchAccounts, addAccount } = accountsStore

const showForm = ref(false)

onMounted(() => {
  fetchAccounts()
})

const handleCreateAccount = async (accountData) => {
  try {
    await addAccount(accountData)
    showForm.value = false
  } catch (err) {
    console.error('Error creating account:', err)
  }
}
</script>

<style scoped>
.account-list-view {
  padding: 1rem;
}

.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.accounts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.loading, .empty-state {
  text-align: center;
  padding: 2rem;
  color: #666;
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
</style>