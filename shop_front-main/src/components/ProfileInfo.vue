<template>
  <div class="profile-section">
    <h3>فرم پروفایل</h3>

    <!-- فرم پروفایل -->
    <form @submit.prevent="saveProfile" class="profile-form">
      <div class="avatar-section">
        <img :src="store.profile.imageUrl || defaultAvatar" alt="Profile" />
        <label class="upload-label">
          <input type="file" accept="image/*" @change="onFileChange" />
          تغییر تصویر
        </label>
      </div>

      <div class="form-group">
        <label>نام:</label>
        <input
          v-model="store.profile.username"
          type="text"
          placeholder="مثلاً رضا رضایی"
        />
      </div>

      <div class="form-group">
        <label>ایمیل:</label>
        <input
          v-model="store.profile.email"
          type="email"
          placeholder="example@mail.com"
        />
      </div>

      <div class="form-group">
        <label>شماره تماس:</label>
        <input
          v-model="store.profile.phone"
          type="text"
          placeholder="مثلاً 09121234567"
        />
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
        />
      </div>

      <button type="submit" class="btn gold-btn">ذخیره تغییرات</button>
    </form>

    <!-- جدول پیش‌نمایش -->
    <h4>پیش‌نمایش مقادیر فرم</h4>
    <table class="preview-table">
      <thead>
        <tr>
          <th>نام</th>
          <th>ایمیل</th>
          <th>شماره تماس</th>
          <th>تاریخ تولد</th>
          <th>ویرایش</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>{{ store.profile.username }}</td>
          <td>{{ store.profile.email }}</td>
          <td>{{ store.profile.phone }}</td>
          <td>{{ store.profile.birthdate }}</td>
          <td><button class="btn edit-btn">ویرایش</button></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useUserStore } from "@/stores/useUserStore";

const store = useUserStore();
const defaultAvatar = "/logos/default.png";

const DatePicker = ref(null);
const datePickerLoaded = ref(false);

onMounted(async () => {
  const module = await import("vue3-persian-datetime-picker");
  DatePicker.value = module.default;
  datePickerLoaded.value = true;
});

const onFileChange = (e) => {
  const file = e.target.files[0];
  if (file) {
    store.updateProfileImage(file);
  }
};

const saveProfile = async () => {
  const formData = new FormData();
  formData.append("username", store.profile.username);
  formData.append("email", store.profile.email);
  formData.append("phone", store.profile.phone);
  formData.append("birthdate", store.profile.birthdate);
  if (store.profile.image instanceof File) formData.append("image", store.profile.image);

  await store.updateProfile(formData);
};
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

/* فرم پروفایل */
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

/* جدول پیش‌نمایش */
.preview-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.preview-table th,
.preview-table td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
  font-size: 0.9rem;
  border-radius: 6px;
}

.preview-table th {
  background: linear-gradient(135deg, #f9c710, #f8b900);
  color: white;
}

.preview-table td {
  background: #f9f9f9;
}

.preview-table td button {
  background-color: #f8b900;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.preview-table td button:hover {
  background-color: #f9c710;
}
</style>
