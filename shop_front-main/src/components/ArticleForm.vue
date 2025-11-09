<template>
  <div class="article-container">
    <div class="article-header">
      <h2>{{ route.params.id ? 'ویرایش مقاله' : 'ایجاد مقاله' }}</h2>
    </div>

    <div v-if="loading">در حال بارگذاری...</div>

    <form v-else @submit.prevent="handleSubmit">
      <div class="form-group">
        <label>عنوان</label>
        <input v-model="form.title" class="form-control lg" />
      </div>

      <div class="form-group">
        <label>خلاصه</label>
        <textarea v-model="form.short_description" class="form-control lg"></textarea>
      </div>

      <div class="form-group">
        <label>متن مقاله</label>
        <ArticleEditor v-model="form.full_description" />
      </div>

      <div class="form-group">
        <label>تصویر</label>
        <input type="file" @change="handleImage" class="form-control lg" />
        <div v-if="form.imagePreview" class="image-preview">
          <img :src="form.imagePreview" alt="preview" />
        </div>
      </div>

      <div class="form-submit">
        <button type="submit" class="btn">ذخیره</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useArticleStore } from '@/stores/ArticleStore'
import ArticleEditor from '@/components/ArticleEditor.vue'

const route = useRoute()
const router = useRouter()
const store = useArticleStore()

const loading = ref(false)

const form = ref({
  title: '',
  short_description: '',
  full_description: '',
  image: null,
  imagePreview: '',
})

const handleImage = (e) => {
  const file = e.target.files[0]
  if (file) {
    form.value.image = file
    form.value.imagePreview = URL.createObjectURL(file)
  }
}

const handleSubmit = async () => {
  const data = new FormData()
  data.append('title', form.value.title)
  data.append('short_description', form.value.short_description)
  data.append('full_description', form.value.full_description)
  if (form.value.image) data.append('image', form.value.image)

  if (route.params.id) {
    await store.updateArticle(route.params.id, data)
  } else {
    await store.createArticle(data)
  }

  router.push('/admin/articles')
}

onMounted(async () => {
  if (route.params.id) {
    loading.value = true
    const article = await store.fetchArticle(route.params.id)
    if (article) {
      form.value.title = article.title || ''
      form.value.short_description = article.short_description || ''
      form.value.full_description = article.full_description || ''
      form.value.imagePreview = article.image || ''
    }
    loading.value = false
  }
})
</script>

<style scoped>
.article-container {
  max-width: 700px;
  margin: 40px auto;
  padding: 20px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  
  direction: rtl;
  color: #333;
}

.article-header h2 {
  margin-bottom: 30px;
  font-size: 28px;
  font-weight: 700;
  text-align: center;
  color: #222;
}

form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  font-weight: 600;
  margin-bottom: 8px;
  font-size: 16px;
  color: #444;
}

input.form-control,
textarea.form-control {
  padding: 10px 15px;
  font-size: 16px;
  border: 1.8px solid #ccc;
  border-radius: 8px;
  transition: border-color 0.3s ease;
  resize: vertical;
  min-height: 40px;
}

input.form-control.lg {
  height: 45px;
}

textarea.form-control.lg {
  min-height: 100px;
}

input.form-control:focus,
textarea.form-control:focus {
  outline: none;
  border-color: gold;
  box-shadow: 0 0 8px rgba(233, 30, 99, 0.3);
}

.image-preview {
  margin-top: 10px;
  max-width: 200px;
  max-height: 150px;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.image-preview img {
  width: 100%;
  height: auto;
  display: block;
}

/* .article-editor {
  min-height: 400px; 
} */

.form-submit {
  text-align: center;
}

.btn {
  background-color: gold;
  color: white;
  font-size: 18px;
  padding: 12px 40px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 700;
  transition: background-color 0.3s ease;
  user-select: none;
}

.btn:hover {
  background-color: rgb(200, 173, 19);
}

@media (max-width: 768px) {
  .article-container {
    margin: 20px 15px;
    padding: 15px;
  }

  .article-header h2 {
    font-size: 22px;
  }
}
</style>
