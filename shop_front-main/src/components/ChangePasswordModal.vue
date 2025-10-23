<template>
  <div class="modal-backdrop" @click.self="close">
    <div class="modal-box">
      <button class="close-icon" @click="close" aria-label="بستن">×</button>

      <h3>تغییر رمز عبور</h3>

      <form @submit.prevent="submit">
        <input
          v-model="store.changePasswordUser.current_password"
          type="password"
          placeholder="رمز فعلی"
          required
        />
        <input
          v-model="store.changePasswordUser.password"
          type="password"
          placeholder="رمز جدید"
          required
        />
        <input
          v-model="store.changePasswordUser.confirm_password"
          type="password"
          placeholder="تکرار رمز جدید"
          required
        />

        <button type="submit" :disabled="store.loading">
          {{ store.loading ? 'در حال ارسال...' : 'تایید' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ChangePassStore } from '@/stores/ChangePassStore'
const store = ChangePassStore()

const emit = defineEmits(['close'])

const close = () => emit('close')

const submit = async () => {
  await store.changePassword()
  if (!store.loading) {
    emit('close')
  }
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(2px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3000;
}

.modal-box {
  background: #fff;
  padding: 32px 24px 24px;
  border-radius: 16px;
  width: 420px;
  max-width: 90%;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 16px;
  font-family: 'Yekan', sans-serif;
}

.close-icon {
  position: absolute;
  top: 14px;
  left: 14px;
  background: transparent;
  border: none;
  font-size: 24px;
  color: #666;
  cursor: pointer;
  transition: 0.2s;
}

.close-icon:hover {
  color: #111;
}

.modal-box h3 {
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.modal-box input {
  padding: 12px 16px;
  font-size: 14px;
  margin: 5px;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px solid #ccc;
  border-radius: 10px;
  transition: all 0.3s ease;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
  background-color: #fafafa;
  direction: rtl;
}

.modal-box input:focus {
  border-color: #ffd700;
  background-color: #fff;
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.25);
  outline: none;
}

.modal-box button[type='submit'] {
  padding: 12px;
  font-size: 15px;
  border: none;
  background-color: #ffd700;
  color: #111;
  font-weight: bold;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.modal-box button[type='submit']:hover {
  background-color: #e5c100;
}

.modal-box button[type='submit']:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
.modal-box form {
  display: flex;
  flex-direction: column;
  gap: 14px; 
}

.modal-box input {
  font-family: 'Yekan';
  width: 90%;
  padding: 12px 16px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 10px;
  transition: all 0.3s ease;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
  background-color: #fafafa;
  direction: rtl;
}

.modal-box input:focus {
  border-color: #ffd700;
  background-color: #fff;
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.25);
  outline: none;
}

.modal-box button[type='submit'] {
  padding: 12px;
  font-size: 15px;
  width: 100%;
  border: none;
  background-color: #ffd700;
  color: #111;
  font-weight: bold;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.modal-box button[type='submit']:hover {
  background-color: #e5c100;
}

.modal-box button[type='submit']:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.close-icon {
  position: absolute;
  top: 12px;
  left: 12px;
  background: transparent;
  border: none;
  font-size: 26px;
  color: #999;
  cursor: pointer;
  transition: 0.2s;
}

.close-icon:hover {
  color: #333;
}
</style>
