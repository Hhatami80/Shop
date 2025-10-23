<template>
  <main class="wrapper default">
    <div class="container">
      <div class="main-content">
        <header class="card-header">
          <h3 class="card-title">
            <span v-if="step === 'request'">بازیابی رمز عبور</span>
            <span v-else-if="step === 'verify'">تأیید کد ارسال شده</span>
            <span v-else>تعیین رمز عبور جدید</span>
          </h3>
        </header>

        <div class="forgot_box">
          <form v-if="step === 'request'" @submit.prevent="sendResetRequest">
            <div class="form-group">
              <label class="form-account-title"><span>*</span> شماره تماس یا ایمیل</label>
              <input
                class="input_second input_all"
                type="text"
                placeholder="شماره تماس یا ایمیل خود را وارد کنید"
                v-model="forgotInput"
              />
            </div>
            <div class="text-center">
              <button type="submit" class="btn btn-main-masai">ارسال کد بازیابی</button>
            </div>
            <div class="footer_login_reg text-center">
              <router-link to="/login">بازگشت به صفحه ورود</router-link>
            </div>
          </form>

          <form v-else-if="step === 'verify'" @submit.prevent="verifyCode">
            <div class="form-group">
              <label class="form-account-title"><span>*</span> کد ارسال شده</label>
              <input
                class="input_second input_all"
                type="text"
                placeholder="کد ارسال شده را وارد کنید"
                v-model="otpCode"
              />
            </div>
            <div class="text-center">
              <button type="submit" class="btn btn-main-masai">تایید کد</button>
            </div>
          </form>

          <form v-else @submit.prevent="resetPassword">
            <div class="form-group password-wrapper">
              <label class="form-account-title"><span>*</span> رمز عبور جدید</label>
              <input
                :type="showPassword ? 'text' : 'password'"
                class="input_second input_all"
                placeholder="رمز عبور جدید"
                v-model="newPassword"
              />
              <i
                :class="['fa', showPassword ? 'fa-eye-slash' : 'fa-eye', 'toggle-password']"
                @click="showPassword = !showPassword"
              ></i>
            </div>
            <div class="text-center">
              <button type="submit" class="btn btn-main-masai">تغییر رمز عبور</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useForgotPasswordStore } from '@/stores/useForgotPasswordStore'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'


const forgotStore = useForgotPasswordStore()
const { step } = storeToRefs(forgotStore)
const router = useRouter()


const forgotInput = ref('')
const otpCode = ref('')
const newPassword = ref('')
const showPassword = ref(false)

const sendResetRequest = async () => {
  const success = await forgotStore.requestReset(forgotInput.value)
  if (success) toast.success('کد بازیابی ارسال شد')
  else toast.error('خطا در ارسال کد بازیابی')
}

const verifyCode = async () => {
  const success = await forgotStore.verifyCode(otpCode.value)
  if (success) toast.success('کد تایید شد')
  else toast.error('کد وارد شده صحیح نیست')
}

const resetPassword = async () => {
  const success = await forgotStore.resetPassword(newPassword.value)
  if (success) {
    toast.success('رمز عبور با موفقیت تغییر یافت')
    router.push('/login')
  } else toast.error('خطا در تغییر رمز عبور')
}
</script>

<style scoped>
*,
*::before,
*::after {
  box-sizing: border-box;
}

.wrapper {
  direction: rtl;
  background-color: #f9f9f9;
  min-height: 100vh;
  padding: 60px 20px;
  font-family: 'Yekan', sans-serif;
  color: #333;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.container {
  max-width: 420px;
  width: 100%;
}

.main-content {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.1);
  padding: 32px 28px;
  animation: floatIn 0.6s ease forwards;
}

@keyframes floatIn {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.card-header {
  text-align: center;
  margin-bottom: 28px;
}

.card-title {
  font-size: 22px;
  font-weight: bold;
  color: #333;
}

.form-group {
  margin-bottom: 18px;
  display: flex;
  flex-direction: column;
}

.form-account-title {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 6px;
  color: #444;
}

.form-account-title span {
  color: #e53935;
  margin-left: 4px;
}

.input_second.input_all {
  width: 100%;
  padding: 12px 14px;
  font-size: 15px;
  border: 1.5px solid #e0e0e0;
  border-radius: 8px;
  transition: all 0.3s ease;
  outline: none;
  color: #222;
  background-color: #fafafa;
}

.input_second.input_all:focus {
  border-color: #ffd700;
  background-color: #fff;
  box-shadow: 0 0 8px rgba(255, 215, 0, 0.4);
}

.input_second.input_all::placeholder {
  color: #999;
}

.password-wrapper {
  position: relative;
}

.password-wrapper input {
  padding-left: 40px;
}

.toggle-password {
  position: absolute;
  top: 50%;
  left: 12px;
  transform: translateY(-50%);
  cursor: pointer;
  color: #aaa;
  font-size: 16px;
  transition: color 0.3s, transform 0.2s;
}

.toggle-password:hover {
  color: #ffd700;
  transform: translateY(-50%) scale(1.1);
}

.text-center {
  text-align: center;
  margin-top: 25px;
}

.btn-main-masai {
  background: linear-gradient(135deg, #ffd740, #ffc107);
  color: #212121;
  border: none;
  padding: 12px 0;
  border-radius: 8px;
  font-weight: bold;
  font-size: 16px;
  cursor: pointer;
  width: 100%;
  transition: transform 0.2s ease, box-shadow 0.3s ease;
}

.btn-main-masai:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(255, 193, 7, 0.5);
}

.footer_login_reg {
  margin-top: 20px;
  font-size: 14px;
  color: #666;
}

.footer_login_reg a {
  color: #ffc107;
  font-weight: bold;
  text-decoration: none;
  transition: color 0.3s ease;
}

.footer_login_reg a:hover {
  color: #ffb300;
}
</style>