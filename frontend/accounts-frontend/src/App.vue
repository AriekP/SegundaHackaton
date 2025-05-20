<template>
  <div class="app-container">
    <header class="app-header">
      <h1>Banca en Línea</h1>
      <nav class="app-nav">
        <RouterLink to="/">Cuentas</RouterLink>
        <RouterLink to="/transactions">Transacciones</RouterLink>
        <RouterLink to="/payments">Pagos</RouterLink>
        <RouterLink to="/providers">Proveedores</RouterLink>
      </nav>
    </header>
    
    <main class="app-main">
      <RouterView v-slot="{ Component }">
        <Transition name="fade" mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script> 

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  background-color: #2c3e50;
  color: white;
  padding: 1rem;
  text-align: center;
}

.app-nav {
  display: flex;
  gap: 1rem;
  justify-content: center;
  padding: 0.5rem;
  background-color: #34495e;
}

.app-nav a {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.app-nav a:hover {
  background-color: #3d566e;
}

.app-nav a.router-link-active {
  font-weight: bold;
  background-color: #3d566e;
}

.app-main {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.app-footer {
  background-color: #2c3e50;
  color: white;
  padding: 1rem;
  text-align: center;
  margin-top: auto;
}

/* Transiciones */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .app-nav {
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
  }
  
  .app-main {
    padding: 1rem;
  }
}
</style>