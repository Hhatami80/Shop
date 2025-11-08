<template>
  <div class="product-container">
    <h4 class="page-title">مدیریت محصولات کارت اسلایدری</h4>

    <h5 class="form-title-section">
      {{ isEditing ? 'ویرایش محصول' : 'افزودن محصول جدید' }}
    </h5>
    <form @submit.prevent="submitForm" class="product-form">
      <div class="row">
        <div class="col-half">
          <label for="title" class="label">عنوان محصول</label>
          <input
            id="title"
            type="text"
            v-model="form.title"
            class="input"
            placeholder="نام کامل محصول"
            required
          />
        </div>

        <div class="col-half">
          <label for="category" class="label">دسته‌بندی</label>
          <select id="category" v-model="form.category_id" class="input select" required>
            <option value="">انتخاب دسته‌بندی</option>
            <option v-for="cat in categoryStore.allCategories" :key="cat.id" :value="cat.id">
              {{ cat.title }}
            </option>
          </select>
        </div>

        <div class="col-half">
          <label for="price" class="label">قیمت اصلی (تومان)</label>
          <input
            id="price"
            type="number"
            v-model.number="form.price"
            class="input"
            placeholder="قیمت"
            required
          />
        </div>

        <div class="col-half">
          <label for="discount" class="label">تخفیف (درصد)</label>
          <input
            id="discount"
            type="number"
            v-model.number="form.discount"
            class="input"
            placeholder="تخفیف (مثلاً 20)"
          />
        </div>

        <div class="col-full">
          <label for="description" class="label">توضیحات محصول</label>
          <textarea
            id="description"
            v-model="form.description"
            class="input"
            rows="4"
            placeholder="توضیحات کامل محصول"
            required
          ></textarea>
        </div>

        <div class="row">
          <div class="col-half image-upload-area">
            <label class="label">عکس اصلی محصول</label>
            <input
              type="file"
              accept="image/*"
              class="input file-input"
              @change="handleMainImage"
              :required="!isEditing && !form.imagePreview"
            />
            <div v-if="form.imagePreview" class="image-preview-wrapper">
              <img :src="form.imagePreview" class="image-preview" alt="پیش‌نمایش" />
              <button type="button" class="remove-image" @click="removeMainImage">×</button>
            </div>
          </div>

          <div class="col-half image-upload-area">
            <label class="label">گالری تصاویر (اختیاری)</label>
            <input
              type="file"
              accept="image/*"
              multiple
              class="input file-input"
              @change="handleGalleryUpload"
            />
            <div class="gallery-preview">
              <div v-for="(img, index) in form.galleryPreviews" :key="index" class="gallery-thumb">
                <img :src="img" alt="گالری" class="image-preview" />
                <button
                  type="button"
                  class="remove-gallery"
                  @click="() => removeGalleryImage(index)"
                >
                  ×
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="col-full properties-section">
          <h6 class="section-title">ویژگی‌ها (اختیاری)</h6>
          <div class="row prop-row" v-for="(property, index) in form.properties" :key="index">
            <div class="col-5">
              <input
                type="text"
                v-model="property.key"
                placeholder="نام ویژگی (مثل: رنگ)"
                class="input"
                required
              />
            </div>
            <div class="col-5">
              <input
                type="text"
                v-model="property.value"
                placeholder="مقدار ویژگی (مثل: مشکی)"
                class="input"
                required
              />
            </div>
            <div class="col-2 remove-prop-btn-col">
              <button type="button" class="btn btn-remove-prop" @click="removeProperty(index)">
                <fa-icon :icon="['fas', 'minus-circle']" />
              </button>
            </div>
          </div>
          <button type="button" class="btn btn-add-prop" @click="addProperty">
            <fa-icon :icon="['fas', 'plus-circle']" /> افزودن ویژگی
          </button>
        </div>

        <div class="col-full form-actions">
          <button type="submit" class="btn btn-submit" :disabled="adminStore.loading">
            <fa-icon v-if="adminStore.loading" :icon="['fas', 'spinner']" pulse />
            {{ isEditing ? 'ذخیره تغییرات' : 'افزودن محصول' }}
          </button>
          <button type="button" class="btn btn-cancel" @click="resetForm">انصراف</button>
        </div>
      </div>
    </form>

    <div v-if="submitSuccess" class="success-message">عملیات با موفقیت انجام شد!</div>
    <div v-if="submitError" class="error-message">{{ submitError }}</div>

    <hr class="divider" />

    <div class="table-wrapper">
      <div v-if="adminStore.loading" class="loading-state">
        <fa-icon :icon="['fas', 'spinner']" pulse /> در حال بارگذاری محصولات...
      </div>
      <table class="custom-table" v-else-if="adminStore.products.length">
        <thead>
          <tr>
            <th>تصویر</th>
            <th>عنوان</th>
            <th>دسته‌بندی</th>
            <th>قیمت</th>
            <th>تخفیف</th>
            <th>توضیحات</th>
            <th>ویژگی‌ها</th>
            <th>وضعیت</th>
            <th>عملیات</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(product, index) in paginatedProducts" :key="product.id || index">
            <td><img :src="product.image" class="product-img-thumb" /></td>
            <td class="product-title-cell">{{ product.title }}</td>
            <td>{{ product.category?.title }}</td>
            <td class="price-cell">{{ product.final_price }}</td>
            <td class="discount-cell">{{ product.discount }}%</td>
            <td class="description-cell">{{ truncateDescription(product.description) }}</td>
            <td>
              <ul class="prop-list">
                <li
                  v-for="(prop, pIndex) in (typeof product.properties === 'string'
                    ? JSON.parse(product.properties)
                    : product.properties) || []"
                  :key="pIndex"
                >
                  <strong>{{ prop.key }}:</strong> {{ truncateDescription(prop.value) }}
                </li>
              </ul>
            </td>
            <td>
              <label class="toggle-switch">
                <input
                  type="checkbox"
                  :checked="product.is_active"
                  @change="adminStore.toggleProductStatus(product.id, $event.target.checked)"
                />
                <span class="slider"></span>
              </label>
            </td>
            <td class="actions-cell">
              <button class="btn btn-view" @click="showProductDetails(product)">
                <fa-icon :icon="['fas', 'eye']" /> نمایش
              </button>
              <button class="btn btn-edit" @click="editProduct(product, index)">
                <fa-icon :icon="['fas', 'edit']" /> ویرایش
              </button>
              <button class="btn btn-delete" @click="removeProduct(product.id, index)">
                <fa-icon :icon="['fas', 'trash']" /> حذف
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="totalPages > 1" class="pagination">
        <button class="pagination-btn" :disabled="currentPage === 1" @click="prevPage">قبلی</button>
        <span>صفحه {{ currentPage }} از {{ totalPages }}</span>
        <button class="pagination-btn" :disabled="currentPage === totalPages" @click="nextPage">
          بعدی
        </button>
      </div>

      <div v-else-if="!adminStore.products.length" class="empty-state">
        محصولی برای نمایش وجود ندارد.
      </div>
    </div>

    <Teleport to="body">
      <div v-if="isModalOpen" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <button class="modal-close-btn" @click="closeModal">&times;</button>
          <div v-if="selectedProduct" class="product-details">
            <h3 class="product-modal-title">مشخصات: {{ selectedProduct.title }}</h3>
            <hr class="modal-divider" />
            <div class="modal-main-info">
              <div class="modal-images">
                <div class="main-image-wrapper">
                  <img :src="selectedProduct.image" alt="تصویر اصلی" class="main-image" />
                </div>
                <div v-if="selectedProduct.galleryPreviews?.length" class="gallery-images">
                  <img
                    v-for="(img, idx) in selectedProduct.galleryPreviews"
                    :key="idx"
                    :src="img"
                    class="gallery-thumb"
                  />
                </div>
              </div>

              <div class="modal-text-info">
                <p class="modal-price">
                  قیمت نهایی:
                  <span
                    >{{
                      (selectedProduct.final_price || selectedProduct.price).toLocaleString()
                    }}
                    تومان</span
                  >
                </p>
                <p class="modal-category">
                  قیمت اصلی: <span>{{ selectedProduct.price.toLocaleString() }} تومان</span>
                </p>
                <p class="modal-category">
                  دسته‌بندی: <span>{{ selectedProduct.category?.title }}</span>
                </p>
                <div v-if="selectedProduct.discount > 0" class="modal-discount-tag">
                  {{ selectedProduct.discount }}% تخفیف!
                </div>
              </div>
            </div>

            <h4 class="modal-subtitle">توضیحات</h4>
            <p class="modal-description">{{ selectedProduct.description }}</p>

            <div
              v-if="selectedProduct.properties && selectedProduct.properties.length"
              class="modal-properties-list"
            >
              <h4 class="modal-subtitle">ویژگی‌ها</h4>
              <ul class="prop-list-modal">
                <li
                  v-for="(prop, pIndex) in (typeof selectedProduct.properties === 'string'
                    ? JSON.parse(selectedProduct.properties)
                    : selectedProduct.properties) || []"
                  :key="pIndex"
                >
                  <strong>{{ prop.key }}:</strong> {{ prop.value }}
                </li>
              </ul>
            </div>

            <button
              class="modal-edit-btn"
              @click="
                () => {
                  editProduct(selectedProduct)
                  closeModal()
                }
              "
            >
              <fa-icon :icon="['fas', 'edit']" /> ویرایش محصول
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useProductStore } from '@/stores/useProductStore'
import { useCategoryStore } from '@/stores/useCategoryStore'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'
import { useAdminStore } from '@/stores/useAdminStore'

const productStore = useProductStore()
const adminStore = useAdminStore()
const categoryStore = useCategoryStore()

const isEditing = ref(false)
const editingIndex = ref(-1)
const isModalOpen = ref(false)
const selectedProduct = ref(null)

const form = reactive({
  id: null,
  title: '',
  category_id: '',
  price: null,
  discount: '',
  description: '',
  imageFile: null,
  imagePreview: null,
  galleryFiles: [],
  galleryPreviews: [],
  properties: [],
})

const submitSuccess = ref(false)
const submitError = ref(null)

const currentPage = ref(1)
const pageSize = 5

const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return adminStore.products.slice(start, start + pageSize)
})

const totalPages = computed(() => Math.ceil(adminStore.products.length / pageSize))

function nextPage() {
  if (currentPage.value < totalPages.value) currentPage.value++
}

function prevPage() {
  if (currentPage.value > 1) currentPage.value--
}

function resetForm() {
  form.id = null
  form.title = ''
  form.category_id = ''
  form.price = null
  form.discount = ''
  form.description = ''
  form.imageFile = null
  form.imagePreview = null
  form.galleryFiles = []
  form.galleryPreviews = []
  form.properties = []
  isEditing.value = false
  editingIndex.value = -1
  submitSuccess.value = false
  submitError.value = null
}

function addProperty() {
  form.properties.push({ key: '', value: '' })
}

function removeProperty(index) {
  form.properties.splice(index, 1)
}

function truncateDescription(text, maxLength = 60) {
  if (!text) return ''
  return text.length > maxLength ? text.slice(0, maxLength) + '...' : text
}

function handleMainImage(event) {
  const file = event.target.files[0]
  if (file) {
    form.imageFile = file
    form.imagePreview = URL.createObjectURL(file)
  }
}

function handleGalleryUpload(event) {
  const files = Array.from(event.target.files)
  form.galleryFiles.push(...files)
  form.galleryPreviews.push(...files.map((f) => URL.createObjectURL(f)))
}

function removeGalleryImage(index) {
  form.galleryFiles.splice(index, 1)
  form.galleryPreviews.splice(index, 1)
}

async function submitForm() {
  submitSuccess.value = false
  submitError.value = null

  if (!form.title || !form.category_id || form.price === null || !form.description) {
    toast.warning('لطفاً همه فیلدهای ضروری را پر کنید.')
    return
  }
  if (!isEditing.value && !form.imageFile) {
    toast.warning('لطفاً یک تصویر برای محصول انتخاب کنید.')
    return
  }

  let payload
  if (form.imageFile || form.galleryFiles.length) {
    payload = new FormData()
    payload.append('title', form.title)
    payload.append('category_id', form.category_id)
    payload.append('price', form.price)
    payload.append('discount', form.discount)
    payload.append('description', form.description)
    if (form.imageFile) payload.append('image', form.imageFile)
    if (form.galleryFiles) form.galleryFiles.forEach((file, idx) => payload.append(`uploaded_images`, file))
    payload.append('properties', JSON.stringify(form.properties || []))
    if (isEditing.value) payload.append('_method', 'PUT')
  } else {
    payload = {
      title: form.title,
      category_id: form.category_id,
      price: form.price,
      discount: form.discount,
      description: form.description,
      properties: JSON.stringify(form.properties || []),
    }
  }

  try {
    if (isEditing.value && form.id) {
      await productStore.updateProduct(form.id, payload)
      productStore.products[editingIndex.value] = {
        ...productStore.products[editingIndex.value],
        title: form.title,
        category: categoryStore.allCategories.find((c) => c.id === form.category_id) || null,
        price: form.price,
        final_price: form.price * (1 - (form.discount || 0) / 100),
        discount: form.discount,
        description: form.description,
        properties: [...form.properties],
        image: form.imagePreview,
      }
      toast.success('محصول با موفقیت ویرایش شد.')
    } else {
     
      const newProduct = await productStore.addProduct(payload)
      const category = categoryStore.allCategories.find((c) => c.id === form.category_id) || null
      productStore.products.unshift({
        ...newProduct,
        title: form.title,
        category,
        price: form.price,
        final_price: form.price * (1 - (form.discount || 0) / 100),
        discount: form.discount,
        description: form.description,
        properties: [...form.properties],
        image: form.imagePreview,
      })
      toast.success('محصول با موفقیت اضافه شد.')
    }

    resetForm()
  } catch (error) {
    const message = productStore.error || 'خطا در ذخیره محصول. لطفاً اتصال و داده‌ها را بررسی کنید.'
    submitError.value = message
    toast.error(message)
  }
}

async function removeProduct(productId, index) {
  if (!confirm('آیا از حذف این محصول مطمئن هستید؟')) return
  try {
    await adminStore.deleteProduct(productId).data
    toast.success("محصول با موفقیت حذف شد")
  } catch {
    toast.error(adminStore.error || 'خطا در حذف محصول')
  }
}

function editProduct(product, index) {
  isEditing.value = true
  editingIndex.value = index
  form.id = product.id || null
  form.title = product.title || ''
  form.category_id = product.category?.id || product.category_id || ''
  form.price = product.price || null
  form.discount = product.discount || ''
  form.description = product.description || ''
  form.imageFile = null
  form.imagePreview = product.image || null
  form.galleryFiles = []
  form.galleryPreviews = []

  if (typeof product.properties === 'string') {
    try {
      form.properties = JSON.parse(product.properties)
    } catch {
      form.properties = []
    }
  } else if (Array.isArray(product.properties)) form.properties = [...product.properties]
  else form.properties = []
}

function showProductDetails(product) {
  selectedProduct.value = product
  isModalOpen.value = true
}

function closeModal() {
  isModalOpen.value = false
  selectedProduct.value = null
}

onMounted(() => {
  adminStore.getAllProducts()
  categoryStore.getAllCategories()
  console.log(adminStore.products)
})
</script>

<style scoped>
.product-container {
  padding: 30px;
  direction: rtl;
  font-family: 'Yekan', sans-serif;
  background-color: #f9f9f9;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-top: 20px;
  font-size: 14px;
  font-weight: 600;
}
.pagination-btn {
  background-color: #ffd700;
  color: #1a1a1a;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.3s;
}
.pagination-btn:hover:not(:disabled) {
  background-color: #e5c100;
}
.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.page-title {
  font-size: 24px;
  font-weight: 800;
  color: #1a1a1a;
  margin-bottom: 25px;
  border-bottom: 3px solid #ffd700;
  padding-bottom: 10px;
}

.form-title-section {
  font-size: 20px;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 20px;
}

.row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.col-half {
  flex: 0 0 calc(50% - 10px);
}

.col-full {
  flex: 0 0 100%;
}

.col-5 {
  flex: 0 0 calc(45% - 10px);
}

.col-2 {
  flex: 0 0 10%;
  display: flex;
  align-items: flex-end;
}

.label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.input,
.input[type='text'],
.input[type='number'],
.input.select,
textarea.input {
  width: 100%;
  padding: 12px 14px;
  font-family: 'Vazirmatn';
  font-size: 15px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #ffffff;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.input:focus,
textarea.input:focus,
.input.select:focus {
  border-color: #ffd700;
  outline: none;
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.25);
}
.input.select {
  appearance: none;
  background: #fff
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath fill='%23666' d='M0 0l5 6 5-6z'/%3E%3C/svg%3E")
    no-repeat left 12px center;
  background-size: 10px;
  cursor: pointer;
}
textarea.input {
  min-height: 48px;
  width: 100%;
  resize: vertical;
}

/* .image-preview {
  max-width: 120px;
  max-height: 120px;
  border: 2px solid #ffd700;
  padding: 5px;
  margin-top: 10px;
  border-radius: 8px;
  background: #f8f9fa;
  display: block;
  object-fit: cover;
} */

.properties-section {
  box-sizing: border-box;
  background-color: #fcfcfc;
  border: 1px solid #eee;
  border-radius: 10px;
  padding: 20px 20px 20px 0;
}

.section-title {
  font-size: 16px;
  font-weight: 700;
  color: #1a1a1a;
  margin-top: 0;
  margin-bottom: 15px;
}

.prop-row {
  margin-bottom: 10px;
  align-items: flex-end;
}

.remove-prop-btn-col {
  justify-content: flex-start;
}
.btn-remove-prop {
  background: transparent;
  color: #dc3545;
  padding: 0;
  font-size: 24px;
  margin-bottom: 1px;
}

.btn-add-prop {
  background-color: #ffd700;
  color: #1a1a1a;
  padding: 8px 15px;
  font-size: 14px;
  margin-top: 10px;
  transition: background-color 0.3s;
}

.btn-add-prop:hover {
  background-color: #1a1a1a;
  color: #ffd700;
  box-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);
}
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 15px;
  font-size: 14px;
  border-radius: 8px;
  cursor: pointer;
  border: 1px solid transparent;
  transition: all 0.3s ease;
  white-space: nowrap;
  gap: 5px;
}

.form-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}
.form-actions .btn {
  flex: 1;
  padding: 10px 0;
  font-size: 14px;
  border-radius: 8px;
}

.btn-submit {
  background-color: #ffd700;
  color: #1a1a1a;
  max-width: 200px;
}
.btn-submit:hover {
  background-color: #ffd700;
  box-shadow: none;
}

.btn-cancel {
  background-color: #6c757d;
  color: #fff;
  max-width: 200px;
}

.btn-cancel:hover {
  background-color: #6c757d;
  box-shadow: none;
}
.divider {
  margin: 30px 0;
  border: none;
  border-top: 1px dashed #ddd;
}

.table-wrapper {
  background-color: #ffffff;
  border-radius: 12px;
  overflow-x: auto;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  margin-bottom: 25px;
}

.custom-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  text-align: center;
}

.custom-table th,
.custom-table td {
  padding: 12px;
  vertical-align: middle;
  border-bottom: 1px solid #eee;
}

.custom-table th {
  background-color: #ffd700;
  color: #1a1a1a;
  font-weight: 700;
  font-size: 14px;
  white-space: nowrap;
}

.custom-table tr:hover td {
  background-color: #fcfcfc;
}

.product-img-thumb {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 6px;
  border: 1px solid #ddd;
}

.prop-list {
  list-style: none;
  margin: 0;
  padding: 0;
  text-align: right;
  font-size: 13px;
  max-height: 80px;
  overflow-y: auto;
}
.prop-list li strong {
  color: #1a1a1a;
}
.discount-cell {
  color: #dc3545;
  font-weight: 600;
}
.price-cell {
  font-weight: 700;
  color: #4a4a4a;
}
.description-cell {
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.actions-cell .btn {
  margin-left: 5px;
}

.btn-view {
  background-color: #5bc0de;
  color: #fff;
}
.btn-view:hover {
  background-color: #31b0d5;
}

.btn-edit {
  background-color: #ffd700;
  color: #1a1a1a;
}

.btn-edit:hover {
  background-color: #e5c100;
}

.btn-delete {
  background-color: #dc3545;
  color: #fff;
}

.btn-delete:hover {
  background-color: #c82333;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 30px;
  font-size: 16px;
  color: #aaaaaa;
}
.loading-state .fa-icon {
  margin-left: 10px;
  color: #ffd700;
}
.error-message {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  padding: 10px;
  border-radius: 8px;
  margin-top: 15px;
  text-align: center;
}
.success-message {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
  padding: 10px;
  border-radius: 8px;
  margin-top: 15px;
  text-align: center;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.modal-content {
  background-color: #ffffff;
  padding: 40px;
  border-radius: 15px;
  width: 90%;
  max-width: 550px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  position: relative;
  animation: slide-in 0.3s ease-out;
  direction: rtl;
}
.image-upload-area {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 15px;
  border: 2px dashed #ffd700;
  border-radius: 12px;
  background-color: #fcfcfc;
  transition: 0.3s;
}

.image-upload-area:hover {
  border-color: #ffc107;
  background-color: #fffbea;
}

.image-upload-area .label {
  font-weight: 600;
  font-size: 14px;
}

.file-input {
  border: none;
  padding: 6px 10px;
  cursor: pointer;
  border-radius: 8px;
  background-color: #fff;
  transition: 0.2s;
}

.file-input:hover {
  background-color: #f9f9f9;
}

.image-preview-wrapper,
.gallery-thumb {
  position: relative;
  display: inline-block;
}

.image-preview {
  width: 140px;
  height: 140px;
  object-fit: cover;
  border-radius: 10px;
  border: 2px solid #ffd700;
  padding: 4px;
  background: #f8f9fa;
  transition:
    transform 0.3s,
    box-shadow 0.3s;
}

.image-preview:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.gallery-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.remove-gallery,
.remove-image {
  position: absolute;
  top: -8px;
  right: -8px;
  background-color: #dc3545;
  color: #fff;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition:
    opacity 0.2s,
    transform 0.2s;
}

.image-preview-wrapper:hover .remove-image,
.gallery-thumb:hover .remove-gallery {
  opacity: 1;
  transform: scale(1.1);
}

.toggle-switch {
  position: relative;
  width: 50px;
  height: 24px;
  display: inline-block;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  border-radius: 24px;
  transition: 0.4s;
}

.slider:before {
  position: absolute;
  content: '';
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  border-radius: 50%;
  transition: 0.4s;
}

input:checked + .slider {
  background-color: #28a745; /* سبز برای فعال */
}

input:checked + .slider:before {
  transform: translateX(26px);
}

@keyframes slide-in {
  from {
    transform: translateY(-50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
.modal-images {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
}

.main-image-wrapper {
  width: 250px;
  height: 250px;
  border: 3px solid #ffd700;
  border-radius: 12px;
  overflow: hidden;
  flex-shrink: 0;
}

.main-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition:
    transform 0.3s,
    box-shadow 0.3s;
}

.main-image:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
}

.gallery-images {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}

.gallery-thumb {
  width: 70px;
  height: 70px;
  object-fit: cover;
  border: 2px solid #ddd;
  border-radius: 8px;
  transition:
    transform 0.2s,
    box-shadow 0.2s;
  cursor: pointer;
}

.gallery-thumb:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.modal-close-btn {
  position: absolute;
  top: 55px;
  left: 15px;
  background: none;
  border: none;
  font-size: 30px;
  cursor: pointer;
  color: #555;
  padding: 5px;
  line-height: 1;
  transition: color 0.2s;
}
.modal-close-btn:hover {
  color: #dc3545;
}

.product-modal-title {
  font-size: 26px;
  font-weight: 800;
  color: #1a1a1a;
  margin-bottom: 5px;
}

.modal-divider {
  border: none;
  border-top: 2px solid #ffd700;
  margin: 15px 0 25px 0;
}

.modal-main-info {
  display: flex;
  gap: 25px;
  align-items: flex-start;
  margin-bottom: 25px;
  padding-bottom: 20px;
  border-bottom: 1px dashed #ddd;
}

.modal-product-image {
  width: 150px;
  height: 150px;
  border-radius: 10px;
  object-fit: cover;
  border: 3px solid #ffd700;
  padding: 5px;
  background: #f8f8f8;
  flex-shrink: 0;
}

.modal-text-info {
  flex-grow: 1;
  text-align: right;
}

.modal-price {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
}
.modal-price span {
  font-size: 22px;
  font-weight: 900;
  color: #dc3545;
  display: block;
}

.modal-category {
  font-size: 15px;
  color: #6c757d;
  margin-bottom: 10px;
}
.modal-category span {
  font-weight: 700;
  color: #1a1a1a;
}

.modal-discount-tag {
  display: inline-block;
  background-color: #ffd700;
  color: #1a1a1a;
  padding: 5px 10px;
  border-radius: 5px;
  font-weight: 700;
  font-size: 14px;
  margin-top: 10px;
}

.modal-subtitle {
  font-size: 18px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 20px 0 10px 0;
  border-bottom: 2px solid #eee;
  padding-bottom: 5px;
}

.modal-description {
  font-size: 15px;
  color: #495057;
  line-height: 1.8;
  text-align: justify;
}

.prop-list-modal {
  list-style: none;
  margin: 0;
  padding: 0;
  font-size: 15px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px 20px;
  margin-top: 10px;
  text-align: right;
}
.prop-list-modal li strong {
  color: #1a1a1a;
  font-weight: 700;
  margin-left: 5px;
}

.modal-edit-btn {
  background-color: #343a40;
  color: #fff;
  border: none;
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border-radius: 8px;
  margin-top: 30px;
  cursor: pointer;
  transition: background-color 0.3s;
}
.modal-edit-btn:hover {
  background-color: #1a1a1a;
}

@media (max-width: 768px) {
  .modal-content {
    padding: 25px;
  }
  .modal-main-info {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  .modal-text-info {
    text-align: center;
  }
  .modal-price span {
    display: inline;
    margin-right: 5px;
  }
  .modal-product-image {
    width: 120px;
    height: 120px;
  }
  .prop-list-modal {
    grid-template-columns: 1fr;
  }
}
</style>
