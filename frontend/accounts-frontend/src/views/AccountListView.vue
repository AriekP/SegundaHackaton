<template>
  <div class="account-list-view">
    <div class="header">
      <h1><i class="fas fa-wallet"></i> Mis Cuentas</h1>
      <AppButton 
        @click="handleNewAccount" 
        variant="primary"
        icon="plus"
      >
        Nueva Cuenta
      </AppButton>
    </div>

    <AppAlert 
      v-if="error" 
      :message="error" 
      type="error" 
      @dismiss="error = null" 
    />

    <template v-if="loading">
      <div class="skeleton-loader">
        <div v-for="i in 3" :key="i" class="skeleton-card"></div>
      </div>
    </template>

    <template v-else>
      <div v-if="accounts.length === 0" class="empty-state">
        <i class="fas fa-piggy-bank"></i>
        <p>No tienes cuentas registradas</p>
        <AppButton 
          @click="handleNewAccount" 
          variant="outline"
          icon="plus"
        >
          Crear mi primera cuenta
        </AppButton>
      </div>

      <div v-else class="account-grid">
        <AccountCard
          v-for="account in accounts"
          :key="account.id"
          :account="account"
          @edit="handleEditAccount"
          @view-transactions="viewTransactions(account.id)"
        />
      </div>
    </template>

    <AppModal 
      v-if="showAccountForm" 
      @close="closeModal"
      :title="currentAccount ? 'Editar Cuenta' : 'Nueva Cuenta'"
    >
      <AccountForm
        :account="currentAccount"
        @submit="handleAccountSubmit"
        @cancel="closeModal"
      />
    </AppModal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountsStore } from '@/stores/accounts'
import AccountCard from '@/components/accounts/AccountCard.vue'
import AccountForm from '@/components/accounts/AccountForm.vue'
import AppAlert from '@/components/ui/AppAlert.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppModal from '@/components/ui/AppModal.vue'

const router = useRouter()
const accountsStore = useAccountsStore()

const { 
  accounts, 
  loading, 
  error, 
  fetchAccounts, 
  addAccount, 
  updateAccount 
} = accountsStore

const showAccountForm = ref(false)
const currentAccount = ref(null)

onMounted(async () => {
  await fetchAccounts()
})

const handleNewAccount = () => {
  currentAccount.value = null
  showAccountForm.value = true
}

const handleEditAccount = (account) => {
  currentAccount.value = { ...account }
  showAccountForm.value = true
}

const handleAccountSubmit = async (accountData) => {
  try {
    if (currentAccount.value) {
      await updateAccount({ 
        id: currentAccount.value.id, 
        accountData 
      })
    } else {
      await addAccount(accountData)
    }
    closeModal()
  } catch (err) {
    console.error('Error al guardar cuenta:', err)
  }
}

const viewTransactions = (accountId) => {
  router.push({ 
    name: 'account-transactions', 
    params: { id: accountId } 
  })
}

const closeModal = () => {
  showAccountForm.value = false
  currentAccount.value = null
}
</script>

<style scoped>
.account-list-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.account-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: var(--text-secondary);
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: var(--primary-light);
}

.skeleton-loader {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.skeleton-card {
  height: 150px;
  background: var(--background-light);
  border-radius: 8px;
  animation: pulse 1.5s infinite ease-in-out;
}

@keyframes pulse {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 0.3; }
}

@media (max-width: 768px) {
  .account-grid {
    grid-template-columns: 1fr;
  }
  
  .header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>