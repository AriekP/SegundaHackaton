<template>
  <div class="login-container">
    <h2>Iniciar sesión</h2>

    <form @submit.prevent="handleLogin">
      <input v-model="form.username" placeholder="Correo" required />
      <input v-model="form.password" type="password" placeholder="Contraseña" required />
      <button type="submit">Entrar</button>
    </form>

    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="perfil">Bienvenido, {{ perfil.correo }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { login, getPerfil } from '../api/auth'

const form = ref({
  username: '',
  password: '',
})

const error = ref('')
const perfil = ref(null)

const handleLogin = async () => {
  try {
    const { access_token } = await login(form.value)
    localStorage.setItem('token', access_token) // 👈
    const userData = await getPerfil(access_token)
    perfil.value = userData
    error.value = ''
  } catch (err) {
    error.value = 'Credenciales inválidas'
  }
}

</script>

<style scoped>
.login-container {
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
  background: #4299e1;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background: #2b6cb0;
}

.error {
  color: red;
  margin-top: 1rem;
}
</style>
