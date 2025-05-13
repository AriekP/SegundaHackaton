<template>
  <div class="account-card">
    <div class="account-header">
      <h3>{{ account.numero_cuenta }}</h3>
      <span class="account-type">{{ account.tipo }}</span>
    </div>
    <div class="account-body">
      <p class="account-balance">
        Saldo: <strong>{{ account.saldo }} {{ account.moneda }}</strong>
      </p>
      <p>Estado: <span :class="account.estado.toLowerCase()">{{ account.estado }}</span></p>
    </div>
    <div class="account-actions">
      <RouterLink 
        :to="{ name: 'account-detail', params: { id: account.id } }" 
        class="btn btn-primary"
      >
        Ver Detalle
      </RouterLink>
      <RouterLink 
        :to="{ name: 'account-transactions', params: { id: account.id } }" 
        class="btn btn-secondary"
      >
        Transacciones
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
defineProps({
  account: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.account-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.account-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.account-type {
  background-color: #2c3e50;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

.account-balance {
  font-size: 1.1rem;
  margin: 0.5rem 0;
}

.activa {
  color: green;
  font-weight: bold;
}

.bloqueada {
  color: red;
  font-weight: bold;
}

.account-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  text-decoration: none;
  font-size: 0.9rem;
}

.btn-primary {
  background-color: #3498db;
  color: white;
}

.btn-secondary {
  background-color: #95a5a6;
  color: white;
}
</style>