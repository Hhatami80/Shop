<template>
  <div class="contact-page">
    <div v-if="loading" class="loading-box">در حال بارگذاری...</div>

    <div v-if="error" class="error-box">
      {{ error }}
    </div>

    <div v-if="info" class="content">
      <section class="contact-header">
        <h1>{{ info.title }}</h1>
        <p>{{ info.subtitle }}</p>
      </section>

      <section class="contact-container">
        <div class="contact-form">
          <h2>فرم تماس</h2>
          <form @submit.prevent="submitForm">
            <div class="form-group">
              <label>نام شما</label>
              <input v-model="form.name" type="text" required />
            </div>

            <div class="form-group">
              <label>ایمیل</label>
              <input v-model="form.email" type="email" required />
            </div>

            <div class="form-group">
              <label>پیام شما</label>
              <textarea v-model="form.message" rows="4" required></textarea>
            </div>

            <button type="submit" class="submit-btn" :disabled="loadingSubmit">
              <span v-if="!loadingSubmit">ارسال پیام</span>
              <span v-else>در حال ارسال...</span>
            </button>
          </form>
        </div>

        <div class="contact-info">
          <h2>اطلاعات تماس</h2>
          <ul>
            <li><i class="fas fa-map-marker-alt"></i> {{ info.address }}</li>

            <li>
              <i class="fas fa-phone"></i>
              <a :href="`tel:${info.phone}`">{{ info.phone }}</a>
            </li>

            <li>
              <i class="fas fa-envelope"></i>
              <a :href="`mailto:${info.email}`">{{ info.email }}</a>
            </li>

            <li><i class="fas fa-clock"></i> {{ info.work_hours }}</li>
          </ul>

          <div class="social-icons">
            <a v-if="info.instagram" :href="info.instagram"><i class="fab fa-instagram"></i></a>
            <a v-if="info.telegram" :href="info.telegram"><i class="fab fa-telegram"></i></a>
            <a v-if="info.whatsapp" :href="info.whatsapp"><i class="fab fa-whatsapp"></i></a>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { contactService } from '@/services/contactService'
import { useContactStore } from '@/stores/contactStore'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

const store = useContactStore()

const form = ref({
  name: '',
  email: '',
  message: '',
})

const loadingSubmit = ref(false)

async function submitForm() {
  if (!form.value.name || !form.value.email || !form.value.message) {
    toast.error('لطفاً تمام فیلدها را پر کنید.')
    return
  }

  try {
    loadingSubmit.value = true

    await contactService.sendMessage({
      name: form.value.name,
      email: form.value.email,
      message: form.value.message,
    })

    toast.success('پیام شما با موفقیت ارسال شد')
    form.value = { name: '', email: '', message: '' }
  } catch (err) {
    toast.error('خطا در ارسال پیام')
  } finally {
    loadingSubmit.value = false
  }
}

onMounted(() => {
  store.fetchInfo()
})

const info = computed(() => store.info)
const loading = computed(() => store.loading)
const error = computed(() => store.error)
</script>

<style scoped>
.contact-page {
  direction: rtl;
  color: #2b2b2b;
  background-color: #fff;
}
.contact-header {
  margin-top: 40px;
  text-align: center;
  padding: 60px 20px 40px;
  background: linear-gradient(135deg, #ffd700 0%, #e5c100 100%);
  color: white;
}
.contact-header h1 {
  font-size: 2.2rem;
  font-weight: bold;
  margin-bottom: 10px;
}
.contact-header p {
  font-size: 1.1rem;
  opacity: 0.9;
}
.contact-container {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 40px;
  padding: 60px 100px;
}
.contact-form,
.contact-info {
  background: #fafafa;
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.06);
}
.contact-form h2,
.contact-info h2 {
  font-size: 1.3rem;
  font-weight: bold;
  color: #ffd700;
  margin-bottom: 20px;
}
.form-group {
  margin-bottom: 18px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
label {
  font-size: 14px;
  margin-bottom: 6px;
}
input,
textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ccc;
  border-radius: 10px;
  font-family: inherit;
  font-size: 14px;
  transition: all 0.3s ease;
}
input:focus,
textarea:focus {
  outline: none;
  border-color: #ffd700;
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.2);
}
.submit-btn {
  background: linear-gradient(135deg, #ffd700 0%, #e5c100 100%);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 12px 25px;
  cursor: pointer;
  font-size: 15px;
  transition: all 0.3s ease;
}
.submit-btn:hover {
  background: linear-gradient(135deg, #e5c100 0%, #c9aa00 100%);
}
.contact-info ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.contact-info li {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
  font-size: 14px;
}
.contact-info i {
  color: #ffd700;
  font-size: 18px;
}
.contact-info a {
  color: #2b2b2b;
  text-decoration: none;
}
.contact-info a:hover {
  color: #c9aa00;
}
.social-icons {
  margin-top: 25px;
  color: black;
  display: flex;
  gap: 15px;
}
.social-icons a {
  background: #ffd700;
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s ease;
}
.social-icons a i {
  color: black;
  font-size: 18px;
  transition: color 0.3s ease;
}
.social-icons a:hover {
  background: #c9aa00;
}
.social-icons a:hover i {
  color: black;
}
.map-section {
  margin: 40px 0 0 0;
  border-top: 1px solid #eee;
}
@media (max-width: 950px) {
  .contact-container {
    grid-template-columns: 1fr;
    padding: 40px 30px;
  }
  .contact-form,
  .contact-info {
    padding: 25px;
  }
}
</style>
