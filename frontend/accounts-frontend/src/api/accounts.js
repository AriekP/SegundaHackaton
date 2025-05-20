import axios from 'axios'

const API_URL = 'http://localhost:8000/accounts'

export const createAccount = async (accountData) => {
  const response = await axios.post(API_URL, accountData)
  return response.data
}

export const updateAccount = async (id, accountData) => {
  const response = await axios.put(`${API_URL}/${id}`, accountData)
  return response.data
}

export const getAccount = async (id) => {
  const response = await axios.get(`${API_URL}/${id}`)
  return response.data
}