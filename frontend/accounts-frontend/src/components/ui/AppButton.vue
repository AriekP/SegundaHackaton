<template>
  <button
    :type="type"
    :class="['btn', variant, size]"
    :disabled="loading || disabled"
    @click="$emit('click')"
  >
    <span v-if="loading" class="loading-spinner">
      <i class="fas fa-spinner fa-spin"></i>
    </span>
    <span v-else-if="$slots.default" class="content">
      <slot></slot>
    </span>
  </button>
</template>

<script setup>
defineProps({
  type: {
    type: String,
    default: 'button'
  },
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'success', 'warning', 'danger', 'outline', 'text'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  loading: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  }
});

defineEmits(['click']);
</script>

<style scoped>
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

/* Variantes */
.primary {
  background-color: var(--primary-color);
  color: white;
  border: 1px solid var(--primary-color);
}

.primary:hover:not(:disabled) {
  background-color: var(--primary-dark);
  border-color: var(--primary-dark);
}

.secondary {
  background-color: var(--secondary-color);
  color: white;
  border: 1px solid var(--secondary-color);
}

.secondary:hover:not(:disabled) {
  background-color: var(--secondary-dark);
  border-color: var(--secondary-dark);
}

.success {
  background-color: var(--success-color);
  color: white;
  border: 1px solid var(--success-color);
}

.success:hover:not(:disabled) {
  background-color: var(--success-dark);
  border-color: var(--success-dark);
}

.warning {
  background-color: var(--warning-color);
  color: white;
  border: 1px solid var(--warning-color);
}

.warning:hover:not(:disabled) {
  background-color: var(--warning-dark);
  border-color: var(--warning-dark);
}

.danger {
  background-color: var(--danger-color);
  color: white;
  border: 1px solid var(--danger-color);
}

.danger:hover:not(:disabled) {
  background-color: var(--danger-dark);
  border-color: var(--danger-dark);
}

.outline {
  background-color: transparent;
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
}

.outline:hover:not(:disabled) {
  background-color: rgba(74, 137, 220, 0.1);
}

.text {
  background-color: transparent;
  color: var(--primary-color);
  border: none;
}

.text:hover:not(:disabled) {
  text-decoration: underline;
}

/* Tamaños */
.sm {
  padding: 0.4rem 0.8rem;
  font-size: 0.85rem;
}

.md {
  padding: 0.6rem 1.2rem;
  font-size: 1rem;
}

.lg {
  padding: 0.8rem 1.6rem;
  font-size: 1.1rem;
}

/* Estados */
:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-spinner {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>