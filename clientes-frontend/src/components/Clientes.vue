<template>
  <div>
    <form @submit.prevent="crearCliente">
      <input v-model="form.nombre" placeholder="Nombre" required />
      <input v-model="form.correo" placeholder="Correo" required />
      <input v-model="form.telefono" placeholder="Teléfono" />
      <input v-model="form.ci" placeholder="CI" required />
      <input v-model="form.fecha_nac" type="date" required />
      <input v-model="form.direccion" placeholder="Dirección" />
      <button type="submit">Agregar</button>
    </form>

    <ul>
      <li v-for="cliente in clientes" :key="cliente.id">
        {{ cliente.nombre }} - {{ cliente.correo }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const clientes = ref([])
const form = ref({
  nombre: '',
  correo: '',
  telefono: '',
  ci: '',
  fecha_nac: '',
  direccion: ''
})

const cargarClientes = async () => {
  const res = await api.get('/')
  clientes.value = res.data
}

const crearCliente = async () => {
  await api.post('/', form.value)
  await cargarClientes()
}

onMounted(cargarClientes)
</script>
