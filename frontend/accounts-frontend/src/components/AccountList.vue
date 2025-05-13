<template>
  <div>
    <h2>Lista de Cuentas</h2>
    <div v-if="loading">Cargando...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <ul v-else>
      <li v-for="account in accounts" :key="account.id">
        <router-link :to="`/accounts/${account.id}`">
          {{ account.numero_cuenta }} - {{ account.saldo }} {{ account.moneda }}
        </router-link>
      </li>
    </ul>
    <router-link to="/accounts/new">Crear Nueva Cuenta</router-link>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useAccountsStore } from '@/stores/accounts'

export default {
  name: 'AccountList',
  setup() {
    const store = useAccountsStore()
    
    // Cargar cuentas al montar el componente
    store.fetchAccounts()
    
    return {
      accounts: computed(() => store.accounts),
      loading: computed(() => store.loading),
      error: computed(() => store.error)
    }
  }
}
</script>