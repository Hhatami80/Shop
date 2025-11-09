<template>
  <div v-if="modelValue" class="modal-overlay">
    <div class="modal-container">
      <h3 class="text-center">ویرایش دسته‌بندی</h3>
      <div v-if="previewImage" class="image-preview">
        <img :src="previewImage" alt="پیش‌نمایش تصویر" width="100" />
      </div>

      <form @submit.prevent="submitEdit" enctype="multipart/form-data">
        <input v-model="editedTitle" placeholder="عنوان جدید دسته" required />

        <input type="file" @change="handleImageChange" />

        <div class="modal-actions">
          <button type="submit">ذخیره تغییرات</button>
          <button type="button" @click="$emit('update:modelValue', false)">انصراف</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { computed } from 'vue'

const props = defineProps({
  modelValue: Boolean,
  category: Object,
})

const emit = defineEmits(['update:modelValue', 'save'])

const editedTitle = ref('')
const imageFile = ref(null)
const previewImage = ref(null)

watch(
  () => props.category,
  (cat) => {
    if (cat) {
      editedTitle.value = cat.title
      previewImage.value = cat.image || null
    }
  },
  { immediate: true }
)

const handleImageChange = (e) => {
  imageFile.value = e.target.files[0]
  if (imageFile.value) {
    previewImage.value = URL.createObjectURL(imageFile.value)
  }
}

const submitEdit = () => {
  const formData = new FormData()
  formData.append('title', editedTitle.value)
  formData.append('id', props.category.id)

  if (imageFile.value) {
    formData.append('image', imageFile.value)
  }

  emit('save', { id: props.category.id, formData })
  emit('update:modelValue', false)
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-container {
  background: #fff;
  padding: 1.5rem;
  border-radius: 12px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 0 20px rgba(249, 199, 16, 0.2);
  
  direction: rtl;
}

.modal-container h3 {
  margin-bottom: 1rem;
  text-align: center;
  color: #222;
  border-bottom: 2px solid #f9c710;
  padding-bottom: 6px;
}

input {
  width: 90%;
  padding: 0.6rem 0.8rem;
  border: 1.5px solid #ccc;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-size: 14px;
  background-color: #f9f9f9;
  color: #111;
  transition: 0.3s;
}

input:focus {
  border-color: #f9c710;
  box-shadow: 0 0 8px rgba(249, 199, 16, 0.3);
  outline: none;
}

.image-preview {
  margin-bottom: 1rem;
  text-align: center;
}

.image-preview img {
  max-width: 120px;
  border-radius: 8px;
  box-shadow: 0 0 8px rgba(249, 199, 16, 0.3);
  border: 1px solid #ddd;
}

.modal-actions {
  display: flex;
  justify-content: center; 
  gap: 0.5rem;
}

.modal-actions button {
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.3s;
  border: 1.5px solid transparent;
}

.modal-actions button:first-child {
  background-color: #f9c710;
  color: #000;
  border-color: #f9c710;
}

.modal-actions button:first-child:hover {
  background-color: #d4b006;
  color: #111;
  box-shadow: 0 0 12px rgba(212, 176, 6, 0.4);
}

.modal-actions button:last-child {
  background-color: #fff;
  color: #888;
  border-color: #ccc;
}

.modal-actions button:last-child:hover {
  background-color: #f9f9f9;
  color: #444;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
}
</style>
