<template>
  <nav class="navbar">
    <h1>BancoApp</h1>
    <ul>
      <li v-if="!perfil">
        <router-link to="/login">Login</router-link>
      </li>
      <li v-if="!perfil">
        <router-link to="/signup">Registrarse</router-link>
      </li>
      <li v-if="perfil">
        <span>{{ perfil.correo }}</span>
      </li>
      <li v-if="perfil">
        <button @click="logout">Logout</button>
      </li>
      <li v-if="perfil">
  <router-link to="/dashboard">Dashboard</router-link>
</li>

    </ul>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getPerfil } from '../api/auth'

const perfil = ref(null)

const token = localStorage.getItem('token')
if (token) {
  getPerfil(token)
    .then((data) => (perfil.value = data))
    .catch(() => localStorage.removeItem('token'))
}

const logout = () => {
  localStorage.removeItem('token')
  location.reload()
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #2d3748;
  padding: 1rem 2rem;
  color: white;
}

.navbar ul {
  list-style: none;
  display: flex;
  gap: 1rem;
  align-items: center;
  margin: 0;
  padding: 0;
}

.navbar a {
  color: white;
  text-decoration: none;
}

button {
  background: #e53e3e;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}
</style>
