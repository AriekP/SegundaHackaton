<template>
  <div class="registro-container">
    <h2>Registrarse</h2>

    <form @submit.prevent="registrarse">
      <input v-model="form.correo" type="email" placeholder="Correo electrónico" required />
      <input v-model="form.password" type="password" placeholder="Contraseña" required />
      <input v-model="form.cliente_id" type="number" placeholder="ID de cliente (opcional)" />
      <button type="submit">Crear cuenta</button>
    </form>

    <p v-if="mensaje" class="mensaje">{{ mensaje }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { signup } from '../api/auth'

const form = ref({
  correo: '',
  password: '',
  cliente_id: null,
})

const mensaje = ref('')

const registrarse = async () => {
  try {
    await signup(form.value)
    mensaje.value = 'Usuario creado correctamente. Ahora puedes iniciar sesión.'
    form.value = { correo: '', password: '', cliente_id: null }
  } catch (error) {
    console.error(error)
    mensaje.value = 'Error al registrarse. Intenta con otro correo.'
  }
}
</script>

<style scoped>
.registro-container {
  max-width: 400px;
  margin: auto;
  padding: 2rem;
  background: #f9f9f9;
  border-radius: 8px;
  font-family: sans-serif;
}

input {
  display: block;
  margin: 1rem 0;
  padding: 0.75rem;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 0.75rem;
  background: #48bb78;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background: #38a169;
}

.mensaje {
  margin-top: 1rem;
  color: #2d3748;
}
</style>
