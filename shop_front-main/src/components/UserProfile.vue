<template>
  <div class="profile-card">
    <h3>پروفایل کاربری</h3>

    <!-- تب‌ها -->
    <div class="profile-tabs">
      <button :class="{ active: tab === 'info' }" @click="tab = 'info'">
        مشخصات فردی
      </button>
      <button :class="{ active: tab === 'addresses' }" @click="tab = 'addresses'">
        آدرس‌ها
      </button>
      <button :class="{ active: tab === 'bank' }" @click="tab = 'bank'">
        حساب بانکی
      </button>
    </div>

    <!-- مشخصات فردی -->
    <!-- مشخصات فردی -->
    <div v-if="tab === 'info'">
      <ProfileInfo />
    </div>

    <!-- آدرس‌ها -->
    <div v-if="tab === 'addresses'" class="profile-form">
      <ProfileAddresses />
    </div>

    <!-- حساب بانکی -->
    <div v-if="tab === 'bank'">
      <BankAccounts />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import ProfileInfo from "@/components/ProfileInfo.vue";
import { useUserStore } from "@/stores/useUserStore";
import ProfileAddresses from "@/components/ProfileAddresses.vue";
import BankAccounts from "@/components/BankAccounts.vue";

const store = useUserStore();
const tab = ref("info");
const defaultAvatar = "/logos/default.png";
const DatePicker = ref(null);
const datePickerLoaded = ref(false);

onMounted(async () => {
  await Promise.all([
    store.fetchProfile(),
    store.fetchAddresses(),
    store.fetchBankAccounts(),
  ]);
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
/* ==== کارت اصلی ==== */
.profile-card {
  background: linear-gradient(180deg, #ffffff 0%, #fdfaf3 100%);
  border-radius: 20px;
  padding: 35px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.05);
  transition: 0.3s ease;
  animation: fadeIn 0.4s ease;
}

.profile-card h3 {
  text-align: center;
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 25px;
  color: #333;
}

/* ==== تب‌ها ==== */
.profile-tabs {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.profile-tabs button {
  padding: 10px 24px;
  border-radius: 25px;
  border: none;
  background: #f3f3f3;
  color: #555;
  font-weight: 600;
  cursor: pointer;
  transition: 0.3s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.profile-tabs button:hover {
  background: #fff8dc;
  color: #333;
}

.profile-tabs button.active {
  background: linear-gradient(135deg, #f9c710, #f8b900);
  color: white;
  box-shadow: 0 4px 10px rgba(249, 199, 16, 0.4);
  transform: translateY(-2px);
}

/* ==== فرم ==== */
.profile-form {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px 25px;
  background: #fafafa;
  padding: 25px;
  border-radius: 18px;
  box-shadow: inset 0 0 8px rgba(0, 0, 0, 0.03);
}

/* ==== آواتار ==== */
.avatar-section {
  grid-column: 1 / -1;
  text-align: center;
  margin-bottom: 15px;
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

.avatar-section img:hover {
  transform: scale(1.05);
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
  outline: none !important;
}

/* ==== فیلدها ==== */
.form-group {
  display: flex;
  flex-direction: column;
}

label {
  font-weight: 600;
  margin-bottom: 6px;
  color: #333;
}

input {
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid #ddd;
  background: white;
  transition: all 0.3s ease;
}
input:focus {
  border-color: #f8b900;
  box-shadow: 0 0 0 3px rgba(248, 185, 0, 0.2);
  outline: none;
}

/* ==== دکمه‌ها ==== */
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

/* ==== انیمیشن ==== */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ==== ریسپانسیو ==== */
@media (max-width: 768px) {
  .profile-form {
    grid-template-columns: 1fr;
    padding: 20px;
  }

  .profile-tabs {
    gap: 10px;
  }

  .profile-tabs button {
    padding: 8px 18px;
    font-size: 0.9rem;
  }

  .avatar-section img {
    width: 100px;
    height: 100px;
  }
}
</style>
