<template>
  <div class="base-select">
    <label v-if="label">{{ label }}</label>

    <div class="custom-select" @click="toggle">
      <span>{{ selectedLabel || placeholder }}</span>
      <i class="fas fa-chevron-down"></i>
    </div>

    <ul v-if="open" class="dropdown-list">
      <li
        v-for="option in options"
        :key="option[valueKey]"
        @click="select(option)"
        class="dropdown-item"
      >
        {{ option[labelKey] }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  modelValue: [String, Number],
  options: Array,
  label: String,
  placeholder: { type: String, default: 'انتخاب کنید' },
  valueKey: { type: String, default: 'id' },
  labelKey: { type: String, default: 'name' }
})

const emit = defineEmits(['update:modelValue', 'change'])

const open = ref(false)
const toggle = () => (open.value = !open.value)
const select = (option) => {
  emit('update:modelValue', option[props.valueKey])
  emit('change', option)
  open.value = false
}

const selectedLabel = computed(() => {
  const item = props.options.find(o => o[props.valueKey] === props.modelValue)
  return item ? item[props.labelKey] : ''
})
</script>

<style scoped>
.base-select {
  position: relative;
  display: inline-block;
  width: 100%;
}

.custom-select {
  padding: 10px 35px 10px 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  cursor: pointer;
  background: white;
  position: relative;
}

.custom-select i {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #777;
}

.dropdown-list {
  position: absolute;
  width: 100%;
  margin-top: 4px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background: white;
  list-style: none;
  padding: 0;
  z-index: 10;
  overflow-y: auto;
  max-height: 180px; 
}

.dropdown-item {
  padding: 10px;
  cursor: pointer;
}

.dropdown-item:hover {
  background: #f5f5f5;
}
</style>
