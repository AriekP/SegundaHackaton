import { defineStore } from 'pinia'
import { ref } from 'vue'
import {
  getAccounts,
  getAccount,
  createAccount,
  updateAccount,
  deleteAccount,
  deposit,
  withdraw,
  getTransactions
} from '@/api/accounts'

export const useAccountsStore = defineStore('accounts', () => {
  const accounts = ref([])
  const currentAccount = ref(null)
  const transactions = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchAccounts = async () => {
    loading.value = true
    error.value = null
    try {
      accounts.value = await getAccounts()
    } catch (err) {
      error.value = err.message || 'Error al cargar las cuentas'
    } finally {
      loading.value = false
    }
  }

  const fetchAccount = async (id) => {
    loading.value = true
    error.value = null
    try {
      currentAccount.value = await getAccount(id)
    } catch (err) {
      error.value = err.message || 'Error al cargar la cuenta'
    } finally {
      loading.value = false
    }
  }

  const addAccount = async (accountData) => {
    loading.value = true
    error.value = null
    try {
      const newAccount = await createAccount(accountData)
      accounts.value.push(newAccount)
      return newAccount
    } catch (err) {
      error.value = err.message || 'Error al crear la cuenta'
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateAccount = async ({ id, accountData }) => {
    loading.value = true
    error.value = null
    try {
      const updatedAccount = await updateAccount(id, accountData)
      const index = accounts.value.findIndex(a => a.id === id)
      if (index !== -1) {
        accounts.value.splice(index, 1, updatedAccount)
      }
      if (currentAccount.value && currentAccount.value.id === id) {
        currentAccount.value = updatedAccount
      }
      return updatedAccount
    } catch (err) {
      error.value = err.message || 'Error al actualizar la cuenta'
      throw err
    } finally {
      loading.value = false
    }
  }

  const removeAccount = async (id) => {
    loading.value = true
    error.value = null
    try {
      await deleteAccount(id)
      accounts.value = accounts.value.filter(a => a.id !== id)
      if (currentAccount.value && currentAccount.value.id === id) {
        currentAccount.value = null
      }
    } catch (err) {
      error.value = err.message || 'Error al eliminar la cuenta'
      throw err
    } finally {
      loading.value = false
    }
  }

  const makeDeposit = async ({ accountId, amount }) => {
    loading.value = true
    error.value = null
    try {
      const result = await deposit(accountId, amount)
      await fetchAccount(accountId)
      return result
    } catch (err) {
      error.value = err.message || 'Error al realizar el depósito'
      throw err
    } finally {
      loading.value = false
    }
  }

  const makeWithdrawal = async ({ accountId, amount }) => {
    loading.value = true
    error.value = null
    try {
      const result = await withdraw(accountId, amount)
      await fetchAccount(accountId)
      return result
    } catch (err) {
      error.value = err.message || 'Error al realizar el retiro'
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchTransactions = async (accountId) => {
    loading.value = true
    error.value = null
    try {
      transactions.value = await getTransactions(accountId)
    } catch (err) {
      error.value = err.message || 'Error al cargar las transacciones'
    } finally {
      loading.value = false
    }
  }

  return {
    accounts,
    currentAccount,
    transactions,
    loading,
    error,
    fetchAccounts,
    fetchAccount,
    addAccount,
    updateAccount,
    removeAccount,
    makeDeposit,
    makeWithdrawal,
    fetchTransactions
  }
})