<template>
  <div class="not-found-view">
    <div class="content">
      <h1>404</h1>
      <p>Página no encontrada</p>
      <p class="description">La página que estás buscando no existe o ha sido movida.</p>
      <router-link to="/" class="home-link">
        <AppButton variant="primary">
          <i class="fas fa-home"></i> Volver al inicio
        </AppButton>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import AppButton from '@/components/ui/AppButton.vue';
</script>

<style scoped>
.not-found-view {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: var(--background-light);
}

.content {
  text-align: center;
  max-width: 500px;
  padding: 2rem;
}

h1 {
  font-size: 5rem;
  margin-bottom: 1rem;
  color: var(--primary-color);
}

p {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.description {
  font-size: 1rem;
  margin-bottom: 2rem;
  color: var(--text-secondary);
}

.home-link {
  text-decoration: none;
}
</style>