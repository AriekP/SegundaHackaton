<template>
  <div class="container">
    <header class="app-header">
      <h1 class="app-title">Gestión de Préstamos</h1>
      <p class="app-subtitle">Sistema integral de administración de préstamos</p>
    </header>

    <div class="card form-card">
      <h2 class="form-title">{{ editando ? 'Editar Préstamo' : 'Nuevo Préstamo' }}</h2>
      <form @submit.prevent="guardarPrestamo" class="loan-form">
        <div class="form-grid">
          <div class="form-group">
            <label class="form-label">ID del Cliente</label>
            <input v-model="form.cliente_id" type="number" class="form-input" placeholder="Ingrese ID del cliente" required />
          </div>
          
          <div class="form-group">
            <label class="form-label">Monto (BOB)</label>
            <div class="input-with-icon">
              <span class="currency-icon"></span>
              <input v-model="form.monto" type="number" step="0.01" class="form-input" placeholder="0.00" required />
            </div>
          </div>
          
          <div class="form-group">
            <label class="form-label">Tasa de Interés (%)</label>
            <div class="input-with-icon">
              <span class="percent-icon"></span>
              <input v-model="form.interes" type="number" step="0.01" class="form-input" placeholder="0.00" required />
            </div>
          </div>
          
          <div class="form-group">
            <label class="form-label">Plazo (meses)</label>
            <input v-model="form.plazo_meses" type="number" class="form-input" placeholder="Número de meses" required />
          </div>
          
          <div class="form-group">
            <label class="form-label">Tipo de Préstamo</label>
            <select v-model="form.tipo" class="form-select" required>
              <option value="consumo">Consumo</option>
              <option value="hipotecario">Hipotecario</option>
              <option value="personal">Personal</option>
            </select>
          </div>
          
          <div class="form-group">
            <label class="form-label">Fecha de Solicitud</label>
            <input v-model="form.fecha_solicitud" type="date" class="form-input" required />
          </div>
          
          <div class="form-group">
            <label class="form-label">Estado</label>
            <select v-model="form.estado" class="form-select" required>
              <option value="pendiente">Pendiente</option>
              <option value="aprobado">Aprobado</option>
              <option value="rechazado">Rechazado</option>
              <option value="pagado">Pagado</option>
            </select>
          </div>
        </div>
        
        <div class="form-group full-width">
          <label class="form-label">Observaciones</label>
          <textarea v-model="form.observaciones" class="form-textarea" placeholder="Notas adicionales (opcional)"></textarea>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn btn-primary">
            <span class="btn-icon">{{ editando ? '🔄' : '➕' }}</span>
            {{ editando ? 'Actualizar Préstamo' : 'Crear Préstamo' }}
          </button>
          <button v-if="editando" type="button" @click="cancelarEdicion" class="btn btn-secondary">
            <span class="btn-icon">✖</span>
            Cancelar
          </button>
        </div>
      </form>
    </div>

    <div class="card list-card">
      <div class="list-header">
        <h2 class="list-title">Listado de Préstamos</h2>
        <div class="list-controls">
          <button @click="cargarPrestamos" class="btn btn-refresh" title="Recargar lista">
            <span class="btn-icon">🔄</span>
          </button>
        </div>
      </div>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Cargando préstamos...</p>
      </div>
      
      <div v-else-if="prestamos.length === 0" class="empty-state">
        <div class="empty-icon">📄</div>
        <h3>No hay préstamos registrados</h3>
        <p>Comience agregando un nuevo préstamo usando el formulario superior</p>
      </div>
      
      <div v-else class="loan-list">
        <div v-for="p in prestamos" :key="p.id" class="loan-item" :class="'status-' + p.estado">
          <div class="loan-main-info">
            <div class="loan-client">
              <span class="info-label">Cliente:</span>
              <span class="client-id">#{{ p.cliente_id }}</span>
            </div>
            <div class="loan-amount">
              <span class="info-label">Monto:</span>
              <span class="amount-value">{{ formatCurrency(p.monto) }}</span>
            </div>
            <div class="loan-type">
              <span class="loan-type-badge" :class="'type-' + p.tipo">{{ formatTipo(p.tipo) }}</span>
            </div>
          </div>
          
          <div class="loan-details">
            <div class="detail-item">
              <span class="detail-label">Interés:</span>
              <span class="detail-value">{{ p.interes }}%</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Plazo:</span>
              <span class="detail-value">{{ p.plazo_meses }} meses</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Solicitud:</span>
              <span class="detail-value">{{ formatDate(p.fecha_solicitud) }}</span>
            </div>
            <div class="detail-item status-item">
              <span class="detail-label">Estado:</span>
              <span class="status-badge" :class="'status-' + p.estado">{{ formatEstado(p.estado) }}</span>
            </div>
          </div>
          
          <div v-if="p.observaciones" class="loan-notes">
            <span class="notes-label">Observaciones:</span>
            <p class="notes-content">{{ p.observaciones }}</p>
          </div>
          
          <div class="loan-actions">
            <button @click="editar(p)" class="btn btn-edit" title="Editar préstamo">
              <span class="btn-icon">✏️</span>
              <span class="btn-text">Editar</span>
            </button>
            <button @click="confirmarEliminar(p.id)" class="btn btn-delete" title="Eliminar préstamo">
              <span class="btn-icon">🗑️</span>
              <span class="btn-text">Eliminar</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const prestamos = ref([])
const editando = ref(false)
const idEditando = ref(null)
const loading = ref(true)

const form = ref({
  cliente_id: '',
  monto: '',
  interes: '',
  plazo_meses: '',
  tipo: 'consumo',
  fecha_solicitud: new Date().toISOString().split('T')[0],
  estado: 'pendiente',
  observaciones: ''
})

// Funciones de formato
const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'short', day: 'numeric' }
  return new Date(dateString).toLocaleDateString('es-ES', options)
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: 'BOB',
    minimumFractionDigits: 2
  }).format(value)
}

const formatTipo = (tipo) => {
  const tipos = {
    consumo: 'Consumo',
    hipotecario: 'Hipotecario',
    personal: 'Personal'
  }
  return tipos[tipo] || tipo
}

const formatEstado = (estado) => {
  const estados = {
    pendiente: 'Pendiente',
    aprobado: 'Aprobado',
    rechazado: 'Rechazado',
    pagado: 'Pagado'
  }
  return estados[estado] || estado
}

// Operaciones CRUD
const cargarPrestamos = async () => {
  try {
    loading.value = true
    const response = await api.get('/')
    prestamos.value = response.data
  } catch (error) {
    console.error('Error al cargar préstamos:', error)
    alert('No se pudieron cargar los préstamos')
  } finally {
    loading.value = false
  }
}

const guardarPrestamo = async () => {
  try {
    const data = {
      ...form.value,
      cliente_id: parseInt(form.value.cliente_id),
      monto: parseFloat(form.value.monto),
      interes: parseFloat(form.value.interes),
      plazo_meses: parseInt(form.value.plazo_meses)
    }

    if (editando.value) {
      await api.put(`/${idEditando.value}`, data)
    } else {
      await api.post('/', data)
    }
    
    cancelarEdicion()
    await cargarPrestamos()
  } catch (error) {
    console.error('Error al guardar préstamo:', error)
    alert('Error al guardar el préstamo. Verifica los datos.')
  }
}

const editar = (prestamo) => {
  form.value = { 
    ...prestamo,
    fecha_solicitud: prestamo.fecha_solicitud.split('T')[0]
  }
  idEditando.value = prestamo.id
  editando.value = true
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const confirmarEliminar = (id) => {
  if (confirm('¿Estás seguro de que deseas eliminar este préstamo?')) {
    eliminarPrestamo(id)
  }
}

const eliminarPrestamo = async (id) => {
  try {
    await api.delete(`/${id}`)
    await cargarPrestamos()
  } catch (error) {
    console.error('Error al eliminar préstamo:', error)
    alert('No se pudo eliminar el préstamo')
  }
}

const cancelarEdicion = () => {
  form.value = {
    cliente_id: '',
    monto: '',
    interes: '',
    plazo_meses: '',
    tipo: 'consumo',
    fecha_solicitud: new Date().toISOString().split('T')[0],
    estado: 'pendiente',
    observaciones: ''
  }
  editando.value = false
  idEditando.value = null
}

onMounted(cargarPrestamos)
</script>

<style scoped>
/* Variables de diseño */
:root {
  --primary-color: #4361ee;
  --primary-hover: #3a56d4;
  --secondary-color: #6c757d;
  --secondary-hover: #5a6268;
  --success-color: #28a745;
  --danger-color: #dc3545;
  --warning-color: #ffc107;
  --info-color: #17a2b8;
  --light-color: #f8f9fa;
  --dark-color: #343a40;
  --border-radius: 8px;
  --box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  --transition: all 0.3s ease;
}

/* Estilos base */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #f5f7fa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* Encabezado */
.app-header {
  text-align: center;
  margin-bottom: 30px;
  padding: 20px 0;
}

.app-title {
  font-size: 2.2rem;
  color: var(--primary-color);
  margin-bottom: 8px;
  font-weight: 700;
}

.app-subtitle {
  font-size: 1.1rem;
  color: var(--secondary-color);
  opacity: 0.9;
}

/* Tarjetas */
.card {
  background: white;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  padding: 25px;
  margin-bottom: 30px;
}

.form-card {
  border-top: 4px solid var(--primary-color);
}

.list-card {
  border-top: 4px solid var(--info-color);
}

/* Formulario */
.form-title {
  font-size: 1.5rem;
  color: var(--dark-color);
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.loan-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-label {
  font-weight: 600;
  color: #495057;
  font-size: 0.95rem;
}

.form-input, .form-select, .form-textarea {
  padding: 12px 15px;
  border: 1px solid #ced4da;
  border-radius: var(--border-radius);
  font-size: 1rem;
  transition: var(--transition);
}

.form-input:focus, .form-select:focus, .form-textarea:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.2);
}

.form-textarea {
  min-height: 100px;
  resize: vertical;
}

.input-with-icon {
  position: relative;
}

.input-with-icon .form-input {
  padding-left: 40px;
}

.currency-icon, .percent-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--secondary-color);
  font-weight: bold;
}

.currency-icon::before {
  content: 'Bs';
}

.percent-icon::before {
  content: '%';
}

/* Botones */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  border: none;
  border-radius: var(--border-radius);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition);
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
}

.btn-primary:hover {
  background-color: var(--primary-hover);
  transform: translateY(-2px);
}

.btn-secondary {
  background-color: var(--secondary-color);
  color: white;
}

.btn-secondary:hover {
  background-color: var(--secondary-hover);
  transform: translateY(-2px);
}

.btn-edit {
  background-color: var(--warning-color);
  color: #212529;
}

.btn-edit:hover {
  background-color: #e0a800;
  transform: translateY(-2px);
}

.btn-delete {
  background-color: var(--danger-color);
  color: white;
}

.btn-delete:hover {
  background-color: #c82333;
  transform: translateY(-2px);
}

.btn-refresh {
  background-color: transparent;
  color: var(--secondary-color);
  padding: 8px;
  border: 1px solid #dee2e6;
}

.btn-refresh:hover {
  background-color: #f8f9fa;
}

.btn-icon {
  font-size: 1.1rem;
}

.btn-text {
  display: inline-block;
}

@media (max-width: 768px) {
  .btn-text {
    display: none;
  }
}

.form-actions {
  display: flex;
  gap: 15px;
  margin-top: 10px;
}

/* Listado de préstamos */
.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.list-title {
  font-size: 1.5rem;
  color: var(--dark-color);
}

.list-controls {
  display: flex;
  gap: 10px;
}

/* Items de préstamo */
.loan-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.loan-item {
  padding: 20px;
  border-radius: var(--border-radius);
  background: white;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  transition: var(--transition);
  border-left: 4px solid var(--primary-color);
}

.loan-item:hover {
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.loan-main-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  flex-wrap: wrap;
  gap: 10px;
}

.loan-client {
  display: flex;
  align-items: center;
  gap: 8px;
}

.info-label {
  font-weight: 600;
  color: var(--secondary-color);
}

.client-id {
  font-weight: 700;
  color: var(--dark-color);
}

.loan-amount {
  font-size: 1.2rem;
  font-weight: 700;
}

.amount-value {
  color: var(--primary-color);
}

.loan-details {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 15px;
  margin-bottom: 15px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.detail-label {
  font-size: 0.85rem;
  color: var(--secondary-color);
}

.detail-value {
  font-weight: 500;
}

.status-item {
  align-items: flex-start;
}

.status-badge {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: capitalize;
}

.status-pendiente {
  background-color: #fff3cd;
  color: #856404;
}

.status-aprobado {
  background-color: #d4edda;
  color: #155724;
}

.status-rechazado {
  background-color: #f8d7da;
  color: #721c24;
}

.status-pagado {
  background-color: #d1ecf1;
  color: #0c5460;
}

.loan-type-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: capitalize;
}

.type-consumo {
  background-color: #e2e3e5;
  color: #383d41;
}

.type-hipotecario {
  background-color: #d6d8db;
  color: #1b1e21;
}

.type-personal {
  background-color: #cce5ff;
  color: #004085;
}

.loan-notes {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px dashed #eee;
}

.notes-label {
  font-weight: 600;
  color: var(--secondary-color);
  font-size: 0.9rem;
}

.notes-content {
  margin-top: 5px;
  color: #6c757d;
  font-size: 0.95rem;
  line-height: 1.5;
}

.loan-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
  justify-content: flex-end;
}

/* Estados */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  gap: 15px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 15px;
  opacity: 0.5;
}

.empty-state h3 {
  color: var(--secondary-color);
  margin-bottom: 10px;
}

.empty-state p {
  color: var(--secondary-color);
  opacity: 0.8;
}

/* Responsive */
@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .loan-details {
    grid-template-columns: 1fr 1fr;
  }
  
  .loan-actions {
    justify-content: flex-start;
  }
}

@media (max-width: 480px) {
  .loan-details {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
  }
}
</style>