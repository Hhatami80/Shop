<template>
  <QuillEditor v-model:content="modelValue" content-type="html" theme="snow" class="quill-wrap" />
</template>

<script setup>
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'

const modelValue = defineModel()
</script>

<style scoped>
.quill-wrap {
  border: 1.5px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
}

.quill-wrap :deep(.ql-editor) {
  min-height: 320px;
  max-height: 600px;
  overflow-y: auto;
  padding: 14px;
  line-height: 1.8;
  direction: rtl;
  text-align: right;
}

.quill-wrap :deep(.ql-container) {
  border: none;
}
.quill-wrap :deep(.ql-toolbar) {
  direction: rtl;
}
</style>
