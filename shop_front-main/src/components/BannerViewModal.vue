<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal-card">
      <h3 class="modal-title">بنرهای دسته‌بندی</h3>

      <div v-if="banners.length" class="banner-list">
        <div v-for="(b, index) in banners" :key="b.id" class="banner-item">
          <img :src="b.image" class="banner-preview" />
          <p class="banner-text">{{ b.text || '' }}</p>

          <!-- ACTION BUTTONS -->
          <div class="banner-actions">
            <button class="action-btn btn-edit" @click="startEdit(b)">ویرایش</button>
            <button class="action-btn btn-delete" @click="deleteBanner(b)">حذف</button>
          </div>
        </div>
      </div>

      <p v-else>هیچ بنری اضافه نشده است.</p>

      <!-- EDIT FORM -->
      <div v-if="editingBanner" class="edit-form">
        <h4>ویرایش بنر</h4>

        <input v-model="editForm.text" placeholder="متن بنر" class="form-input" />

        <input type="file" @change="handleFile" class="form-input" />

        <div class="edit-actions">
          <button class="action-btn btn-save" @click="saveEdit">ذخیره</button>
          <button class="action-btn btn-cancel" @click="cancelEdit">لغو</button>
        </div>
      </div>

      <div class="modal-actions">
        <button class="action-btn btn-save" @click="openAddModal">افزودن بنر جدید </button>
        <button class="btn-cancel" @click="$emit('close')">بستن</button>
      </div>
    </div>
  </div>
  <add-banner-modal
  v-model="modelValue"
  :banners="[]"
  @update="saveNewBanners"
  @refresh="refreshBanners"
/>
</template>

<script setup>
import { useCategoryBannerStore } from '@/stores/useCatBannerStore'
import AddBannerModal from './BannerModal.vue'
import { ref } from 'vue'

const catBannerStore = useCategoryBannerStore()
// Props
const props = defineProps({
  banners: Array,
  categoryId: Number, // required for API calls
})



// Local state
let editingBanner = ref(null)
let editForm = ref({ text: '', image: null })
let modelValue = ref(false)

const openAddModal = () => {
  modelValue.value = true
}

async function refreshBanners() {
  await catBannerStore.fetchBanners(props.categoryId); // reload banners from store/DB
}

const saveNewBanners = async (bannerList) => {

  for (const banner of bannerList) {
    const form = new FormData()
    form.append(`text`, banner.text)
    if (banner.file) form.append(`image`, banner.file)

    await catBannerStore.addBanner(props.categoryId, form)
  }

  emitRefresh()
}

const startEdit = (banner) => {
  editingBanner.value = banner
  editForm.value = {
    text: banner.text,
    image: null,
  }
}

const cancelEdit = () => {
  editingBanner.value = null
  editForm.value = { text: '', image: null }
}

const handleFile = (e) => {
  editForm.value.image = e.target.files[0]
}

const saveEdit = async () => {
  const form = new FormData()
  form.append('text', editForm.value.text)
  if (editForm.value.image) form.append('image', editForm.value.image)

  await catBannerStore.updateBanner(props.categoryId, editingBanner.value.id, form)

  // Let parent refresh
  emitRefresh()
}

const deleteBanner = async (banner) => {
  if (!confirm('حذف بنر؟')) return

  await catBannerStore.deleteBanner(props.categoryId, banner.id)

  emitRefresh()
}

const emit = defineEmits(['close', 'refresh'])
const emitRefresh = () => emit('refresh')
</script>

<style scoped>
.form-input {
  width: 60%;
  padding: 10px 0px;
  border: 1px solid #dcdcdc;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: border-color 0.3s;
  margin: 0 auto 8px;
  text-indent: 2px;
}

.form-input:focus {
  border-color: #007bff;
  outline: none;
}

.action-btn {
  border: 1px solid transparent;
  border-radius: 8px;
  padding: 7px 6px;
  font-weight: 500;
  cursor: pointer;
  transition:
    0.3s,
    transform 0.1s;
  margin: 0 5px;
  display: inline-flex;
  align-items: center;
  font-size: 0.95rem;
}

.action-btn i {
  margin-left: 5px;
}

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

.btn-edit {
  background-color: var(--warning-color);
  color: white;
}

.btn-edit:hover {
  background-color: #e68900;
  box-shadow: 0 2px 8px rgba(255, 152, 0, 0.4);
  transform: translateY(-1px);
}
.btn-delete {
  background-color: var(--danger-color);
  color: white;
}

.btn-delete:hover {
  background-color: #c82333;
  box-shadow: 0 2px 8px rgba(220, 53, 69, 0.4);
  transform: translateY(-1px);
}
</style>
