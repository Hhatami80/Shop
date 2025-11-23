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
import { ref, onMounted , computed } from 'vue'
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

    toast.success('پیام شما با موفقیت ارسال شد!')
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
.loading-box {
  text-align: center;
  padding: 30px;
  font-size: 18px;
}

.error-box {
  margin-top: 30px;
  text-align: center;
  padding: 20px;
  color: red;
}

.contact-page {
  direction: rtl;
  background-color: white;
  min-height: 100vh;
}

.contact-header {
  text-align: center;
  padding: 60px 20px;
  background: linear-gradient(135deg, #ffd700, #e5c100);
  color: white;
}

.contact-container {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 40px;
  padding: 50px 100px;
}

.contact-form,
.contact-info {
  background: #fafafa;
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.06);
}

.form-group {
  margin-bottom: 20px;
}

.submit-btn {
  background: #ffd700;
  color: white;
  padding: 12px 25px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
}
.social-icons {
  margin-top: 20px;
  display: flex;
  gap: 15px;
}

.social-icons a {
  width: 38px;
  height: 38px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #ffd700;
  border-radius: 50%;
}

@media (max-width: 950px) {
  .contact-container {
    grid-template-columns: 1fr;
    padding: 30px;
  }
}
</style>
