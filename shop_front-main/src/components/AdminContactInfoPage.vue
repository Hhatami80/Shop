<template>
  <div class="admin-page">
    <div class="header">
      <h1>مدیریت اطلاعات تماس</h1>
      <p>در این بخش می‌توانید محتوای صفحه تماس با ما را مدیریت کنید.</p>
    </div>

    <div class="card">
      <form v-if="info" @submit.prevent="updateInfo">
        <div class="form-grid">
          <div class="form-group">
            <label>عنوان</label>
            <input v-model="info.title" type="text" />
          </div>

          <div class="form-group">
            <label>زیرعنوان</label>
            <input v-model="info.subtitle" type="text" />
          </div>

          <div class="form-group">
            <label>آدرس</label>
            <input v-model="info.address" type="text" />
          </div>

          <div class="form-group">
            <label>تلفن</label>
            <input v-model="info.phone" type="text" />
          </div>

          <div class="form-group">
            <label>ایمیل</label>
            <input v-model="info.email" type="email" />
          </div>

          <div class="form-group">
            <label>ساعت کاری</label>
            <input v-model="info.work_hours" type="text" />
          </div>
        </div>

        <h3 class="section-title">شبکه‌های اجتماعی</h3>

        <div class="form-group">
          <div class="social-input">
            <i class="fab fa-instagram"></i>
            <label>Instagram:</label>
            <input v-model="info.instagram" placeholder="https://instagram.com/yourpage" />
          </div>
        </div>
        <div class="form-group">
          <div class="social-input">
            <i class="fab fa-telegram"></i>
            <label>Telegram:</label>
            <input v-model="info.telegram" placeholder="https://t.me/yourpage" />
          </div>
        </div>

        <div class="form-group">
          <div class="social-input">
            <i class="fab fa-whatsapp"></i>
            <label>Whatsapp:</label>
            <input v-model="info.whatsapp" placeholder="https://wa.me/yourphone" />
          </div>
        </div>

        <button type="submit" class="submit-btn" :disabled="store.saving">
          {{ store.saving ? 'در حال ذخیره...' : 'ذخیره تغییرات' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useAdminContactInfoStore } from '@/stores/contactInfoAdminStore'

const store = useAdminContactInfoStore()

onMounted(() => {
  store.fetchInfo()
})

const info = computed(() => store.info)

async function updateInfo() {
  await store.updateInfo()
}
</script>

<style scoped>
.admin-page {
  direction: rtl;
  padding: 35px;
}

.header {
  margin-bottom: 25px;
}

.header h1 {
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 8px;
}

.header p {
  font-size: 14px;
  color: #555;
}

.card {
  background: #ffffff;
  padding: 25px;
  border-radius: 14px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 18px;
}

.form-group label {
  font-size: 14px;
  margin-bottom: 5px;
  display: block;
}

.form-group input {
  width: 85%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  outline: none;
  transition: border 0.2s;
}

.form-group input:focus {
  border-color: #facc15;
}

.section-title {
  margin: 25px 0 10px;
  font-size: 16px;
  font-weight: bold;
  color: #444;
}

.submit-btn {
  margin-top: 20px;
  background: #facc15;
  color: black;
  padding: 12px 25px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 15px;
  transition: 0.2s;
}

.submit-btn:hover {
  background: #e0b814;
}
.social-input {
  display: flex;
  width: 96%;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
}

.social-input i {
  font-size: 20px;
  color: #ffd700;
  width: 25px;
  text-align: center;
}

.social-input label {
  width: 90px;
  font-size: 14px;
}

.social-input input {
  flex: 1;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  outline: none;
  transition: border 0.2s;
}

.social-input input:focus {
  border-color: #facc15;
}
</style>
