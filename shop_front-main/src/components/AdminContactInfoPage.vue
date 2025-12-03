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
  --gold: #f9c710;
  --gold-hover: #e6b800;
  --gold-light: #fff9e6;
  --dark: #1a1a1a;
  --gray-100: #f8f9fa;
  --gray-200: #e9ecef;
  --gray-600: #6c757d;
  --gray-800: #343a40;
  --success: #10b981;

  font-family: 'IRANSansX', 'Vazirmatn', sans-serif;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ed 100%);
  min-height: 100vh;
  padding: 3rem 2rem;
  direction: rtl;
}


.header {
  text-align: center;
  margin-bottom: 3rem;
}

.header h1 {
  font-size: 2.4rem;
  font-weight: 900;
  color: var(--dark);
  margin: 0 0 1rem 0;
  position: relative;
  display: inline-block;
}

.header h1::after {
  content: '';
  position: absolute;
  bottom: -12px;
  left: 50%;
  transform: translateX(-50%);
  width: 140px;
  height: 6px;
  background: var(--gold);
  border-radius: 4px;
}

.header p {
  font-size: 1.15rem;
  color: #555;
  max-width: 700px;
  margin: 2rem auto 0;
  line-height: 1.7;
}


.card {
  background: #fff;
  padding: 2.5rem;
  border-radius: 28px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.12);
  max-width: 1000px;
  margin: 0 auto;
  border: 1px solid rgba(249, 199, 16, 0.15);
  backdrop-filter: blur(12px);
}


.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: 1.8rem;
  margin-bottom: 2.5rem;
}


.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.form-group label {
  font-weight: 700;
  color: var(--dark);
  font-size: 1.05rem;
  padding-right: 4px;
}


.form-group input {
  padding: 1rem 1.4rem;
  border: 2.2px solid #e0e0e0;
  border-radius: 18px;
  font-size: 1.05rem;
  transition: all 0.35s ease;
  background: #fdfdfd;
  color: var(--dark);
}

.form-group input:focus {
  outline: none;
  border-color: var(--gold);
  box-shadow: 0 0 0 5px rgba(249, 199, 16, 0.22);
  transform: translateY(-3px);
  background: #fff;
}


.section-title {
  font-size: 1.6rem;
  font-weight: 900;
  color: var(--dark);
  margin: 2.5rem 0 1.8rem;
  padding-bottom: 0.8rem;
  border-bottom: 3px solid var(--gold);
  display: inline-block;
}


.social-input {
  display: grid;
  grid-template-columns: 40px 110px 1fr;
  align-items: center;
  gap: 12px;
  padding: 0.9rem 1rem;
  background: var(--gold-light);
  border-radius: 18px;
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.social-input:hover {
  border-color: var(--gold);
  background: #fff;
  box-shadow: 0 8px 25px rgba(249, 199, 16, 0.15);
}

.social-input i {
  font-size: 1.6rem;
  color: var(--gold);
  justify-self: center;
}

.social-input label {
  font-weight: 700;
  color: var(--dark);
  font-size: 1rem;
}

.social-input input {
  background: transparent;
  border: none;
  outline: none;
  font-size: 1rem;
  color: var(--gray-800);
}

.social-input input::placeholder {
  color: #aaa;
  font-style: italic;
}


.fa-instagram { color: #e4405f; }
.fa-telegram { color: #0088cc; }
.fa-whatsapp { color: #25d366; }


.submit-btn {
  margin-top: 2.5rem;
  padding: 1.1rem 3rem;
  background: linear-gradient(135deg, var(--gold), var(--gold-hover));
  color: #111;
  border: none;
  border-radius: 20px;
  font-size: 1.2rem;
  font-weight: 900;
  cursor: pointer;
  transition: all 0.4s ease;
  box-shadow: 0 10px 30px rgba(249, 199, 16, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  min-width: 220px;
  margin-left: auto;
  margin-right: auto;
}

.submit-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #ffd700, var(--gold));
  transform: translateY(-5px);
  box-shadow: 0 18px 40px rgba(249, 199, 16, 0.5);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}


.submit-btn::after {
  content: '';
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid transparent;
  border-top: 3px solid #111;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-right: 10px;
  opacity: 0;
}

.submit-btn:disabled::after {
  opacity: 1;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .social-input {
    grid-template-columns: 40px 90px 1fr;
  }
  
  .submit-btn {
    width: 100%;
    max-width: 300px;
  }
  
  .header h1 {
    font-size: 2rem;
  }
}
</style>