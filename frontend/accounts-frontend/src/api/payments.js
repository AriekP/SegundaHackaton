import axios from 'axios'

const API_URL = '/payments' // Usa proxy configurado en vite.config.js

export const getPayments = async (accountId) => {
  const response = await axios.get(`${API_URL}/account/${accountId}`)
  return response.data
}

export const getPayment = async (id) => {
  const response = await axios.get(`${API_URL}/${id}`)
  return response.data
}

export const getServiceProviders = async () => {
  const response = await axios.get('/services/providers')
  return response.data
}