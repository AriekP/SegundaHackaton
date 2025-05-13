<template>
  <div class="not-found-view">
    <h2>404 - Página no encontrada</h2>
    <p>La página que estás buscando no existe.</p>
    <RouterLink to="/" class="home-link">Volver al inicio</RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.not-found-view {
  text-align: center;
  padding: 2rem;
}

.home-link {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background-color: #3498db;
  color: white;
  text-decoration: none;
  border-radius: 4px;
}
</style>