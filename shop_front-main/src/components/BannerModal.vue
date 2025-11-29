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
/* simple styling — adjust as needed */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-card {
  background: #fff;
  padding: 22px;
  border-radius: 12px;
  width: 700px;
}

.banner-table {
  width: 100%;
  margin-bottom: 16px;
}

.btn-add, .btn-save, .btn-cancel {
  margin-top: 12px;
}
</style>
