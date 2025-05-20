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
        placeholder="Ej: 1234567890"
        :disabled="!!account"
      >
    </div>

    <div class="form-row">
      <div class="form-group">
        <label for="tipo">Tipo de Cuenta</label>
        <select id="tipo" v-model="formData.tipo" required>
          <option value="AHORRO">Ahorro</option>
          <option value="CORRIENTE">Corriente</option>
        </select>
      </div>

      <div class="form-group">
        <label for="moneda">Moneda</label>
        <select id="moneda" v-model="formData.moneda" required>
          <option value="BOB">Bolivianos (BOB)</option>
          <option value="USD">Dólares (USD)</option>
        </select>
      </div>
    </div>

    <div class="form-group">
      <label for="saldo">Saldo Inicial</label>
      <input
        type="number"
        id="saldo"
        v-model.number="formData.saldo"
        step="0.01"
        min="0"
        placeholder="0.00"
        :disabled="!!account"
      >
    </div>

    <div class="form-actions">
      <AppButton type="button" variant="secondary" @click="$emit('cancel')">
        Cancelar
      </AppButton>
      <AppButton type="submit" variant="primary" :loading="loading">
        {{ account ? 'Actualizar' : 'Crear' }} Cuenta
      </AppButton>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </form>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { createAccount, updateAccount, getAccount } from '@/api/accounts'
import AppButton from '@/components/ui/AppButton.vue'

const props = defineProps({
  accountId: {
    type: Number,
    default: null
  },
  clienteId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['success', 'cancel'])

const loading = ref(false)
const error = ref(null)
const formData = ref({
  cliente_id: props.clienteId,
  numero_cuenta: '',
  tipo: 'AHORRO',
  moneda: 'BOB',
  saldo: 0
})

// Cargar datos de la cuenta si estamos editando
onMounted(async () => {
  if (props.accountId) {
    loading.value = true
    try {
      const account = await getAccount(props.accountId)
      formData.value = {
        cliente_id: account.cliente_id,
        numero_cuenta: account.numero_cuenta,
        tipo: account.tipo,
        moneda: account.moneda,
        saldo: account.saldo
      }
    } catch (err) {
      error.value = 'Error al cargar la cuenta'
      console.error(err)
    } finally {
      loading.value = false
    }
  }
})

const handleSubmit = async () => {
  loading.value = true
  error.value = null
  
  try {
    if (props.accountId) {
      // Actualizar cuenta existente
      await updateAccount(props.accountId, formData.value)
    } else {
      // Crear nueva cuenta
      await createAccount(formData.value)
    }
    emit('success')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al procesar la solicitud'
    console.error(err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.account-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-width: 600px;
  margin: 0 auto;
  padding: 1.5rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-row {
  display: flex;
  gap: 1rem;
}

.form-row .form-group {
  flex: 1;
}

label {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--text-primary);
}

input, select {
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 1rem;
  background: white;
}

input:disabled, select:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

input:focus, select:focus {
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

.error-message {
  color: #d32f2f;
  background: #fde8e8;
  padding: 0.75rem;
  border-radius: 4px;
  margin-top: 1rem;
}

/* Responsive design */
@media (max-width: 600px) {
  .form-row {
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .account-form {
    padding: 1rem;
  }
}
</style>