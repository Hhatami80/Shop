<template>
  <div class="editor-wrapper" :class="theme">
    <div class="toolbar">
      <button @click="toggleTheme">
        {{ theme === 'light' ? 'حالت شب' : 'حالت روز' }}
      </button>
      <button @click="togglePreview">
        {{ previewOnly ? 'نمایش ویرایشگر' : 'فقط پیش‌نمایش' }}
      </button>
      <button @click="emitSave">ذخیره</button>
    </div>

    <MdEditor
      v-if="!previewOnly"
      v-model="content"
      :theme="theme"
      language="fa-IR"
      preview-theme="default"
      code-theme="github"
      :toolbars="customToolbar"
      :show-code-row-number="true"
      @on-upload-img="handleUpload"
      height="500px"
      style="direction: rtl; text-align: right; font-family: Vazir, Tahoma, sans-serif"
    />

    <MdPreview v-else :model-value="content" :theme="theme" language="fa-IR" class="preview-box" />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { MdEditor, MdPreview, config } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import api from '@/services/AxiosService'

const faIR = {
  bold: 'پررنگ',
  italic: 'کج',
  underline: 'زیرخط',
  strikeThrough: 'خط‌خورده',
  title: 'عنوان',
  quote: 'نقل قول',
  unorderedList: 'لیست نامرتب',
  orderedList: 'لیست مرتب',
  link: 'لینک',
  image: 'تصویر',
  table: 'جدول',
  code: 'کد',
  codeBlock: 'بلوک کد',
  preview: 'پیش‌نمایش',
  fullscreen: 'تمام صفحه',
  uploadImage: 'آپلود تصویر',
  undo: 'بازگشت',
  redo: 'بازکردن',
}

config({
  editorConfig: {
    language: 'fa-IR',
  },
  languageUserDefined: {
    'fa-IR': faIR,
  },
})

const props = defineProps({
  modelValue: { type: String, default: '' },
})

const emits = defineEmits(['update:modelValue', 'save'])

const content = ref(props.modelValue)
const theme = ref('light')
const previewOnly = ref(false)

const customToolbar = [
  'bold',
  'underline',
  'italic',
  'strikeThrough',
  'title',
  'quote',
  'unorderedList',
  'orderedList',
  'link',
  'image',
  'table',
  'code',
  'codeBlock',
  'preview',
  'fullscreen',
]

watch(content, (value) => {
  emits('update:modelValue', value)
})

const toggleTheme = () => {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
}

const togglePreview = () => {
  previewOnly.value = !previewOnly.value
}

const handleUpload = async (files, callback) => {
  const urls = []
  for (const file of files) {
    const formData = new FormData()
    formData.append('file', file)

    const res = await api.post('/articles/upload-image/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    const data = res.data
    urls.push(data.url)
  }
  callback(urls)
}

const emitSave = () => {
  emits('save', content.value)
}
</script>

<style scoped>
@import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazir-font@v30.1.0/dist/font-face.css');

.editor-wrapper {
  border: 1px solid #ddd;
  border-radius: 10px;
  overflow: hidden;
}

.light {
  background: #ffffff;
  color: #333;
}
.dark {
  background: #1e1e1e;
  color: white;
}

.toolbar {
  display: flex;
  gap: 10px;
  padding: 10px;
  background: #f2f2f2;
  border-bottom: 1px solid #ddd;
  direction: rtl;
}

.toolbar button {
  padding: 7px 14px;
  border: none;
  cursor: pointer;
  border-radius: 6px;
  background: #ffd700;
  color: white;
  font-size: 14px;
}

.toolbar button:hover {
  opacity: 0.8;
}

.preview-box {
  padding: 16px;
  background: white;
}
</style>
