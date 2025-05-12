import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8001/clientes' // Asegúrate que FastAPI esté corriendo
})

export default api
