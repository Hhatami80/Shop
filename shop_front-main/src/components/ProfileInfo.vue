<template>
  <div class="profile-section">
    <h3>پروفایل کاربری</h3>

    
    <form @submit.prevent="saveProfile" class="profile-form" novalidate>
      
      <div class="avatar-section">
        <img
          :src="
            store.profile.previewImage ||
            (typeof store.profile.image === 'string' ? store.profile.image : defaultAvatar)
          "
          alt="profile"
          class="table-avatar"
        />
        <label class="upload-label" v-if="editing">
          <input type="file" accept="image/*" @change="onFileChange" />
          تغییر تصویر
        </label>
      </div>

      
      <div class="form-group">
        <label>نام کاربری:</label>
        <input v-model="store.profile.username" type="text" :disabled="!editing" />
        <span class="error" v-if="errors.username">{{ errors.username }}</span>
      </div>

      <div class="form-group">
        <label>نام:</label>
        <input v-model="store.profile.first_name" type="text" :disabled="!editing" />
        <span class="error" v-if="errors.first_name">{{ errors.first_name }}</span>
      </div>

      <div class="form-group">
        <label>نام خانوادگی:</label>
        <input v-model="store.profile.last_name" type="text" :disabled="!editing" />
        <span class="error" v-if="errors.last_name">{{ errors.last_name }}</span>
      </div>

      <div class="form-group">
        <label>ایمیل:</label>
        <input v-model="store.profile.email" type="email" :disabled="!editing" />
        <span class="error" v-if="errors.email">{{ errors.email }}</span>
      </div>

      <div class="form-group">
        <label>شماره تماس:</label>
        <input
          v-model="store.profile.phone"
          type="text"
          :disabled="!editing"
          placeholder="مثلاً 09121234567"
          @input="onPhoneInput"
        />
        <span class="error" v-if="errors.phone">{{ errors.phone }}</span>
      </div>

      <div class="form-group">
        <label>تاریخ تولد:</label>
        <component
          v-if="datePickerLoaded"
          :is="DatePicker"
          v-model="store.profile.birthdate"
          format="jYYYY/jMM/jDD"
          placeholder="انتخاب تاریخ"
          color="#f9c710"
          position="bottom"
          :disabled="!editing"
        />
      </div>

      <button type="submit" class="btn gold-btn" :disabled="!editing || saving">
        {{ saving ? 'در حال ذخیره ...' : 'ذخیره تغییرات' }}
      </button>
    </form>

 
    <h4>پیش‌نمایش اطلاعات</h4>
    <table class="preview-table">
      <thead>
        <tr>
          <th>نام کاربری</th>
          <th>نام</th>
          <th>نام خانوادگی</th>
          <th>ایمیل</th>
          <th>شماره تماس</th>
          <th>تاریخ تولد</th>
          <th>عکس</th>
          <th>عملیات</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>{{ store.profile.username }}</td>
          <td>{{ store.profile.first_name }}</td>
          <td>{{ store.profile.last_name }}</td>
          <td>{{ store.profile.email }}</td>
          <td>{{ store.profile.phone }}</td>
          <td>{{ birthdateShamsi }}</td>
          <td>
            <img
              v-if="store.profile.previewImage || store.profile.image"
              :src="store.profile.previewImage || store.profile.image"
              alt="profile"
              width="50"
              height="50"
              style="border-radius: 50%; object-fit: cover"
            />
            <span v-else>-</span>
          </td>
          <td>
            <button class="edit-btn" @click="editing = true">ویرایش</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/useUserStore'
import defaultAvatar from '@/assets/image/icons/avatar1.jpg'
import jalaali from 'jalaali-js'
import { toast } from 'vue3-toastify'

const store = useUserStore()
const DatePicker = ref(null)
const datePickerLoaded = ref(false)
const saving = ref(false)
const editing = ref(false)

const errors = reactive({
  username: '',
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
})


function toJalali(gDate) {
  if (!gDate) return ''
  const [gy, gm, gd] = gDate.split('-').map(Number)
  const { jy, jm, jd } = jalaali.toJalaali(gy, gm, gd)
  return `${jy}/${String(jm).padStart(2, '0')}/${String(jd).padStart(2, '0')}`
}

const birthdateShamsi = computed(() => {
  const date = store.profile.birthdate
  if (!date) return '-'
  if (date.includes('/')) return date
  return toJalali(date)
})


onMounted(async () => {
  const module = await import('vue3-persian-datetime-picker')
  DatePicker.value = module.default
  datePickerLoaded.value = true
  await store.fetchProfile()
})


const onPhoneInput = (e) => {
  let val = e.target.value.replace(/\D/g, '')
  if (val.length > 11) val = val.slice(0, 11)
  store.profile.phone = val
}


const onFileChange = (e) => {
  const file = e.target.files[0]
  if (!file) return
  store.profile.image = file
  store.profile.previewImage = URL.createObjectURL(file)
}


function validateForm() {
  let valid = true
  errors.username = store.profile.username ? '' : 'نام کاربری الزامی است'
  errors.first_name = store.profile.first_name ? '' : 'نام الزامی است'
  errors.last_name = store.profile.last_name ? '' : 'نام خانوادگی الزامی است'
  errors.email = /^\S+@\S+\.\S+$/.test(store.profile.email) ? '' : 'ایمیل معتبر نیست'
  errors.phone = /^\d{11}$/.test(store.profile.phone) ? '' : 'شماره تماس باید 11 رقم باشد'

  Object.values(errors).forEach((err) => {
    if (err) valid = false
  })
  return valid
}


const saveProfile = async () => {
  if (!validateForm()) {
    toast.error('لطفا فیلدهای فرم را بررسی کنید')
    return
  }
  saving.value = true
  try {
    const formData = new FormData()
    formData.append('username', store.profile.username)
    formData.append('first_name', store.profile.first_name)
    formData.append('last_name', store.profile.last_name)
    formData.append('email', store.profile.email)
    formData.append('phone', store.profile.phone)
    if (store.profile.birthdate) formData.append('birthdate', store.profile.birthdate)
    if (store.profile.image instanceof File) formData.append('image', store.profile.image)
    await store.updateProfile(formData)
    editing.value = false
  } catch {
    toast.error('خطا در ذخیره پروفایل')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.profile-section {
  display: flex;
  flex-direction: column;
  gap: 25px;
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

.profile-form {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px 25px;
  background: #fafafa;
  padding: 25px;
  border-radius: 18px;
  box-shadow: inset 0 0 8px rgba(0, 0, 0, 0.03);
  max-width: 800px;
  margin: 0 auto;
}

.avatar-section {
  grid-column: 1 / -1;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.avatar-section img {
  width: 130px;
  height: 130px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #f9c710;
  box-shadow: 0 4px 12px rgba(249, 199, 16, 0.3);
  transition: 0.3s ease;
}

.upload-label {
  margin-top: 10px;
  cursor: pointer;
  background: #fff8dc;
  border-radius: 20px;
  padding: 6px 16px;
  font-size: 0.9rem;
  font-weight: 600;
  color: #444;
  transition: 0.3s;
  border: 1px solid #f9c710;
}

.upload-label:hover {
  background: #f9c710;
  color: white;
}

.upload-label input {
  display: none;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  font-weight: 600;
  margin-bottom: 6px;
  color: #333;
}

input,
component {
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid #ddd;
  background: white;
  transition: all 0.3s ease;
  height: 42px;
  box-sizing: border-box;
}

input:focus,
component:focus {
  border-color: #f8b900;
  box-shadow: 0 0 0 3px rgba(248, 185, 0, 0.2);
  outline: none;
}

.btn {
  grid-column: 1 / -1;
  border: none;
  padding: 9px 0;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.gold-btn {
  background: linear-gradient(135deg, #f9c710, #f8b900);
  color: white;
  box-shadow: 0 4px 10px rgba(191, 162, 52, 0.4);
}

.gold-btn:hover {
  background: linear-gradient(135deg, #ffd740, #f9c710);
  transform: translateY(-2px);
  box-shadow: 0 6px 14px rgba(191, 162, 52, 0.5);
}

.preview-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  border-radius: 12px;
  overflow: hidden;
  margin-top: 25px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  background: #fff;
}

.preview-table th {
  background: linear-gradient(135deg, #f9c710, #f8b900);
  color: white;
  padding: 12px;
  font-size: 0.95rem;
  font-weight: 600;
}

.preview-table td {
  padding: 12px;
  text-align: center;
  border-bottom: 1px solid #f3f3f3;
  font-size: 0.9rem;
}

.preview-table tr:last-child td {
  border-bottom: none;
}

.preview-table tr:nth-child(even) td {
  background-color: #fffdf3;
}

.preview-table tr:hover td {
  background-color: #fff6d6;
  transition: 0.3s;
}

.table-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #f9c710;
  background: #fff8dc;
}
.error {
  color: #f44336;
  font-size: 0.8rem;
  margin-top: 4px;
}
.edit-btn {
  background: #f9c710;
  border: none;
  padding: 4px 10px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.8rem;
  transition: 0.3s;
}
.edit-btn:hover {
  background: #f8b900;
  color: white;
}
.table-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #f9c710;
  background: #fff8dc;
}
</style>
