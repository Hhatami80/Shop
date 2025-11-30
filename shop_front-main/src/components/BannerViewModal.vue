<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal-card">
      <h3 class="modal-title">بنرهای دسته‌بندی</h3>

      <div v-if="banners.length" class="banner-list">
        <div v-for="(b, index) in banners" :key="index" class="banner-item">
          <img :src="b.image" class="banner-preview" />
          <p class="banner-text">{{ b.text || '' }}</p>
        </div>
      </div>
      <p v-else>هیچ بنری اضافه نشده است.</p>

      <div class="modal-actions">
        <button class="btn-cancel" @click="$emit('close')">بستن</button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  banners: Array,
})
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
}

.modal-card {
  background: #fff;
  padding: 25px;
  border-radius: 12px;
  width: 600px;
  max-width: 95%;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 15px;
  text-align: center;
}

.banner-list {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  justify-content: center;
  margin-bottom: 20px;
}

.banner-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 150px;
  text-align: center;
}

.banner-preview {
  width: 100%;
  height: 100px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 8px;
  border: 1px solid #e9ecef;
}

.banner-text {
  font-size: 0.9rem;
  color: #333;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
}

.btn-cancel {
  padding: 10px 20px;
  background-color: #ccc;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: 0.3s;
}

.btn-cancel:hover {
  background-color: #b3b3b3;
}
</style>
