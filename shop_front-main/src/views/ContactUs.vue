<template>
  <div class="contact-page">
    <section class="contact-header">
      <h1>تماس با ما</h1>
      <p>خوشحال می‌شویم از شنیدن نظرات و پیشنهادات شما</p>
    </section>

    <section class="contact-container">
      <div class="contact-form">
        <h2>فرم تماس</h2>
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label for="name">نام شما</label>
            <input
              v-model="form.name"
              id="name"
              type="text"
              placeholder="نام خود را وارد کنید"
              required
            />
          </div>

          <div class="form-group">
            <label for="email">ایمیل</label>
            <input
              v-model="form.email"
              id="email"
              type="email"
              placeholder="example@gmail.com"
              required
            />
          </div>

          <div class="form-group">
            <label for="message">پیام شما</label>
            <textarea
              v-model="form.message"
              id="message"
              rows="5"
              placeholder="متن پیام..."
              required
            ></textarea>
          </div>

          <button type="submit" class="submit-btn">ارسال پیام</button>
        </form>
      </div>

      <div class="contact-info">
        <h2>اطلاعات تماس</h2>
        <ul>
          <li>
            <i class="fas fa-map-marker-alt"></i> تهران، خیابان ولیعصر، کوچه بهار، پلاک ۲۳
          </li>
          <li>
            <i class="fas fa-phone"></i> <a href="tel:+982112345678">۰۲۱-۱۲۳۴۵۶۷۸</a>
          </li>
          <li>
            <i class="fas fa-envelope"></i>
            <a href="mailto:info@coffeehouse.ir">info@coffeehouse.ir</a>
          </li>
          <li><i class="fas fa-clock"></i> ساعت کاری: شنبه تا چهارشنبه، ۹ تا ۱۸</li>
        </ul>

        <div class="social-icons">
          <a href="#" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
          <a href="#" aria-label="Telegram"><i class="fab fa-telegram"></i></a>
          <a href="#" aria-label="Whatsapp"><i class="fab fa-whatsapp"></i></a>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

const form = ref({ name: "", email: "", message: "" });

function submitForm() {
  if (!form.value.name || !form.value.email || !form.value.message) {
    toast.error("لطفاً تمام فیلدها را پر کنید.");
    return;
  }
  toast.success("پیام شما با موفقیت ارسال شد!");
  form.value = { name: "", email: "", message: "" };
}
</script>

<style scoped>
.contact-page {
  direction: rtl;
  font-family: "Yekan", sans-serif;
  color: #2b2b2b;
  background-color: #fff;
}

.contact-header {
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
  font-family: "Yekan", sans-serif;
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
