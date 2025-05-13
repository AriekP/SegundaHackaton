import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8001/clientes' // Asegúrate que FastAPI esté corriendo
  //baseURL: 'http://clientes-backend:8001/clientes'  // nombre del servicio en docker-compose
})

export default api
