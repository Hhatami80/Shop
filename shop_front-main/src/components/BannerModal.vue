<template>
  <div v-if="modelValue" class="modal-backdrop">
    <div class="modal-card">

      <h3 class="modal-title">افزودن بنرها</h3>

      <table class="banner-table">
        <thead>
          <tr>
            <th>فایل بنر</th>
            <th>متن</th>
            <th></th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="(item, index) in localBanners"
            :key="index"
          >
            <td>
              <input
                type="file"
                @change="e => handleFileUpload(e, index)"
              />
            </td>
            <td>
              <input
                type="text"
                v-model="item.text"
                placeholder="متن بنر"
                class="form-input"
              />
            </td>
            <td>
              <button
                class="btn-delete"
                @click="removeBanner(index)"
              >حذف</button>
            </td>
          </tr>
        </tbody>
      </table>

      <button class="btn-add" @click="addBanner">
        + افزودن ردیف
      </button>

      <div class="modal-actions">
        <button class="btn-cancel" @click="$emit('update:modelValue', false)">
          لغو
        </button>
        <button class="btn-save" @click="saveChanges">
          ذخیره
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: Boolean,
  banners: Array
})

const emit = defineEmits(['update:modelValue', 'update'])

const localBanners = ref([])

watch(
  () => props.banners,
  (val) => {
    localBanners.value = JSON.parse(JSON.stringify(val))
  },
  { immediate: true }
)

const addBanner = () => {
  localBanners.value.push({ file: null, text: '' })
}

const removeBanner = (index) => {
  localBanners.value.splice(index, 1)
}

const handleFileUpload = (e, index) => {
  localBanners.value[index].file = e.target.files[0]
}

const saveChanges = () => {
  emit('update', localBanners.value)
  emit('update:modelValue', false)
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
  font-family: 'Vazirmatn', sans-serif;
}

.modal-card {
  background-color: #fff;
  padding: 25px;
  border-radius: 12px;
  width: 700px;
  max-width: 95%;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #34495e;
  margin-bottom: 15px;
  text-align: center;
}

.banner-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-bottom: 15px;
}

.banner-table th,
.banner-table td {
  padding: 10px 12px;
  text-align: center;
  border-bottom: 1px solid #e9ecef;
  font-size: 0.95rem;
  color: #333;
}

.banner-table th {
  font-weight: 600;
  background-color: #f8f9fa;
}

.banner-table input[type="file"] {
  padding: 6px;
}

.form-input {
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid #e9ecef;
  width: 100%;
  font-size: 0.95rem;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.form-input:focus {
  border-color: #ffd700;
  box-shadow: 0 0 5px rgba(255, 215, 0, 0.5);
  outline: none;
}

.btn-add {
  padding: 10px 20px;
  background-color: #ffd700;
  color: #333;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.3s;
  align-self: flex-start;
}

.btn-add:hover {
  background-color: #e6c200;
}

.btn-delete {
  padding: 6px 12px;
  background-color: #dc3545;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: 0.3s;
}

.btn-delete:hover {
  background-color: #c82333;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 10px;
}

.btn-save {
  padding: 10px 20px;
  background-color: #28a745;
  color: #fff;
  border-radius: 8px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: 0.3s;
}

.btn-save:hover {
  background-color: #218838;
}

.btn-cancel {
  padding: 10px 20px;
  background-color: #ccc;
  color: #333;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: 0.3s;
}

.btn-cancel:hover {
  background-color: #b3b3b3;
}
</style>

