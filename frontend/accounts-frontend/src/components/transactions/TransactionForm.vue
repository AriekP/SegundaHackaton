<template>
  <form @submit.prevent="handleSubmit" class="transaction-form">
    <div v-if="!type" class="form-group">
      <label>Tipo de Transacción</label>
      <div class="transaction-type-selector">
        <label class="type-option">
          <input 
            type="radio" 
            v-model="formData.tipo" 
            value="DEPOSITO"
            required
          >
          <div class="option-content deposito">
            <i class="fas fa-arrow-down"></i>
            <span>Depósito</span>
          </div>
        </label>
        <label class="type-option">
          <input 
            type="radio" 
            v-model="formData.tipo" 
            value="RETIRO"
            required
          >
          <div class="option-content retiro">
            <i class="fas fa-arrow-up"></i>
            <span>Retiro</span>
          </div>
        </label>
      </div>
    </div>
    <div v-else class="transaction-type-display">
      <div :class="['type-badge', type.toLowerCase()]">
        <i :class="type === 'DEPOSITO' ? 'fas fa-arrow-down' : 'fas fa-arrow-up'"></i>
        <span>{{ type === 'DEPOSITO' ? 'Depósito' : 'Retiro' }}</span>
      </div>
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
        placeholder="0.00"
      >
    </div>

    <div class="form-group">
      <label for="descripcion">Descripción</label>
      <input
        type="text"
        id="descripcion"
        v-model="formData.descripcion"
        placeholder="Ej: Pago de servicios"
      >
    </div>

    <div class="form-group">
      <label for="referencia">Referencia (Opcional)</label>
      <input
        type="text"
        id="referencia"
        v-model="formData.referencia"
        placeholder="Ej: Factura 123"
      >
    </div>

    <div class="form-actions">
      <AppButton type="button" variant="secondary" @click="$emit('cancel')">
        Cancelar
      </AppButton>
      <AppButton type="submit" variant="primary">
        Confirmar Transacción
      </AppButton>
    </div>
  </form>
</template>

<script setup>
import { ref, watch } from 'vue';
import AppButton from '@/components/ui/AppButton.vue';

const props = defineProps({
  accountId: {
    type: [Number, String],
    required: true
  },
  type: {
    type: String,
    default: null
  }
});

const emit = defineEmits(['submit', 'cancel']);

const formData = ref({
  cuenta_id: props.accountId,
  tipo: props.type || 'DEPOSITO',
  monto: null,
  descripcion: '',
  referencia: ''
});

watch(() => props.accountId, (newVal) => {
  formData.value.cuenta_id = newVal;
});

watch(() => props.type, (newVal) => {
  if (newVal) {
    formData.value.tipo = newVal;
  }
});

const handleSubmit = () => {
  emit('submit', formData.value);
};
</script>

<style scoped>
.transaction-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.transaction-type-selector {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
}

.type-option {
  flex: 1;
}

.type-option input {
  display: none;
}

.option-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.option-content i {
  font-size: 1.5rem;
}

.option-content.deposito i {
  color: var(--success-color);
}

.option-content.retiro i {
  color: var(--warning-color);
}

.type-option input:checked + .option-content {
  border-color: var(--primary-color);
  background-color: rgba(74, 137, 220, 0.05);
}

.transaction-type-display {
  margin-bottom: 1rem;
}

.type-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: bold;
}

.type-badge.deposito {
  background-color: #e8f8f0;
  color: var(--success-color);
}

.type-badge.retiro {
  background-color: #fef5e7;
  color: var(--warning-color);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--text-primary);
}

input {
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 1rem;
}

input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(74, 137, 220, 0.2);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}
</style>