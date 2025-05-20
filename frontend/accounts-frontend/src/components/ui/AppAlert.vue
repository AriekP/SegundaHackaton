<template>
  <div v-if="message" class="alert" :class="type">
    <div class="alert-content">
      <i :class="iconClass"></i>
      <span>{{ message }}</span>
    </div>
    <button v-if="dismissible" @click="$emit('dismiss')" class="close-btn">
      <i class="fas fa-times"></i>
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  message: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'info',
    validator: (value) => ['info', 'success', 'warning', 'error'].includes(value)
  },
  dismissible: {
    type: Boolean,
    default: false
  }
});

const iconClass = computed(() => {
  return {
    'info': 'fas fa-info-circle',
    'success': 'fas fa-check-circle',
    'warning': 'fas fa-exclamation-triangle',
    'error': 'fas fa-exclamation-circle'
  }[props.type];
});
</script>

<style scoped>
.alert {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  margin-bottom: 1.5rem;
  border-radius: 6px;
  font-size: 0.95rem;
}

.alert-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.alert i {
  font-size: 1.1rem;
}

.info {
  background-color: #e8f4fd;
  color: #2980b9;
}

.success {
  background-color: #e8f8f0;
  color: #27ae60;
}

.warning {
  background-color: #fef5e7;
  color: #f39c12;
}

.error {
  background-color: #fdecea;
  color: #e74c3c;
}

.close-btn {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  padding: 0.25rem;
  margin-left: 1rem;
}
</style>