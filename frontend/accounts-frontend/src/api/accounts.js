import axios from 'axios'

const API_BASE = '/api/accounts'

export const getAccounts = async () => {
  const response = await axios.get(API_BASE)
  return response.data
}

export const getAccount = async (id) => {
  const response = await axios.get(`${API_BASE}/${id}`)
  return response.data
}

export const createAccount = async (accountData) => {
  const response = await axios.post(API_BASE, accountData)
  return response.data
}

export const updateAccount = async (id, accountData) => {
  const response = await axios.put(`${API_BASE}/${id}`, accountData)
  return response.data
}

export const deleteAccount = async (id) => {
  await axios.delete(`${API_BASE}/${id}`)
}

export const deposit = async (accountId, amount, description = '') => {
  const response = await axios.post(`${API_BASE}/transactions/deposit`, {
    cuenta_id: accountId,
    tipo: 'DEPOSITO',
    monto: amount,
    descripcion: description
  })
  return response.data
}

export const withdraw = async (accountId, amount, description = '') => {
  const response = await axios.post(`${API_BASE}/transactions/withdraw`, {
    cuenta_id: accountId,
    tipo: 'RETIRO',
    monto: amount,
    descripcion: description
  })
  return response.data
}

export const getTransactions = async (accountId) => {
  const response = await axios.get(`${API_BASE}/transactions/account/${accountId}`)
  return response.data
}