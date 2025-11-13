<template>
  <StickyHeader :visible="true" :use-scroll-blur="false" />
  <main class="wrapper default">
    <div class="container">
      <div class="main-content login_content">
        <header class="card-header">
          <h3 class="card-title">
            <span v-if="step === 'form'">ایجاد حساب کاربری</span>
            <span v-else>تأیید شماره تماس</span>
          </h3>
        </header>

        <div class="login_box">
          <form v-if="step === 'form'" @submit.prevent="sendOtp">
            <div class="form-group">
              <label class="form-account-title"> نام کاربری <span>*</span></label>
              <input
                class="input_second input_all"
                type="text"
                placeholder="نام کاربری شما"
                v-model="registers.registerUser.username"
              />
            </div>

            <div class="form-group">
              <label class="form-account-title"> شماره تماس <span>*</span></label>
              <input
                class="input_second input_all"
                type="text"
                placeholder="شماره تماس شما"
                v-model="registers.registerUser.phone"
                maxlength="11"
                pattern="^\d{11}$"
              />
            </div>

            <div class="form-group password-wrapper">
              <label class="form-account-title"> کلمه عبور <span>*</span></label>
              <input
                :type="showPassword ? 'text' : 'password'"
                class="input_second input_all"
                placeholder="کلمه عبور شما"
                v-model="registers.registerUser.password"
              />
              <i
                :class="[
                  'fa',
                  showPassword ? 'fa-eye-slash' : 'fa-eye',
                  'toggle-password',
                ]"
                @click="showPassword = !showPassword"
              ></i>
            </div>

            <div class="form-group password-wrapper">
              <label class="form-account-title"> تکرار کلمه عبور <span>*</span></label>
              <input
                :type="showConfirmPassword ? 'text' : 'password'"
                class="input_second input_all"
                placeholder="تکرار کلمه عبور شما"
                v-model="registers.registerUser.confirm_password"
              />
              <i
                :class="[
                  'fa',
                  showConfirmPassword ? 'fa-eye-slash' : 'fa-eye',
                  'toggle-password',
                ]"
                @click="showConfirmPassword = !showConfirmPassword"
              ></i>
            </div>

            <div class="text-center">
              <button type="submit" class="btn big_btn btn-main-masai">
                ارسال کد تأیید
              </button>
            </div>

            <div class="footer_login_reg text-center">
              <p>
                <span>قبلا ثبت نام کرده‌اید؟</span>
                <router-link to="/login">ورود</router-link>
              </p>
            </div>
          </form>

          <form v-else @submit.prevent="verifyOtp">
            <div class="form-group">
              <label class="form-account-title"><span>*</span> کد تایید ارسال شده</label>
              <input
                class="input_second input_all"
                type="text"
                placeholder="کد تایید"
                v-model="registers.otpCode"
              />
            </div>

            <div class="text-center">
              <button type="submit" class="btn big_btn btn-main-masai">
                تأیید و ثبت‌نام
              </button>
            </div>

            <div class="footer_login_reg text-center">
              <p>
                <span>قبلاً ثبت‌نام کرده‌اید؟</span>
                <router-link to="/login">ورود</router-link>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { useRouter } from "vue-router";
import { useRegisterStore } from "@/stores/useRegisterStore";
import { ref } from "vue";
import { storeToRefs } from "pinia";
import StickyHeader from "@/components/StickyHeader.vue";

const router = useRouter();
const registers = useRegisterStore();
const { step } = storeToRefs(registers);

const showPassword = ref(false);
const showConfirmPassword = ref(false);

const sendOtp = async () => {
  const success = await registers.requestOtp();
  if (!success) {
    toast.error(registers.errors.username[0]);
  } else {
    toast.error("خطایی رخ داد. لطفا دوباره تلاش کنید.");
  }
};

const verifyOtp = async () => {
  const result = await registers.verifyAndActivate();
  if (result) router.push("/login");
};
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
  margin-top: 50px;
  color: #333;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.container {
  max-width: 520px;
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
  font-size: 24px;
  font-weight: bold;
  color: #333;
  border-bottom: none;
  letter-spacing: 0.5px;
}

.login_box {
  width: 100%;
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
  top: 50px;
  left: 10px;
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

.footer_login_reg span {
  margin-left: 5px;
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
