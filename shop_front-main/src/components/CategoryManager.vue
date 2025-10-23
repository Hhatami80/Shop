<template>
  <div class="category-management">
    <h2 class="page-title">مدیریت دسته‌بندی‌ها</h2>

    <form @submit.prevent="handleSubmit" enctype="multipart/form-data" class="modern-form-card">
      <input v-model="form.title" placeholder="عنوان دسته" required class="form-input" />
      <div class="file-input-wrapper">
        <input type="file" ref="fileInput" @change="handleFileUpload" required id="file-upload" class="hidden-file-input" />
        <label for="file-upload" class="custom-file-label">
          <i class="fas fa-upload"></i> {{ imageFile ? imageFile.name : 'انتخاب تصویر دسته' }}
        </label>
      </div>
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
          <th>عملیات</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="cat in categoryStore.allCategories" :key="cat.id">
          <td class="table-title">{{ cat.title }}</td>
          <td><img :src="cat.image" alt="Category Image" class="category-image" /></td>
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

    <edit-modal v-model="isEditModalOpen" :category="categoryToEdit" @save="saveEditedCategory" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCategoryStore } from '@/stores/useCategoryStore'
import EditModal from '@/components/EditModal.vue'
import Swal from 'sweetalert2'
import 'sweetalert2/dist/sweetalert2.min.css'
import { toast } from 'vue3-toastify'

const categoryStore = useCategoryStore()

const form = ref({ title: '' })
const imageFile = ref(null)
const fileInput = ref(null)

const loading = ref(false)
const error = ref(null)

onMounted(async () => {
  await loadCategories()
})

const loadCategories = async () => {
  try {
    loading.value = true
    await categoryStore.getAllCategories()
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

  const isSuccess = await categoryStore.addCategory(formData)
  if (isSuccess) {
    toast.success('دسته‌بندی با موفقیت اضافه شد')
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
  --primary-color: #ffd700; 
  --primary-color-hover: #E6C200; 
  --primary-text-color: #333;
  --primary-light: #fff8e1;
  --secondary-color: #34495e;
  --danger-color: #dc3545; 
  --success-color: #28a745; 
  --bg-light: #f8f9fa; 
  --border-light: #e9ecef;
  --shadow-color: rgba(0, 0, 0, 0.08);
  --warning-color: #FF9800;
  
  font-family: 'Vazirmatn', sans-serif;
  padding: 25px;
  background-color: var(--bg-light);
  min-height: 100%;
}

.page-title {
  color: var(--secondary-color);
  font-size: 1.8rem;
  margin-bottom: 25px;
  border-bottom: 2px solid var(--border-light);
  padding-bottom: 10px;
}

.modern-form-card {
  background-color: #fff;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 15px var(--shadow-color);
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  align-items: center;
  margin-bottom: 30px;
}

.form-input {
  padding: 12px;
  border-radius: 8px;
  border: 1px solid var(--border-light);
  font-size: 15px;
  flex: 1 1 200px;
  background-color: #fff;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.form-input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 5px rgba(255, 215, 0, 0.5); 
  outline: none;
}

.file-input-wrapper {
  flex: 1 1 250px;
}

.hidden-file-input {
  display: none;
}

.custom-file-label {
  display: block;
  padding: 12px 15px;
  border-radius: 8px;
  background-color: var(--primary-color); 
  color: var(--primary-text-color); 
  border: 1px solid var(--primary-color);
  text-align: center;
  cursor: pointer;
  transition: background-color 0.3s, opacity 0.3s;
  font-size: 15px;
  font-weight: 600;
}

.custom-file-label:hover {
  background-color: var(--primary-color-hover); 
  opacity: 1;
}

.custom-file-label i {
  margin-left: 8px;
}

.primary-btn {
  background-color: var(--primary-color);
  color: var(--primary-text-color); 
  border: none;
  border-radius: 8px;
  padding: 12px 25px;
  cursor: pointer;
  font-weight: 600;
  transition: 0.3s;
  flex-grow: 0;
  white-space: nowrap;
}

.primary-btn:hover {
  background-color: var(--primary-color-hover); 
  box-shadow: 0 4px 10px rgba(255, 215, 0, 0.4);
}

.primary-btn i {
  margin-left: 5px;
}

.divider {
  border: none;
  border-top: 1px solid var(--border-light);
  margin: 30px 0;
}

.loading-state, .error-state {
  text-align: center;
  padding: 30px;
  font-size: 1.1rem;
  color: var(--secondary-color);
}
.loading-state i {
  margin-left: 10px;
  color: var(--primary-color);
}
.error-state {
  color: var(--danger-color);
  background-color: #ffeaea;
  border-radius: 8px;
}

.data-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 15px var(--shadow-color);
  background-color: #fff;
}

.data-table thead tr {
  background-color: var(--primary-color); 
  color: var(--primary-text-color); 
}

th, td {
  padding: 15px;
  text-align: center;
}

th {
  font-weight: 700;
  font-size: 1rem;
}

.data-table tbody tr:nth-child(even) {
  background-color: var(--primary-light); 
}

.data-table tbody tr:hover {
  background-color: var(--primary-light); 
  filter: brightness(0.95); 
}

.table-title {
  font-weight: 500;
  color: var(--secondary-color);
}

.category-image {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid var(--border-light);
  transition: transform 0.3s;
}

.category-image:hover {
  transform: scale(1.05);
}

.action-btn {
  border: 1px solid transparent; 
  border-radius: 8px;
  padding: 10px 15px;
  font-weight: 500;
  cursor: pointer;
  transition: 0.3s, transform 0.1s;
  margin: 0 5px;
  display: inline-flex;
  align-items: center;
  font-size: 0.95rem;
}

.action-btn i {
  margin-left: 5px;
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

/* .my-swal-popup {
  font-family: 'Vazirmatn', sans-serif;
  border-radius: 12px;
  direction: rtl;
}
.my-swal-confirm-btn {
  background-color: var(--danger-color) !important;
  color: white !important;
  padding: 10px 20px;
  border-radius: 8px;
  box-shadow: none !important;
  margin: 0 5px;
  transition: background-color 0.3s;
}
.my-swal-cancel-btn {
  background-color: var(--secondary-color) !important;
  color: white !important;
  padding: 10px 20px;
  border-radius: 8px;
  box-shadow: none !important;
  margin: 0 5px;
  transition: background-color 0.3s;
}

.my-swal-confirm-btn-success {
  background-color: var(--success-color) !important;
  color: white !important;
  padding: 10px 20px;
  border-radius: 8px;
  box-shadow: none !important;
  margin: 0 5px;
} */
</style>