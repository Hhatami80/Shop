<template>
  <div class="base-select">
    <label v-if="label">{{ label }}</label>

    <div class="select-wrapper" :class="{ disabled }">
      <select
        v-model="localValue"
        :disabled="disabled"
        @change="$emit('change', localValue)"
      >
        <option disabled value="">{{ placeholder }}</option>
        <option
          v-for="option in options"
          :key="option[valueKey]"
          :value="option[valueKey]"
        >
          {{ option[labelKey] }}
        </option>
      </select>
      <i class="fas fa-chevron-down"></i>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  modelValue: [String, Number],
  options: { type: Array, default: () => [] },
  label: String,
  placeholder: { type: String, default: "انتخاب کنید" },
  valueKey: { type: String, default: "id" },
  labelKey: { type: String, default: "name" },
  disabled: Boolean,
});

const emit = defineEmits(["update:modelValue", "change"]);

const localValue = ref(props.modelValue);

watch(
  () => props.modelValue,
  (val) => (localValue.value = val)
);

watch(localValue, (val) => emit("update:modelValue", val));
</script>

<style scoped>
.base-select {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

label {
  font-weight: 600;
  font-size: 0.9rem;
  color: #333;
}

.select-wrapper {
  position: relative;
}

.select-wrapper select {
  width: 100%;
  padding: 10px 35px 10px 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 0.9rem;
  outline: none;
  background: white;
  appearance: none;
  transition: border-color 0.2s ease;
}

.select-wrapper select:focus {
  border-color: #f9c710;
}

.select-wrapper i {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #777;
  pointer-events: none;
}

.select-wrapper.disabled {
  opacity: 0.6;
  pointer-events: none;
}
</style>
