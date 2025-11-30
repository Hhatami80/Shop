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
          <tr v-for="(item, index) in localBanners" :key="index">
            <td>
              <input
                type="file"
                class="form-input"
                @change="e => handleFileUpload(e, index)"
              />
            </td>

            <td>
              <input
                type="text"
                class="form-input"
                v-model="item.text"
                placeholder="متن بنر"
              />
            </td>

            <td>
              <button class="btn-delete" @click="removeBanner(index)">
                حذف
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <button class="btn-add-row" @click="addBanner">+ افزودن ردیف</button>

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

const emit = defineEmits(['update:modelValue', 'update', 'refresh'])

const localBanners = ref([])

watch(
  () => props.banners,
  (val) => {
    localBanners.value = JSON.parse(JSON.stringify(val || []))
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
  emit('refresh')
}
</script>

<style scoped>
.banner-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.banner-table th,
.banner-table td {
  padding: 10px;
  border-bottom: 1px solid #eaeaea;
}

.btn-add-row {
  background-color: #007bff;
  color: white;
  padding: 8px 12px;
  border-radius: 6px;
  margin-bottom: 15px;
}

.btn-add-row:hover {
  background-color: #0069d9;
}

.form-input {
  width: 100%;
  padding: 8px 10px;
  border: 1px solid #dcdcdc;
  border-radius: 6px;
}
</style>
