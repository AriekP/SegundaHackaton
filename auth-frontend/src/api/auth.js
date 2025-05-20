// src/api/auth.js
import axios from 'axios'

const API = axios.create({
  baseURL: 'http://localhost:8005',
})

export const login = async (credentials) => {
  const response = await API.post('/login', credentials, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })
  return response.data
}

export const getPerfil = async (token) => {
  const response = await API.get('/me', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  return response.data
}
export const signup = async (data) => {
  const response = await API.post('/signup', data)
  return response.data
}
