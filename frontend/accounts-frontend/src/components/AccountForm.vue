<template>
  <form @submit.prevent="handleSubmit" class="account-form">
    <div class="form-group">
      <label for="numero_cuenta">Número de Cuenta</label>
      <input
        type="text"
        id="numero_cuenta"
        v-model="formData.numero_cuenta"
        required
        maxlength="12"
      />
    </div>

    <div class="form-group">
      <label for="cliente_id">ID de Cliente</label>
      <input
        type="number"
        id="cliente_id"
        v-model.number="formData.cliente_id"
        required
      />
    </div>

    <div class="form-group">
      <label for="saldo">Saldo Inicial</label>
      <input
        type="number"
        id="saldo"
        v-model.number="formData.saldo"
        step="0.01"
        min="0"
      />
    </div>

    <div class="form-group">
      <label for="tipo">Tipo de Cuenta</label>
      <select id="tipo" v-model="formData.tipo">
        <option value="AHORRO">Ahorro</option>
        <option value="CORRIENTE">Corriente</option>
      </select>
    </div>

    <div class="form-group">
      <label for="moneda">Moneda</label>
      <select id="moneda" v-model="formData.moneda">
        <option value="BOB">Bolivianos (BOB)</option>
        <option value="USD">Dólares (USD)</option>
      </select>
    </div>

    <div class="form-actions">
      <button type="submit" class="btn btn-primary">
        {{ submitText }}
      </button>
      <button type="button" class="btn btn-secondary" @click="$emit('cancel')">
        Cancelar
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  account: {
    type: Object,
    default: null
  },
  submitText: {
    type: String,
    default: 'Guardar'
  }
})

const emit = defineEmits(['submit', 'cancel'])

const formData = ref({
  numero_cuenta: '',
  cliente_id: null,
  saldo: 0,
  tipo: 'AHORRO',
  moneda: 'BOB',
  estado: 'ACTIVA'
})

watch(() => props.account, (newVal) => {
  if (newVal) {
    formData.value = { ...newVal }
  }
}, { immediate: true })

const handleSubmit = () => {
  emit('submit', formData.value)
}
</script>

<style scoped>
.account-form {
  max-width: 500px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1.5rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
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