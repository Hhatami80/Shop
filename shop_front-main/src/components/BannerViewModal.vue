<template>
  <!-- MAIN MODAL -->
  <Teleport to="body">
    <Transition name="modal">
      <div class="modal-backdrop" @click="$emit('close')">
        <div class="modal-panel" @click.stop>
          <div class="modal-header">
            <h3>بنرهای دسته‌بندی</h3>
            <button class="close-btn" @click="$emit('close')" aria-label="بستن">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path
                  d="M18 6L6 18M6 6L18 18"
                  stroke="currentColor"
                  stroke-width="2.5"
                  stroke-linecap="round"
                />
              </svg>
            </button>
          </div>

          <!-- LIST -->
          <div v-if="catBannerStore.banners?.length" class="banner-list">
            <div
              v-for="b in catBannerStore.banners"
              :key="b.id"
              class="banner-item"
            >
              <img :src="b.image" class="banner-preview" />
              <p class="banner-text">{{ b.text || '' }}</p>

              <div class="banner-actions">
                <button class="action-btn btn-edit" @click="startEdit(b)">
                  ویرایش
                </button>
                <button class="action-btn btn-delete" @click="deleteBanner(b)">
                  حذف
                </button>
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

          <!-- FOOTER -->
          <div class="modal-actions">
            <button class="action-btn btn-save" @click="openAddModal">
              افزودن بنر جدید
            </button>
            <button class="btn-cancel" @click="$emit('close')">بستن</button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>

  <!-- ADD BANNER MODAL -->
  <BannerModal
    v-model="modelValue"
    :banners="[]"
    @update="saveNewBanners"
    @refresh="refreshBanners"
  />
</template>


<script setup>
import { ref, onMounted } from 'vue'
import Swal from 'sweetalert2'
import { useCategoryBannerStore } from '@/stores/useCatBannerStore'
import BannerModal from './BannerModal.vue'

const props = defineProps({
  categoryId: Number
})

const emit = defineEmits(['close', 'refresh'])

const catBannerStore = useCategoryBannerStore()

let editingBanner = ref(null)
let editForm = ref({ text: '', image: null })
let modelValue = ref(false)

onMounted(async () => {
  await catBannerStore.fetchBanners(props.categoryId)
})

const emitRefresh = () => emit('refresh')

const openAddModal = () => {
  modelValue.value = true
}

async function refreshBanners() {
  await catBannerStore.fetchBanners(props.categoryId)
}

const saveNewBanners = async (bannerList) => {
  for (const banner of bannerList) {
    const form = new FormData()
    form.append('text', banner.text)
    if (banner.file) form.append('image', banner.file)

    await catBannerStore.addBanner(props.categoryId, form)
  }

  emitRefresh()
}

const startEdit = (banner) => {
  editingBanner.value = banner
  editForm.value = {
    text: banner.text,
    image: null
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
  emitRefresh()
}

const deleteBanner = async (banner) => {
  Swal.fire({
    title: 'حذف بنر؟',
    html: '<p>این بنر پس از حذف قابل بازگشت نیست.</p>',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#e63946',
    cancelButtonColor: '#adb5bd',
    confirmButtonText: 'حذف',
    cancelButtonText: 'لغو'
  }).then(async (res) => {
    if (res.isConfirmed) {
      await catBannerStore.deleteBanner(props.categoryId, banner.id)

      Swal.fire({
        title: 'حذف شد!',
        icon: 'success',
        confirmButtonText: 'باشه'
      })

      emitRefresh()
    }
  })
}
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
  background: rgba(0, 0, 0, 0.55);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1rem;
}

.modal-panel {
  background: #fff;
  border-radius: 20px;
  width: 100%;
  max-width: 780px;
  max-height: 92vh;
  box-shadow: 0 25px 70px rgba(0, 0, 0, 0.22);
  overflow: hidden;
  direction: rtl;
  font-family: 'IRANSansX', sans-serif;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 1.5rem 1.8rem 1.2rem;
  background: linear-gradient(135deg, #f9c710, #e6b800);
  color: #111;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.55rem;
  font-weight: 900;
}

.close-btn {
  background: none;
  border: none;
  color: #111;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: 0.2s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.25);
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 2rem 1.8rem;
  background: #fdfdfd;
}

.banners-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1.8rem;
  justify-items: center;
}

.banner-card {
  background: #fff;
  border-radius: 18px;
  overflow: hidden;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  width: 100%;
  max-width: 280px;
}

.banner-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.18);
}

.image-wrapper {
  position: relative;
  width: 100%;
  padding-top: 56.25%;
  background: #f0f0f0;
  overflow: hidden;
}

.banner-image {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.banner-card:hover .banner-image {
  transform: scale(1.05);
}

.banner-caption {
  padding: 1rem 0.8rem;
  text-align: center;
  font-weight: 600;
  color: #222;
  font-size: 1rem;
  margin: 0;
  background: #fff;
}

.no-caption {
  padding: 0.8rem;
  text-align: center;
  color: #999;
  font-style: italic;
  font-size: 0.9rem;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #888;
}

.empty-state svg {
  color: #ccc;
  margin-bottom: 1rem;
}

.empty-state p {
  margin: 0.5rem 0 0;
  font-size: 1.1rem;
  font-weight: 500;
}

.modal-footer {
  padding: 1.4rem 1.8rem;
  background: #f9fafb;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: center;
  flex-shrink: 0;
}

.btn-close {
  padding: 0.9rem 2.5rem;
  background: #f9c710;
  color: #111;
  border: none;
  border-radius: 14px;
  font-weight: 900;
  font-size: 1.05rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 5px 18px rgba(249, 199, 16, 0.4);
}

.btn-close:hover {
  background: #e6b800;
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(249, 199, 16, 0.5);
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
