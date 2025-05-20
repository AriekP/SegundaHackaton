<template>
  <div class="payment-detail-view">
    <router-link 
      :to="{ name: 'payments' }" 
      class="back-link"
    >
      <i class="fas fa-arrow-left"></i> Volver a pagos
    </router-link>

    <AppAlert 
      v-if="error" 
      :message="error" 
      type="error" 
      @dismiss="error = null"
    />

    <template v-if="loading">
      <div class="skeleton-loader">
        <div class="skeleton-header"></div>
        <div class="skeleton-line"></div>
        <div class="skeleton-line"></div>
        <div class="skeleton-line"></div>
      </div>
    </template>

    <template v-else>
      <div v-if="!payment" class="not-found">
        <i class="fas fa-exclamation-triangle"></i>
        <p>Pago no encontrado</p>
      </div>

      <div v-else class="payment-content">
        <div class="payment-header">
          <h2>Pago #{{ payment.referencia }}</h2>
          <span :class="['payment-status', payment.estado.toLowerCase()]">
            {{ payment.estado }}
          </span>
        </div>

        <div class="payment-info">
          <div class="info-card">
            <h3>Detalles del Pago</h3>
            <div class="info-grid">
              <div>
                <label>Monto</label>
                <p class="amount">{{ formatCurrency(payment.monto) }}</p>
              </div>
              <div>
                <label>Fecha</label>
                <p>{{ formatDate(payment.fecha) }}</p>
              </div>
              <div>
                <label>Servicio</label>
                <p>{{ payment.servicio }}</p>
              </div>
              <div>
                <label>Método</label>
                <p>{{ payment.metodo }}</p>
              </div>
            </div>
          </div>

          <div class="info-card">
            <h3>Información Adicional</h3>
            <p>{{ payment.descripcion || 'Sin descripción adicional' }}</p>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { usePaymentStore } from '@/stores/payments'
import AppAlert from '@/components/ui/AppAlert.vue'

const route = useRoute()
const paymentStore = usePaymentStore()

const { currentPayment: payment, loading, error, fetchPayment } = paymentStore

onMounted(async () => {
  await fetchPayment(route.params.id)
})

const formatCurrency = (value) => {
  return new Intl.NumberFormat('es-BO', {
    style: 'currency',
    currency: 'BOB'
  }).format(value)
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('es-BO', {
    day: '2-digit',
    month: 'long',
    year: 'numeric'
  })
}
</script>

<style scoped>
.payment-detail-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  color: var(--primary-color);
  text-decoration: none;
}

.payment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.payment-status {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.9rem;
}

.payment-status.completado {
  background-color: var(--success-light);
  color: var(--success-dark);
}

.payment-status.pendiente {
  background-color: var(--warning-light);
  color: var(--warning-dark);
}

.payment-status.rechazado {
  background-color: var(--danger-light);
  color: var(--danger-dark);
}

.payment-info {
  display: grid;
  gap: 1.5rem;
}

.info-card {
  padding: 1.5rem;
  background: var(--background-light);
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.info-card h3 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: var(--text-secondary);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
}

.info-grid label {
  display: block;
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin-bottom: 0.25rem;
}

.amount {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--primary-dark);
}

.not-found {
  text-align: center;
  padding: 3rem;
  color: var(--danger-dark);
}

.not-found i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.skeleton-loader {
  display: grid;
  gap: 1.5rem;
}

.skeleton-header {
  height: 40px;
  width: 60%;
  background: var(--background-light);
  border-radius: 4px;
  margin-bottom: 2rem;
}

.skeleton-line {
  height: 20px;
  background: var(--background-light);
  border-radius: 4px;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .payment-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>