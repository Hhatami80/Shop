<template>
  <div class="category-management">
    <h2 class="page-title">مدیریت دسته‌بندی‌ها</h2>

    <form @submit.prevent="handleSubmit" enctype="multipart/form-data" class="modern-form-card">
      <input v-model="form.title" placeholder="عنوان دسته" required class="form-input" />
      <div class="file-input-wrapper">
        <input
          type="file"
          ref="fileInput"
          @change="handleFileUpload"
          required
          id="file-upload"
          class="hidden-file-input"
        />
        <label for="file-upload" class="custom-file-label">
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2.5"
          >
            <path
              d="M21 15V19C21 20.105 20.105 21 19 21H5C3.895 21 3 20.105 3 19V15M17 8L12 3L7 8M12 3V15"
            />
          </svg>
          <span class="label-text">
            {{ imageFile ? imageFile.name : 'انتخاب تصویر دسته' }}
          </span>
        </label>
      </div>
      <button type="button" class="submit-button primary-btn" @click="isBannerModalOpen = true">
        افزودن بنرها
      </button>
      <button type="submit" class="submit-button primary-btn">
        <i class="fas fa-plus"></i> افزودن
      </button>
    </form>

    <hr class="divider" />

    <div v-if="loading" class="loading-state">
      <i class="fas fa-spinner fa-spin"></i> در حال بارگذاری...
    </div>
    <div v-else-if="error" class="error-state">{{ error }}</div>

    <table v-else class="data-table">
      <thead>
        <tr>
          <th>عنوان</th>
          <th>تصویر</th>
          <th>بنرها</th>
          <th>عملیات</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="cat in categoryStore.allCategories" :key="cat.id">
          <td class="table-title">{{ cat.title }}</td>
          <td><img :src="cat.image" alt="Category Image" class="category-image" /></td>
          <td>
            <button class="action-btn btn-view" @click="openBannerModal(cat)">
              <i class="fas fa-images"></i> مشاهده
            </button>
          </td>
          <td>
            <button class="action-btn btn-edit" @click="editCategory(cat)">
              <i class="fas fa-pen"></i> ویرایش
            </button>
            <button class="action-btn btn-delete" @click="openDelete(cat.id)">
              <i class="fas fa-trash-alt"></i> حذف
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <banner-view-modal
      v-if="isBannerViewModalOpen"
      :category-id="selectedCategory.id"
      @close="isBannerViewModalOpen = false"
      @refresh="loadCategories"
    />
    <edit-modal v-model="isEditModalOpen" :category="categoryToEdit" @save="saveEditedCategory" />
    <banner-modal v-model="isBannerModalOpen" :banners="banners" @update="updateBanners" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCategoryStore } from '@/stores/useCategoryStore'
import BannerViewModal from './BannerViewModal.vue'
import EditModal from '@/components/EditModal.vue'
import BannerModal from './BannerModal.vue'
import Swal from 'sweetalert2'
import 'sweetalert2/dist/sweetalert2.min.css'
import { toast } from 'vue3-toastify'
import { useCategoryBannerStore } from '@/stores/useCatBannerStore'

const categoryStore = useCategoryStore()
const catbannerStore = useCategoryBannerStore()

const form = ref({ title: '' })
const imageFile = ref(null)
const fileInput = ref(null)
const isBannerViewModalOpen = ref(false)
const banners = ref([])
const isBannerModalOpen = ref(false)

const loading = ref(false)
const error = ref(null)
const selectedCategory = ref({})
const selectedCategoryBanners = ref([])

const openBannerModal = (category) => {
  selectedCategory.value = category
  selectedCategoryBanners.value = category.banner_images || []
  isBannerViewModalOpen.value = true
}

onMounted(async () => {
  await loadCategories()
})

function updateBanners(newList) {
  banners.value = newList
}


const loadCategories = async () => {
  try {
    loading.value = true
    await categoryStore.getAllCategories();
  } catch (err) {
    error.value = 'خطا در دریافت دسته‌بندی‌ها'
  } finally {
    loading.value = false
  }
}

const handleFileUpload = (e) => {
  imageFile.value = e.target.files[0]
}

const handleSubmit = async () => {
  const formData = new FormData()
  formData.append('title', form.value.title)
  if (imageFile.value) formData.append('image', imageFile.value)

  banners.value.forEach((banner, index) => {
    if (banner.file) {
      formData.append(`banner[${index}]`, banner.file)
    }
    if (banner.text) {
      formData.append(`text[${index}]`, banner.text)
    }
  })

  const isSuccess = await categoryStore.addCategory(formData)
  if (isSuccess) {
    resetForm()
    await loadCategories()
  } else {
    toast.error('خطا در افزودن دسته‌بندی!')
  }
}

const resetForm = () => {
  form.value = { title: '' }
  imageFile.value = null
  if (fileInput.value) fileInput.value.value = null
}

const openDelete = (id) => {
  Swal.fire({
    title: '<span style="font-weight:bold; font-size:20px;">آیا مطمئنی؟</span>',
    html: '<p style="font-size:16px;">با حذف این دسته دیگر قابل بازیابی نیست!</p>',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#007bff',
    cancelButtonColor: '#6c757d',
    confirmButtonText: '<i class="fa fa-trash"></i> حذف دسته',
    cancelButtonText: '<i class="fa fa-times"></i> لغو',
    buttonsStyling: false,
    customClass: {
      popup: 'my-swal-popup',
      confirmButton: 'my-swal-confirm-btn',
      cancelButton: 'my-swal-cancel-btn',
    },
  }).then(async (result) => {
    if (result.isConfirmed) {
      await categoryStore.deleteCategory(id)
      await loadCategories()
      Swal.fire({
        title: '<span style="font-weight:bold; font-size:20px;">حذف شد!</span>',
        html: '<p style="font-size:16px;">دسته موردنظر با موفقیت حذف شد.</p>',
        icon: 'success',
        confirmButtonText: 'باشه',
        buttonsStyling: false,
        customClass: {
          popup: 'my-swal-popup',
          confirmButton: 'my-swal-confirm-btn-success',
        },
      })
    }
  })
}

const isEditModalOpen = ref(false)
const categoryToEdit = ref(null)

const editCategory = (cat) => {
  categoryToEdit.value = { ...cat }
  isEditModalOpen.value = true
}

const saveEditedCategory = async ({ id, formData }) => {
  await categoryStore.updateCategory(id, formData)
  await loadCategories()
}
</script>

<style scoped>
.category-management {
  --gold: #f9c710;
  --gold-hover: #e6b800;
  --gold-light: #fff9e6;
  --dark: #1a1a1a;
  --gray-100: #f8f9fa;
  --gray-200: #e9ecef;
  --gray-600: #6c757d;
  --gray-800: #343a40;
  --danger: #dc3545;
  --danger-hover: #c82333;
  --warning: #fd7e14;
  --success: #28a745;

  font-family: 'IRANSansX', 'Vazirmatn', sans-serif;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ed 100%);
  min-height: 100vh;
  padding: 2.5rem 2rem;
  direction: rtl;
}

.page-title {
  font-size: 2.2rem;
  font-weight: 900;
  color: var(--dark);
  text-align: center;
  margin-bottom: 2rem;
  position: relative;
}

.page-title::after {
  content: '';
  width: 120px;
  height: 6px;
  background: var(--gold);
  border-radius: 4px;
  display: block;
  margin: 1rem auto 0;
}


.modern-form-card {
  background: #fff;
  padding: 2rem;
  border-radius: 24px;
  box-shadow: 0 15px 45px rgba(0, 0, 0, 0.1);
  margin-bottom: 3rem;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  align-items: end;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(249, 199, 16, 0.15);
}

.form-input {
  padding: 1rem 1.2rem;
  border: 2px solid #e0e0e0;
  border-radius: 16px;
  font-size: 1.05rem;
  transition: all 0.3s ease;
  background: #fdfdfd;
}

.form-input:focus {
  outline: none;
  border-color: var(--gold);
  box-shadow: 0 0 0 5px rgba(249, 199, 16, 0.2);
  transform: translateY(-2px);
}


.file-input-wrapper {
  position: relative;
}

.custom-file-label {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, var(--gold), var(--gold-hover));
  color: #111;
  font-weight: 900;
  border-radius: 18px;
  cursor: pointer;
  transition: all 0.35s ease;
  box-shadow: 0 8px 25px rgba(249, 199, 16, 0.35);
  font-size: 1.05rem;
}

.custom-file-label:hover {
  background: linear-gradient(135deg, #ffd700, var(--gold));
  transform: translateY(-4px);
  box-shadow: 0 15px 35px rgba(249, 199, 16, 0.45);
}

.custom-file-label i {
  font-size: 1.3rem;
}


.primary-btn {
  padding: 1rem 2rem;
  background: linear-gradient(135deg, var(--gold), var(--gold-hover));
  color: #111;
  border: none;
  border-radius: 18px;
  font-weight: 900;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.35s ease;
  box-shadow: 0 8px 25px rgba(249, 199, 16, 0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  min-width: 160px;
}

.primary-btn:hover {
  transform: translateY(-4px);
  box-shadow: 0 15px 35px rgba(249, 199, 16, 0.45);
}


.divider {
  height: 2px;
  background: linear-gradient(to right, transparent, var(--gold), transparent);
  border: none;
  margin: 3rem 0;
}


.loading-state,
.error-state {
  text-align: center;
  padding: 4rem 2rem;
  font-size: 1.4rem;
  border-radius: 20px;
  background: #fff;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
}

.loading-state i {
  color: var(--gold);
  font-size: 2rem;
  margin-left: 1rem;
}

.error-state {
  background: #ffe6e6;
  color: var(--danger);
  border: 2px dashed #fca5a5;
}


.data-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: #fff;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.12);
  margin-top: 1rem;
}

.data-table thead {
  background: linear-gradient(135deg, var(--gold), var(--gold-hover));
  color: #111;
}

.data-table th {
  padding: 1.4rem 1rem;
  font-weight: 900;
  font-size: 1.1rem;
  text-align: center;
}

.data-table tbody tr {
  transition: all 0.3s ease;
  border-bottom: 1px solid #eee;
}

.data-table tbody tr:hover {
  background: var(--gold-light);
  transform: scale(1.005);
  box-shadow: 0 10px 30px rgba(249, 199, 16, 0.15);
}

.data-table td {
  padding: 1.2rem 1rem;
  text-align: center;
  vertical-align: middle;
}

.table-title {
  font-weight: 700;
  color: var(--dark);
  font-size: 1.1rem;
}

.category-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 16px;
  border: 3px solid #fff;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  transition: all 0.4s ease;
}

.category-image:hover {
  transform: scale(1.1);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.25);
}


.action-btn {
  padding: 0.75rem 1.2rem;
  border: none;
  border-radius: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  margin: 0 6px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 0.95rem;
  min-width: 100px;
}

.btn-view {
  background: #17a2b8;
  color: white;
}

.btn-view:hover {
  background: #138496;
  transform: translateY(-3px);
}

.btn-edit {
  background: var(--warning);
  color: white;
}

.btn-edit:hover {
  background: #e68900;
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(253, 126, 20, 0.4);
}

.btn-delete {
  background: var(--danger);
  color: white;
}

.btn-delete:hover {
  background: var(--danger-hover);
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(220, 53, 69, 0.4);
}

.action-btn i {
  font-size: 1.1rem;
}
.hidden-file-input {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}


.custom-file-label {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 1.1rem 1.8rem;
  background: linear-gradient(135deg, var(--gold), var(--gold-hover));
  color: #111;
  font-weight: 900;
  border-radius: 18px;
  cursor: pointer;
  transition: all 0.35s ease;
  box-shadow: 0 8px 25px rgba(249, 199, 16, 0.35);
  font-size: 1.05rem;
  user-select: none;
  /* min-height: 56px; */
}

.custom-file-label:hover {
  background: linear-gradient(135deg, #ffd700, var(--gold));
  transform: translateY(-4px);
  box-shadow: 0 15px 35px rgba(249, 199, 16, 0.45);
}

.custom-file-label svg {
  flex-shrink: 0;
}

.label-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 220px; 
}


.custom-file-label.has-file {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}


@media (max-width: 768px) {
  .modern-form-card {
    grid-template-columns: 1fr;
  }

  .data-table {
    font-size: 0.9rem;
  }

  .action-btn {
    padding: 0.6rem 1rem;
    font-size: 0.85rem;
    min-width: auto;
  }

  .category-image {
    width: 60px;
    height: 60px;
  }
}
</style>
