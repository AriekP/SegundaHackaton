<template>
  <form @submit.prevent="handleSubmit" class="transaction-form">
    <div class="form-group">
      <label for="tipo">Tipo de Transacción</label>
      <select id="tipo" v-model="formData.tipo" required>
        <option value="DEPOSITO">Depósito</option>
        <option value="RETIRO">Retiro</option>
      </select>
    </div>

    <div class="form-group">
      <label for="monto">Monto</label>
      <input
        type="number"
        id="monto"
        v-model.number="formData.monto"
        step="0.01"
        min="0.01"
        required
      />
    </div>

    <div class="form-group">
      <label for="descripcion">Descripción</label>
      <input
        type="text"
        id="descripcion"
        v-model="formData.descripcion"
      />
    </div>

    <div class="form-group">
      <label for="referencia">Referencia</label>
      <input
        type="text"
        id="referencia"
        v-model="formData.referencia"
      />
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
  accountId: {
    type: Number,
    required: true
  },
  transaction: {
    type: Object,
    default: null
  },
  submitText: {
    type: String,
    default: 'Realizar Transacción'
  }
})

const emit = defineEmits(['submit', 'cancel'])

const formData = ref({
  cuenta_id: props.accountId,
  tipo: 'DEPOSITO',
  monto: 0,
  descripcion: '',
  referencia: ''
})

watch(() => props.transaction, (newVal) => {
  if (newVal) {
    formData.value = { ...newVal }
  }
}, { immediate: true })

const handleSubmit = () => {
  emit('submit', formData.value)
}
</script>

<style scoped>
.transaction-form {
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