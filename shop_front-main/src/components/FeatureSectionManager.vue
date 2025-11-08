<template>
  <div class="admin-banner-right">
    <h2>مدیریت بنر اصلی</h2>

    <div class="form-group">
      <label>عنوان:</label>
      <input v-model="form.title" type="text" placeholder="عنوان را وارد کنید..." />
    </div>

    <div class="form-group">
      <label>زیرعنوان:</label>
      <input v-model="form.subtitle" type="text" placeholder="زیرعنوان را وارد کنید..." />
    </div>

    <div class="form-group">
      <label>انتخاب تصویر:</label>
      <input type="file" @change="onFileChange" accept="image/*" />
    </div>

    <div v-if="previewImage" class="image-preview">
      <img :src="previewImage" alt="پیش‌نمایش تصویر" />
    </div>

    <button @click="save" :disabled="loading">
      <span v-if="loading" class="spinner"></span>
      {{ loading ? 'در حال ذخیره...' : 'ذخیره تغییرات' }}
    </button>

  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useFeatureSectionStore } from '@/stores/FeatureSectionStore'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

const store = useFeatureSectionStore()

const form = ref({
  title: '',
  subtitle: '',
  image: '',
})

const previewImage = ref(null)
const loading = ref(false)

const selectedFile = ref(null)

watch(
  () => store.featureSection,
  (newVal) => {
    if (newVal?.banner?.length) {
      form.value = { ...newVal.banner[0] }
      previewImage.value = form.value.image
    }
  },
  { immediate: true }
)

onMounted(() => {
  store.getFeatureSection()
})

function onFileChange(event) {
  const file = event.target.files[0]
  if (!file) return

  const maxWidth = 1000
  const maxHeight = 400
  const minWidth = 1000
  const minHeight = 400

  const img = new Image()
  img.onload = () => {
    if (img.width > maxWidth || img.height > maxHeight) {
      toast.error(`عرض تصویر نباید بیشتر از ${maxWidth}px و ارتفاع بیشتر از ${maxHeight}px باشد.`)
      selectedFile.value = null
      previewImage.value = null
      return
    }
    if (img.width < minWidth || img.height < minHeight) {
      toast.error(`عرض تصویر نباید کمتر از ${minWidth}px و ارتفاع کمتر از ${minHeight}px باشد.`)
      selectedFile.value = null
      previewImage.value = null
      return
    }

    selectedFile.value = file
    previewImage.value = URL.createObjectURL(file)
  }

  img.src = URL.createObjectURL(file)
}


async function save() {
  loading.value = true

  try {
    const formData = new FormData()
    formData.append('title', form.value.title)
    formData.append('subtitle', form.value.subtitle)

    if (selectedFile.value) {
      formData.append('image', selectedFile.value)
    }

    await store.updateMainBanner(formData)
    toast.success('بنر با موفقیت ذخیره شد ')
  } catch (err) {
    toast.error(store.error || err.message || 'خطا در ذخیره‌سازی ')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.admin-banner-right {
  --gold-primary: #ffd700;
  --gold-hover: #E6C200;
  --text-dark: #34495e;
  --text-light: #555;
  --border-light: #e9ecef;
  --bg-form: #fcfcfc;
  --shadow-light: rgba(0, 0, 0, 0.08);

  max-width: 450px;
  margin: 40px auto;
  direction: rtl;
  font-family: 'Vazirmatn', sans-serif;
  background: #fff;
  padding: 30px 35px;
  border-radius: 12px;
  box-shadow: 0 8px 25px var(--shadow-light);
  color: var(--text-dark);
  border: 1px solid var(--border-light);
  transition: box-shadow 0.3s ease;
}

h2 {
  text-align: right;
  margin-bottom: 25px;
  color: var(--text-dark);
  font-weight: 800;
  font-size: 2rem;
  border-bottom: 2px solid var(--gold-primary);
  padding-bottom: 10px;
}

.form-group {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 8px;
  font-weight: 600;
  color: var(--text-dark);
  font-size: 16px;
}

input[type='text'],
input[type='number'] {
  padding: 12px 15px;
  font-size: 15px;
  border-radius: 8px;
  border: 1px solid var(--border-light);
  background-color: var(--bg-form);
  color: var(--text-dark);
  transition: border-color 0.3s ease, background-color 0.3s ease, box-shadow 0.3s ease;
  outline: none;
  font-family: inherit;
}
input[type='text']::placeholder,
input[type='number']::placeholder {
  color: #aaa;
  font-style: italic;
}
input[type='text']:focus,
input[type='number']:focus {
  border-color: var(--gold-primary);
  background-color: #fff;
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.3); 
}
input[type='file'] {
  margin-top: 5px;
  cursor: pointer;
  padding: 10px 0;
  border: 1px dashed var(--border-light);
  border-radius: 8px;
  color: var(--text-light);
  background-color: var(--bg-form);
}
input[type='file']::-webkit-file-upload-button {
  background-color: var(--gold-primary);
  color: var(--text-dark);
  padding: 8px 15px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  margin-left: 10px;
  transition: background-color 0.3s;
}

.image-preview {
  margin: 25px 0;
  padding: 15px;
  background-color: var(--bg-form);
  border-radius: 12px;
  text-align: center;
  border: 1px solid var(--border-light);
}
.image-preview img {
  max-width: 100%;
  max-height: 200px;
  border-radius: 8px;
  object-fit: contain;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease;
}
.image-preview img:hover {
  transform: scale(1.03);
}

button {
  width: 100%;
  background-color: var(--gold-primary);
  border: none;
  padding: 15px 0;
  font-size: 17px;
  font-weight: 700;
  color: var(--text-dark);
  border-radius: 10px;
  cursor: pointer;
  box-shadow: 0 5px 15px rgba(255, 215, 0, 0.4);
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}
button:hover:not(:disabled) {
  background-color: var(--gold-hover);
  box-shadow: 0 8px 20px rgba(230, 194, 0, 0.6);
}

button:disabled {
  background-color: #bfa600;
  cursor: not-allowed;
  box-shadow: none;
  opacity: 0.7;
}
.error {
  margin-top: 18px;
  padding: 12px 15px;
  background-color: #fceaea;
  border-radius: 8px;
  color: #b00020;
  font-weight: 600;
  text-align: center;
  box-shadow: 0 2px 8px rgba(176, 0, 32, 0.2);
}

.success {
  margin-top: 18px;
  padding: 12px 15px;
  background-color: #f7fce7;
  border-radius: 8px;
  color: #7a6f00;
  font-weight: 600;
  text-align: center;
  box-shadow: 0 2px 8px rgba(212, 176, 6, 0.2);
}

.spinner {
  border: 3px solid #f3f3f3;
  border-top: 3px solid var(--text-dark);
  border-radius: 50%;
  width: 18px;
  height: 18px;
  animation: spin 1s linear infinite;
  display: inline-block;
}
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>