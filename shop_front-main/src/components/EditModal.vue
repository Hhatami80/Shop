<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="modelValue" class="modal-backdrop" @click="$emit('update:modelValue', false)">
        <div class="modal-panel" @click.stop @keydown.esc="$emit('update:modelValue', false)">
          <div class="modal-header">
            <h3>ویرایش دسته‌بندی</h3>
            <button class="close-btn" @click="$emit('update:modelValue', false)">
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

          <div class="modal-body">
            <form @submit.prevent="submitEdit" class="edit-form">
              <div class="form-group">
                <label>تصویر اصلی دسته</label>
                <div class="main-image-upload">
                  <div v-if="previewImage" class="image-preview">
                    <img :src="previewImage" alt="پیش‌نمایش" />
                  </div>
                  <label class="upload-label">
                    <span>{{ previewImage ? 'تغییر تصویر' : 'انتخاب تصویر' }}</span>
                    <input type="file" accept="image/*" @change="handleImageChange" />
                  </label>
                </div>
              </div>

              <div class="form-group">
                <label>عنوان دسته‌بندی</label>
                <input
                  v-model="editedTitle"
                  type="text"
                  placeholder="مثلاً: لپ‌تاپ و کامپیوتر"
                  required
                />
              </div>

              <hr class="divider" />

              <div class="banners-section">
                <div class="section-header">
                  <h4>بنرهای تبلیغاتی دسته</h4>
                  <button type="button" class="btn-add" @click="addBanner">افزودن بنر جدید</button>
                </div>

                <div class="banners-list">
                  <div v-for="(banner, index) in localBanners" :key="index" class="banner-item">
                    <div class="banner-preview">
                      <img v-if="banner.preview" :src="banner.preview" alt="بنر" />
                      <div v-else class="placeholder">
                        <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
                          <rect
                            x="3"
                            y="3"
                            width="18"
                            height="18"
                            rx="2"
                            stroke="currentColor"
                            stroke-width="1.5"
                          />
                          <circle cx="8" cy="8" r="2" fill="currentColor" />
                          <path d="M21 15L16 10L5 21" stroke="currentColor" stroke-width="1.5" />
                        </svg>
                        <span>بدون تصویر</span>
                      </div>

                      <label class="upload-btn">
                        تغییر
                        <input
                          type="file"
                          accept="image/*"
                          @change="(e) => handleBannerFile(e, index)"
                        />
                      </label>
                    </div>

                    <input
                      v-model="banner.text"
                      type="text"
                      placeholder="متن روی بنر (اختیاری)"
                      class="banner-text"
                    />

                    <button
                      type="button"
                      class="btn-remove"
                      @click="removeBanner(index)"
                      title="حذف بنر"
                    >
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                        <path
                          d="M3 6H5H21"
                          stroke="currentColor"
                          stroke-width="2"
                          stroke-linecap="round"
                        />
                        <path
                          d="M8 6V4C8 3.447 8.447 3 9 3H15C15.553 3 16 3.447 16 4V6M19 6V20C19 21.105 18.105 22 17 22H7C5.895 22 5 21.105 5 20V6H19Z"
                          stroke="currentColor"
                          stroke-width="2"
                        />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </form>
          </div>

          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="$emit('update:modelValue', false)">
              انصراف
            </button>
            <button
              type="submit"
              class="btn-save"
              @click="submitEdit"
              :disabled="!editedTitle.trim()"
            >
              ذخیره تغییرات
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue'
import {useCategoryBannerStore} from '@/stores/useCatBannerStore'
const catBannerStore = useCategoryBannerStore();
const props = defineProps({
  modelValue: Boolean,
  category: Object,
})

const emit = defineEmits(['update:modelValue', 'save'])

const editedTitle = ref('')
const imageFile = ref(null)
const previewImage = ref(null)
const localBanners = ref([])

watch(
  () => props.category,
  (cat) => {
    if (cat) {
      editedTitle.value = cat.title || ''
      previewImage.value = cat.image || null
      localBanners.value = (cat.banner_images || []).map((b) => ({
        id: b.id || null,
        text: b.text || '',
        file: null,
        preview: b.image || null,
      }))
    }
  },
  { immediate: true },
)

const handleImageChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    imageFile.value = file
    previewImage.value = URL.createObjectURL(file)
  }
}

const handleBannerFile = (e, index) => {
  const file = e.target.files[0]
  if (file) {
    localBanners.value[index].file = file
    localBanners.value[index].preview = URL.createObjectURL(file)
  }
}

const addBanner = () => {
  localBanners.value.push({ id: null, text: '', file: null, preview: null })
}

const removeBanner = (index) => {
  localBanners.value.splice(index, 1)
}

const submitEdit = async () => {
  // 1) ذخیره خود دسته (عکس + عنوان)
  const form = new FormData()
  form.append('title', editedTitle.value)
  if (imageFile.value) form.append('image', imageFile.value)

  // این emit مربوط به ذخیره خود دسته است
  emit('save', { id: props.category.id, formData: form })


  // 2) مقایسه بنرهای جدید و قدیمی
  const oldBanners = props.category.banner_images || []
  const newBanners = localBanners.value

  // پیدا کردن بنرهای حذف‌شده
  const deleted = oldBanners.filter(
    old => !newBanners.find(n => n.id === old.id)
  )

  // پیدا کردن بنرهای جدید (id ندارد)
  const added = newBanners.filter(b => !b.id)

  // پیدا کردن بنرهای ویرایش‌شده
  const updated = newBanners.filter(b => b.id)


  // --- 3) حذف بنرهای حذف‌شده ---
  for (const b of deleted) {
    await catBannerStore.deleteBanner(props.category.id, b.id)
  }

  // --- 4) اضافه کردن بنرهای جدید ---
  for (const b of added) {
    const fd = new FormData()
    if (b.file) fd.append('image', b.file)
    fd.append('text', b.text || '')
    await catBannerStore.addBanner(props.category.id, fd)
  }

  // --- 5) آپدیت بنرهای قدیمی ---
  for (const b of updated) {
    const fd = new FormData()
    fd.append('text', b.text || '')
    if (b.file) fd.append('image', b.file)
    await catBannerStore.updateBanner(props.category.id, b.id, fd)
  }


  emit('update:modelValue', false)
}

</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-from .modal-panel,
.modal-leave-to .modal-panel {
  transform: scale(0.9);
}

.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(6px);
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
  max-width: 520px;
  height: auto;
  max-height: 92vh;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  direction: rtl;
  font-family: 'IRANSansX', sans-serif;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 1.5rem 1.5rem 1rem;
  background: linear-gradient(135deg, #f9c710, #e6b800);
  color: #111;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.5rem;
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
  background: rgba(255, 255, 255, 0.3);
}

.modal-body {
  padding: 1.5rem;
  flex: 1;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.form-group label {
  font-weight: 700;
  color: #222;
  font-size: 0.95rem;
}

.main-image-upload {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 2px dashed #ddd;
  border-radius: 16px;
  background: #fafafa;
}

.image-preview img {
  max-width: 160px;
  max-height: 160px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.upload-label {
  cursor: pointer;
  background: #f9c710;
  color: #111;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-weight: 700;
  transition: 0.3s;
}

.upload-label:hover {
  background: #e6b800;
}
.upload-label input {
  display: none;
}

input[type='text'] {
  padding: 0.9rem 1rem;
  border: 1.8px solid #e0e0e0;
  border-radius: 12px;
  font-size: 1rem;
  transition: 0.3s;
  background: #fdfdfd;
}

input:focus {
  outline: none;
  border-color: #f9c710;
  box-shadow: 0 0 0 4px rgba(249, 199, 16, 0.2);
}

.divider {
  border: none;
  height: 1px;
  background: linear-gradient(to right, transparent, #ddd, transparent);
  margin: 1.5rem 0;
}

.banners-section .section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.banners-section h4 {
  margin: 0;
  color: #222;
  font-size: 1.2rem;
}

.btn-add {
  background: #10b981;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-add:hover {
  background: #059669;
}

.banners-list {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.banner-item {
  background: #fdfdfd;
  border: 1.8px solid #eee;
  border-radius: 16px;
  padding: 1rem;
  display: grid;
  grid-template-columns: 120px 1fr auto;
  gap: 1rem;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.banner-preview {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  background: #f5f5f5;
}

.banner-preview img {
  width: 100%;
  height: 80px;
  object-fit: cover;
}

.placeholder {
  height: 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #aaa;
  font-size: 0.8rem;
  gap: 0.5rem;
}

.upload-btn {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(249, 199, 16, 0.9);
  color: #111;
  text-align: center;
  padding: 6px;
  font-size: 0.8rem;
  font-weight: 700;
  cursor: pointer;
  transition: 0.2s;
}

.upload-btn:hover {
  background: #f9c710;
}
.upload-btn input {
  display: none;
}

.banner-text {
  padding: 0.7rem;
  border: 1.5px solid #ddd;
  border-radius: 10px;
  font-size: 0.95rem;
}

.btn-remove {
  background: #ef4444;
  color: white;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-remove:hover {
  background: #dc2626;
}

.modal-footer {
  padding: 1.2rem 1.5rem;
  background: #f9fafb;
  border-top: 1px solid #eee;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  flex-shrink: 0;
  position: sticky;
  bottom: 0;
  z-index: 10;
}

.btn-cancel {
  padding: 0.8rem 1.5rem;
  background: #f3f4f6;
  color: #666;
  border: 1.5px solid #ddd;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
}

.btn-save {
  background: #f9c710;
  min-width: 110px;
  padding: 0.9rem 1.2rem !important;
  font-size: 1rem !important;
  color: #111;
  border: none;
  border-radius: 12px;
  font-weight: 900;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(249, 199, 16, 0.4);
}
.btn-cancel {
  min-width: 110px;
  background-color: red;
  color: #e0e0e0;
  padding: 0.9rem 1.2rem !important;
  font-size: 1rem !important;
}

.btn-save:hover {
  background: #e6b800;
  transform: translateY(-2px);
}
.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
@media screen and (max-width: 480px), (max-height: 600px) {
  .modal-panel {
    max-height: 95vh;
    border-radius: 16px;
  }
  .modal-header h3 {
    font-size: 1.3rem;
  }
  .modal-footer {
    padding: 1rem;
  }
  .btn-save,
  .btn-cancel {
    padding: 0.8rem 1rem;
    font-size: 0.95rem;
  }
}
</style>
