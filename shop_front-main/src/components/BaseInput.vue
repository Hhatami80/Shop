<template>
  <div class="base-input">
    <label v-if="label">{{ label }}</label>

    <div class="input-wrapper" :class="{ disabled }">
      <input
        :type="type"
        :placeholder="placeholder"
        :value="displayValue"
        @input="onInput($event.target.value)"
        :disabled="disabled"
      />
      <span v-if="unit" class="input-unit">{{ unit }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: [String, Number],
  label: String,
  placeholder: String,
  type: { type: String, default: 'text' },
  unit: String,       
  disabled: Boolean,
})

const emit = defineEmits(['update:modelValue'])

const displayValue = ref('')

watch(() => props.modelValue, val => {
  displayValue.value = formatNumber(val)
})

function onInput(val) {
  const numericValue = val.replace(/[^0-9]/g, '')
  const number = numericValue ? Number(numericValue) : ''
  emit('update:modelValue', number)
  displayValue.value = formatNumber(number)
}

function formatNumber(val) {
  if (!val && val !== 0) return ''
  return Number(val).toLocaleString('fa-IR')
}
</script>

<style scoped>
.base-input {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

label {
  font-weight: 600;
  font-size: 0.9rem;
  color: #333;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-wrapper input {
  width: 100%;
  padding: 10px 45px 10px 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 0.95rem;
  outline: none;
  background: white;
  transition: border-color 0.2s ease;
}

.input-wrapper input:focus {
  border-color: #f9c710;
}

.input-unit {
  position: absolute;
  right: 12px;
  font-size: 0.95rem;
  color: #777;
  pointer-events: none;
}

.input-wrapper.disabled {
  opacity: 0.6;
  pointer-events: none;
}
</style>
