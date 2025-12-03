<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="modelValue" class="modal-backdrop" @click="$emit('update:modelValue', false)">
        <div class="modal-panel" @click.stop>
          <div class="modal-header">
            <h3>افزودن / ویرایش بنرها</h3>
            <button class="close-btn" @click="$emit('update:modelValue', false)" tabindex="0">
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
            <div class="banners-table-container">
              <table class="banners-table">
                <thead>
                  <tr>
                    <th>فایل بنر</th>
                    <th>متن روی بنر</th>
                    <th width="100">عملیات</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(item, index) in localBanners" :key="index">
                    <td class="file-cell">
                      <label class="file-upload-label">
                        <span v-if="item.file?.name">{{ item.file.name }}</span>
                        <span v-else class="placeholder-text">انتخاب فایل...</span>
                        <input
                          type="file"
                          accept="image/*"
                          @change="(e) => handleFileUpload(e, index)"
                        />
                      </label>
                    </td>
                    <td>
                      <input
                        v-model="item.text"
                        type="text"
                        placeholder="مثلاً: تخفیف ویژه تا ۵۰٪"
                        class="text-input"
                      />
                    </td>
                    <td class="action-cell">
                      <button class="btn-remove" @click="removeBanner(index)" title="حذف بنر">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                          <path
                            d="M3 6H21M10 11V17M14 11V17M5 6L6 19C6 20.104 6.895 21 8 21H16C17.105 21 18 20.104 18 19L19 6M9 6V4C9 3.448 9.448 3 10 3H14C14.552 3 15 3.448 15 4V6"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                          />
                        </svg>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>

              <div v-if="localBanners.length === 0" class="empty-state">
                <p>هنوز بنری اضافه نشده است</p>
                <small>با دکمه زیر شروع کنید</small>
              </div>
            </div>

            <button class="btn-add-banner" @click="addBanner">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path
                  d="M12 5V19M5 12H19"
                  stroke="currentColor"
                  stroke-width="2.5"
                  stroke-linecap="round"
                />
              </svg>
              افزودن بنر جدید
            </button>
          </div>

          <div class="modal-footer">
            <button class="btn-cancel" @click="$emit('update:modelValue', false)">لغو</button>
            <button class="btn-save" @click="saveChanges" :disabled="localBanners.length === 0">
              ذخیره بنرها
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: Boolean,
  banners: Array,
})

const emit = defineEmits(['update:modelValue', 'update'])

const localBanners = ref([])

watch(
  () => props.banners,
  (val) => {
    localBanners.value = val ? JSON.parse(JSON.stringify(val)) : []
  },
  { immediate: true },
)

const addBanner = () => {
  localBanners.value.push({ file: null, text: '' })
}

const removeBanner = (index) => {
  localBanners.value.splice(index, 1)
}

const handleFileUpload = (e, index) => {
  const file = e.target.files[0]
  if (file) {
    localBanners.value[index].file = file
  }
}

const saveChanges = () => {
  emit('update', localBanners.value)
  emit('update:modelValue', false)
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: all 0.32s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-from .modal-panel,
.modal-leave-to .modal-panel {
  transform: scale(0.92);
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
  max-width: 760px;
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
  padding: 1.5rem 1.8rem;
  background: #fdfdfd;
}

.banners-table-container {
  margin-bottom: 1.5rem;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
  background: #fff;
}

.banners-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
}

.banners-table th {
  background: #f8f9fa;
  padding: 1rem 0.8rem;
  font-weight: 700;
  color: #222;
  font-size: 0.95rem;
  border-bottom: 2px solid #f9c710;
}

.banners-table td {
  padding: 0.9rem 0.8rem;
  border-bottom: 1px solid #eee;
  vertical-align: middle;
}

.file-upload-label {
  display: block;
  padding: 0.75rem 1rem;
  background: #f5f5f5;
  border: 2px dashed #ccc;
  border-radius: 12px;
  cursor: pointer;
  text-align: center;
  transition: all 0.3s;
  font-size: 0.9rem;
  color: #555;
}

.file-upload-label:hover {
  border-color: #f9c710;
  background: #fff9e6;
}

.file-upload-label input {
  display: none;
}

.placeholder-text {
  color: #999;
  font-style: italic;
}

.text-input {
  width: 100%;
  padding: 0.8rem 1rem;
  border: 1.8px solid #e0e0e0;
  border-radius: 12px;
  font-size: 0.95rem;
  transition: 0.3s;
}

.text-input:focus {
  outline: none;
  border-color: #f9c710;
  box-shadow: 0 0 0 4px rgba(249, 199, 16, 0.18);
}

.btn-remove {
  background: #ef4444;
  color: white;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: 0.3s;
  margin-right: 30px;
}

.btn-remove:hover {
  background: #dc2626;
  transform: scale(1.08);
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #888;
}

.empty-state p {
  margin: 0 0 0.5rem;
  font-size: 1.1rem;
}
.empty-state small {
  font-size: 0.9rem;
}

.btn-add-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0.9rem 1.6rem;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 14px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: 0.3s;
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
}

.btn-add-banner:hover {
  background: #059669;
  transform: translateY(-2px);
}

.modal-footer {
  padding: 1.4rem 1.8rem;
  background: #f9fafb;
  border-top: 1px solid #eee;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  flex-shrink: 0;
}

.btn-cancel {
  padding: 0.85rem 1.8rem;
  background: #f3f4f6;
  color: #666;
  border: 1.5px solid #ddd;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.3s;
}

.btn-cancel:hover {
  background: #e5e7eb;
}

.btn-save {
  padding: 0.85rem 2.2rem;
  background: #f9c710;
  color: #111;
  border: none;
  border-radius: 12px;
  font-weight: 900;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(249, 199, 16, 0.4);
  transition: 0.3s;
}

.btn-save:hover:not(:disabled) {
  background: #e6b800;
  transform: translateY(-3px);
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}
</style>
