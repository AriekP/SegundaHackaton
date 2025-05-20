import axios from 'axios'

const API_URL = 'http://localhost:8001/payments'

export const getPayments = async (accountId) => {
  const response = await axios.get(`${API_URL}/account/${accountId}`)
  return response.data
}

export const getPayment = async (id) => {
  const response = await axios.get(`${API_URL}/${id}`)
  return response.data
}

export const createPayment = async (paymentData) => {
  const response = await axios.post(API_URL, paymentData)
  return response.data
}

export const getServiceProviders = async () => {
  const response = await axios.get('http://localhost:8001/services/providers')
  return response.data
}

export const getServiceProvider = async (id) => {
  const response = await axios.get(`http://localhost:8001/services/providers/${id}`)
  return response.data
}

export const getProvidersByType = async (type) => {
  const response = await axios.get(`http://localhost:8001/services/providers/by-type/${type}`)
  return response.data
}