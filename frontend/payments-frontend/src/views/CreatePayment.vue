<template>
  <div>
    <h1>Nuevo Pago</h1>
    <form @submit.prevent="submitPayment">
      <div>
        <label>Cuenta ID:</label>
        <input v-model="formData.cuenta_id" type="number" required />
      </div>
      <div>
        <label>Proveedor ID:</label>
        <input v-model="formData.proveedor_id" type="number" required />
      </div>
      <div>
        <label>Monto:</label>
        <input v-model="formData.monto" type="number" step="0.01" required />
      </div>
      <div>
        <label>Referencia:</label>
        <input v-model="formData.referencia" type="text" required />
      </div>
      <button type="submit" :disabled="loading">
        {{ loading ? 'Procesando...' : 'Realizar Pago' }}
      </button>
      <div v-if="error" class="error">{{ error }}</div>
    </form>
  </div>
</template>

<script>
import { usePaymentStore } from '../stores/payments'
import { reactive } from 'vue'
import { useRouter } from 'vue-router'

export default {
  setup() {
    const paymentStore = usePaymentStore()
    const router = useRouter()
    
    const formData = reactive({
      cuenta_id: '',
      proveedor_id: '',
      monto: '',
      referencia: ''
    })

    const submitPayment = async () => {
      try {
        await paymentStore.makePayment({
          ...formData,
          monto: parseFloat(formData.monto)
        })
        router.push('/')
      } catch (error) {
        console.error(error)
      }
    }

    return {
      formData,
      submitPayment,
      loading: paymentStore.loading,
      error: paymentStore.error
    }
  }
}
</script>

<style>
form div {
  margin-bottom: 10px;
}
label {
  display: inline-block;
  width: 100px;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>