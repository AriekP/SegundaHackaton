<template>
  <div class="contenedor">
    <h2>Gestión de Clientes</h2>

    <form @submit.prevent="handleSubmit" class="formulario">
      <div class="form-grid">
        <div class="form-group">
          <label for="nombre">Nombre completo <span class="required">*</span></label>
          <input id="nombre" v-model="form.nombre" required 
                 placeholder="Ej: Juan Pérez"
                 aria-describedby="nombre-help" />
          <small id="nombre-help" class="help-text">Nombre completo del cliente</small>
        </div>

        <div class="form-group">
          <label for="correo">Correo electrónico <span class="required">*</span></label>
          <input id="correo" v-model="form.correo" type="email" required
                 placeholder="Ej: juan@correo.com"
                 :class="{ 'input-error': errors.correo }"
                 aria-describedby="correo-help" />
          <small id="correo-help" class="help-text">{{ errors.correo || 'Formato válido: nombre@dominio.com' }}</small>
        </div>

        <div class="form-group">
          <label for="telefono">Teléfono</label>
          <input id="telefono" v-model="form.telefono" type="tel"
                 placeholder="Ej: +591 70012345"
                 pattern="^\+?\d{6,15}$"
                 aria-describedby="telefono-help" />
          <small id="telefono-help" class="help-text">Formato internacional opcional</small>
        </div>

        <div class="form-group">
          <label for="ci">Cédula de Identidad <span class="required">*</span></label>
          <input id="ci" v-model="form.ci" required
                 placeholder="Ej: 1234567 LP"
                 maxlength="15"
                 aria-describedby="ci-help" />
          <small id="ci-help" class="help-text">Número de documento con extensión</small>
        </div>

        <div class="form-group">
          <label for="fecha_nac">Fecha de Nacimiento <span class="required">*</span></label>
          <input id="fecha_nac" v-model="form.fecha_nac" type="date" required
                 :max="maxDate"
                 aria-describedby="fecha-help" />
          <small id="fecha-help" class="help-text">Formato: DD/MM/AAAA</small>
        </div>

        <div class="form-group">
          <label for="direccion">Dirección</label>
          <input id="direccion" v-model="form.direccion"
                 placeholder="Ej: Calle Principal #123"
                 aria-describedby="direccion-help" />
          <small id="direccion-help" class="help-text">Dirección completa</small>
        </div>
      </div>

      <div class="acciones">
        <button type="submit" class="btn-primary" :disabled="processing">
          {{ editando ? 'Actualizar' : 'Agregar' }}
          <span v-if="processing" class="spinner"></span>
        </button>
        <button v-if="editando" type="button" class="btn-secondary" 
                @click="cancelarEdicion" :disabled="processing">
          Cancelar
        </button>
      </div>
    </form>

    <div v-if="loading" class="loading">Cargando clientes...</div>
    
    <div v-else>
      <div v-if="clientes.length === 0" class="empty-state">
        No hay clientes registrados
      </div>

      <ul class="lista-clientes" aria-live="polite">
        <li v-for="cliente in clientes" :key="cliente.id" class="cliente-item">
          <div class="cliente-info">
            <div class="cliente-header">
              <h3 class="cliente-nombre">{{ cliente.nombre }}</h3>
              <span class="cliente-ci">{{ cliente.ci }}</span>
            </div>
            <p class="cliente-correo">{{ cliente.correo }}</p>
            <p v-if="cliente.telefono" class="cliente-telefono">Tel: {{ cliente.telefono }}</p>
            <p v-if="cliente.direccion" class="cliente-direccion">{{ cliente.direccion }}</p>
            <p class="cliente-fecha">Nacimiento: {{ formatDate(cliente.fecha_nac) }}</p>
          </div>
          <div class="cliente-acciones">
            <button @click="editarCliente(cliente)" class="btn-edit" 
                    aria-label="Editar cliente">
              ✏️ Editar
            </button>
            <button @click="eliminarCliente(cliente.id)" class="btn-delete" 
                    aria-label="Eliminar cliente">
              🗑️ Eliminar
            </button>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../api'

const clientes = ref([])
const loading = ref(true)
const processing = ref(false)
const editando = ref(false)
const idEditando = ref(null)

const form = ref({
  nombre: '',
  correo: '',
  telefono: '',
  ci: '',
  fecha_nac: '',
  direccion: ''
})

const errors = ref({
  correo: ''
})

const maxDate = computed(() => {
  const today = new Date()
  return today.toISOString().split('T')[0]
})

const validateEmail = (email) => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return regex.test(email)
}

const cargarClientes = async () => {
  try {
    const res = await api.get('/')
    clientes.value = res.data
  } catch (error) {
    console.error('Error al cargar clientes:', error)
    alert('No se pudieron cargar los clientes.')
  }
}

const limpiarFormulario = () => {
  Object.keys(form.value).forEach(k => form.value[k] = '')
  editando.value = false
  idEditando.value = null
}

const handleSubmit = async () => {
  processing.value = true
  errors.value.correo = ''

  if (!validateEmail(form.value.correo)) {
    errors.value.correo = 'Correo electrónico inválido'
    processing.value = false
    return
  }

  try {
    if (editando.value) {
      await api.put(`/${idEditando.value}`, form.value)
    } else {
      await api.post('/', form.value)
    }
    await cargarClientes()
    limpiarFormulario()
  } catch (error) {
    console.error('Error al guardar:', error)
    alert('Ocurrió un error. Por favor intente nuevamente.')
  } finally {
    processing.value = false
  }
}

const editarCliente = (cliente) => {
  form.value = { ...cliente }
  editando.value = true
  idEditando.value = cliente.id
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const cancelarEdicion = () => {
  limpiarFormulario()
}

const eliminarCliente = async (id) => {
  if (confirm("¿Estás seguro de eliminar este cliente?")) {
    try {
      await api.delete(`/${id}`)
      await cargarClientes()
    } catch (error) {
      console.error("Error al eliminar cliente:", error)
      alert("No se pudo eliminar el cliente.")
    }
  }
}

const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString('es-ES', options)
}

onMounted(async () => {
  await cargarClientes()
  loading.value = false
})

</script>

<style scoped>
/* Estilos mejorados con enfoque en accesibilidad y diseño moderno */
.contenedor {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 15px rgba(0,0,0,0.1);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-weight: 500;
  color: #333;
}

.required {
  color: #e53e3e;
}

input {
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  transition: border-color 0.2s;
}

input:focus {
  border-color: #4299e1;
  outline: none;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2);
}

.input-error {
  border-color: #fc8181;
}

.help-text {
  color: #718096;
  font-size: 0.875rem;
}

.acciones {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

/* Estilos para botones y estados */
button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary {
  background: #4299e1;
  color: white;
}

.btn-primary:hover {
  background: #3182ce;
}

.btn-primary:disabled {
  background: #cbd5e0;
  cursor: not-allowed;
}

.btn-secondary {
  background: #e2e8f0;
  color: #2d3748;
}

.btn-secondary:hover {
  background: #cbd5e0;
}

.btn-edit {
  background: #f6e05e;
  color: #2d3748;
}

.btn-delete {
  background: #fc8181;
  color: white;
}

/* Estilos para la lista de clientes */
.lista-clientes {
  margin-top: 2rem;
  display: grid;
  gap: 1rem;
}

.cliente-item {
  background: #f7fafc;
  border-radius: 8px;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1.5rem;
}

.cliente-header {
  display: flex;
  align-items: baseline;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.cliente-nombre {
  margin: 0;
  color: #2d3748;
}

.cliente-ci {
  color: #718096;
  font-size: 0.875rem;
}

.cliente-correo {
  color: #4299e1;
  margin: 0.25rem 0;
}

.cliente-direccion {
  color: #4a5568;
  margin: 0.25rem 0;
}

.cliente-fecha {
  color: #718096;
  font-size: 0.875rem;
  margin: 0.25rem 0;
}

.cliente-acciones {
  display: flex;
  gap: 0.5rem;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #718096;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  background: #f7fafc;
  border-radius: 8px;
  color: #718096;
}

.spinner {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(255,255,255,0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>