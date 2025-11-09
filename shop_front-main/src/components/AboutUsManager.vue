<template>
  <div class="admin-about">
    <h2>مدیریت بخش درباره ما</h2>

    <form @submit.prevent="handleSubmit" class="about-form">
      <div class="form-group">
        <label for="title" class="label-style">عنوان</label>
        <input id="title" type="text" v-model="form.title" class="input-style" required />
      </div>

      <div class="form-group">
        <label for="text" class="label-style">متن</label>
        <textarea id="text" v-model="form.text" rows="8" class="input-style textarea-style" required></textarea>
      </div>

      <div class="form-group image-upload-group">
        <label for="image-file" class="label-style">انتخاب تصویر</label>
        <input id="image-file" type="file" accept="image/*" @change="handleImageUpload" class="file-input-style" />
      </div>

      <button type="submit" class="btn-submit">
        ذخیره تغییرات
      </button>
    </form>

    <div v-if="preview" class="preview-section">
      <h3>پیش‌نمایش (نمای کاربر)</h3>
      <div class="about-us-preview">
        <h4 class="preview-title">{{ form.title || 'عنوان پیش‌فرض' }}</h4>
        <p class="preview-text">{{ form.text || 'متن پیش‌فرض درباره ما...' }}</p>
        <img v-if="form.imageUrl" :src="form.imageUrl" alt="About Preview" class="preview-image" />
        <div v-else class="image-placeholder">بدون تصویر</div>
      </div>
    </div>

    <div v-if="aboutStore.loading" class="status-message loading">در حال ذخیره...</div>
    <div v-if="aboutStore.error" class="status-message error">{{ aboutStore.error }}</div>
  </div>
</template>

<script setup>
import { reactive, watch, ref, onMounted } from 'vue'
import { useAboutUsStore } from '@/stores/useAboutUsStore'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

const aboutStore = useAboutUsStore()

const form = reactive({
  title: '',
  text: '',
  imageFile: null,
  imageUrl: '',
})

const preview = ref(true)

async function initializeForm() {
  await aboutStore.fetchAbout()
  form.title = aboutStore.title
  form.text = aboutStore.text
  form.imageUrl = aboutStore.imageurl
  form.imageFile = null
}

onMounted(() => {
  initializeForm()
})

watch(
  () => [aboutStore.title, aboutStore.text, aboutStore.imageurl],
  ([newTitle, newText, newImageUrl]) => {
    form.title = newTitle
    form.text = newText
    
    if (!form.imageFile) {
      form.imageUrl = newImageUrl
    }
  }
)

function handleImageUpload(e) {
  const file = e.target.files[0]
  if (file) {
    form.imageFile = file
    const reader = new FileReader()
    reader.onload = (event) => {
      form.imageUrl = event.target.result 
    }
    reader.readAsDataURL(file)
  }
}

async function handleSubmit() {
  try {
    
    aboutStore.loading = true; 
    
    await aboutStore.saveAbout({
      title: form.title,
      text: form.text,
      imageFile: form.imageFile,
    })
    
    
    aboutStore.error = null;
    toast.success('اطلاعات با موفقیت ذخیره شد '); 
    await initializeForm() 
    
  } catch(error) {
    toast.error('خطا در ذخیره اطلاعات ');
  } finally {
    aboutStore.loading = false;
  }
}
</script>


<style scoped>

.admin-about {
  padding: 30px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
  direction: rtl;
  
}

h2 {
  font-size: 26px;
  margin-bottom: 25px;
  color: #1a1a1a;
  font-weight: 800;
  border-bottom: 2px solid #F9C710;
  padding-bottom: 8px;
}


.about-form {
    margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
}

.label-style {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 700;
  font-size: 15px;
}

.input-style {
  width: 90%;
  padding: 12px 15px;
  border: 2px solid #eee;
  border-radius: 8px;
  background: #fcfcfc;
  color: #1a1a1a;
  transition: all 0.3s ease;
  font-size: 15px;
}

.input-style:focus {
  border-color: #F9C710;
  box-shadow: 0 0 0 4px rgba(249, 199, 16, 0.2);
  outline: none;
  background: #fff;
}

.textarea-style {
  resize: vertical;
  min-height: 150px;
}

.file-input-style {
  padding: 8px;
  border: 1px dashed #F9C710;
  background-color: #fffaf0;
  cursor: pointer;
}


.btn-submit {
  background: #F9C710; 
  color: #1a1a1a;
  padding: 12px 30px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 700;
  font-size: 16px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(249, 199, 16, 0.4);
}
.btn-submit:hover {
  background: #e5c100; 
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(249, 199, 16, 0.5);
}


.preview-section {
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px dashed #ddd;
}

h3 {
  font-size: 20px;
  font-weight: 700;
  color: #555;
  margin-bottom: 20px;
}

.about-us-preview {
  background: #ffffff;
  max-width: 500px;
  min-width: 250px;
  padding: 30px;
  border-radius: 15px;
  border: 2px solid #F9C710; 
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
}

.preview-title {
  color: #1a1a1a;
  margin-bottom: 15px;
  font-size: 24px;
  font-weight: 800;
}

.preview-text {
  color: #444;
  font-size: 15px;
  line-height: 1.8;
  margin-bottom: 20px;
  text-align: justify;
}

.preview-image {
  width: 100%;
  height: auto;
  max-height: 250px;
  object-fit: cover;
  border-radius: 10px;
  border: 1px solid #ddd;
}

.image-placeholder {
    width: 100%;
    height: 150px;
    background-color: #f0f0f0;
    border: 1px solid #ccc;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #999;
    font-size: 14px;
}


.status-message {
    padding: 10px;
    border-radius: 8px;
    margin-top: 15px;
    font-weight: 600;
    text-align: center;
}
.loading {
    background-color: #fff9e6;
    color: #b8860b;
    border: 1px solid #ffe0a3;
}
.error {
    background-color: #fdd;
    color: #c00;
    border: 1px solid #fbb;
}
</style>