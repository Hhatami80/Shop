<template>
  <StickyHeader :visible="true" :use-scroll-blur="false" />
  <main class="login-wrapper">

    <div class="login-container">
      <h2 class="login-title">ورود به حساب کاربری</h2>
      <form class="login-form" @submit.prevent="loginUser">
        <label class="form-label">
          <label> نام کاربری <span>*</span></label>
          <input
            type="text"
            v-model="login.loginUser.username"
            placeholder="نام کاربری شما"
            @keydown.enter="loginUser"
          />
        </label>

        <label class="form-label">
          <label> کلمه عبور <span>*</span></label>
          <div class="password-wrapper">
            <input
              :type="showPassword ? 'text' : 'password'"
              v-model="login.loginUser.password"
              placeholder="کلمه عبور شما"
              @keydown.enter="loginUser"
            />
            <transition name="fade-scale">
              <i
                v-if="!showPassword"
                key="eye"
                class="fa fa-eye toggle-password"
                @click="showPassword = !showPassword"
              ></i>
              <i
                v-else
                key="eye-slash"
                class="fa fa-eye-slash toggle-password"
                @click="showPassword = !showPassword"
              ></i>
            </transition>
          </div>
        </label>

        <div class="form-actions">
          <router-link to="/forgotPassword" class="forgot-link">
            رمز عبور را فراموش کرده‌اید؟
          </router-link>
        </div>

        <button type="submit" class="login-button">ورود</button>

        <div class="register-link">
          <span>کاربر جدید هستید؟</span>
          <router-link to="/register">ثبت نام</router-link>
        </div>
      </form>
    </div>
  </main>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useLoginStore } from "@/stores/useLoginStore";
import { toast } from "vue3-toastify";
import StickyHeader from "@/components/StickyHeader.vue";

const login = useLoginStore();
const router = useRouter();
const showPassword = ref(false);

async function loginUser() {
  try {
    const response = await login.login();

    if (response) {
      
      const role = login.user?.role;

      if (role === "admin") {
        toast.success("خوش آمدید مدیر محترم 🌟");
        router.push("/admin/dashboard");
      } else {
        toast.success("ورود با موفقیت انجام شد ");
        router.push("/user/dashboard");
      }

   
      login.loginUser.username = "";
      login.loginUser.password = "";
    }
  } catch (error) {
    console.error("Error in Login =>", error);
  }
}
</script>

<style scoped>

*,
*::before,
*::after {
  box-sizing: border-box;
}

.login-wrapper {
  direction: rtl;
  margin-top: 10px;
  background-color: #f9f9f9;
  min-height: 100vh;
  display: flex;
  margin-top: 10px;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}

.login-container {
  background: #fff;
  padding: 2.2rem 2.5rem;
  border-radius: 16px;
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 420px;
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

.login-title {
  font-size: 24px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 1.8rem;
  color: #333;
  letter-spacing: 0.5px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.3rem;
}

.form-label {
  display: flex;
  font-weight: 600;
  flex-direction: column;
  font-size: 14px;
  color: #333;
}

.form-label span {
  color: #e53935;
  margin-left: 4px;
}

input {
  width: 100%;
  
  padding: 12px 14px;
  font-family: inherit;
  border: 1.5px solid #e0e0e0;
  border-radius: 8px;
  font-size: 15px;
  margin-top: 6px;
  background-color: #fafafa;
  transition: all 0.3s ease;
}

input:focus {
  border-color: #ffd700;
  background-color: #fff;
  box-shadow: 0 0 8px rgba(255, 215, 0, 0.4);
  outline: none;
}

.password-wrapper {
  position: relative;
}

.password-wrapper input {
  padding-left: 42px;
}

.toggle-password {
  position: absolute;
  top: 55%;
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

.form-actions {
  text-align: left;
  margin-top: -0.5rem;
}

.forgot-link {
  font-size: 13px;
  color: #1976d2;
  text-decoration: none;
  transition: color 0.3s ease;
}

.forgot-link:hover {
  color: #ffa000;
}

.login-button {
  background: linear-gradient(135deg, #ffd740, #ffc107);
  color: #212121;
  padding: 12px 0;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.3s ease;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(255, 193, 7, 0.5);
}

.register-link {
  text-align: center;
  margin-top: 1rem;
  font-size: 14px;
}

.register-link span {
  color: #666;
  margin-left: 4px;
}

.register-link a {
  color: #ffc107;
  font-weight: bold;
  text-decoration: none;
  transition: color 0.3s ease;
}

.register-link a:hover {
  color: #ffb300;
}

.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: all 0.3s ease;
}
.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.8) translateY(-50%);
}
.fade-scale-enter-to,
.fade-scale-leave-from {
  opacity: 1;
  transform: scale(1) translateY(-50%);
}
</style>
