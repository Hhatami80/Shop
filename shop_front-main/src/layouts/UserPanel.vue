<template>
  <div v-if="isAuthenticated" class="user-dashboard">
   
    <TheSidebar
      :user="user"
      :menu-items="menuItems"
      @go-to="goTo"
      @logout="logout"
    />

    <main class="main-content">
    
      <TheHeader
        :title="'پنل کاربری'"
        :user="user"
        :profileMenu="profileMenu"
        @goHome="goHome"
        @profileAction="handleProfileAction"
      />

    
      <router-view />
    </main>
  </div>

  <div v-else class="unauthorized">
    <p>برای مشاهده‌ی این صفحه باید وارد شوید.</p>
    <button @click="goToLogin">ورود</button>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useLoginStore } from '@/stores/useLoginStore'
import TheSidebar from '@/components/TheSidebar.vue'
import TheHeader from '@/components/TheHeader.vue'

const router = useRouter()
const loginStore = useLoginStore()


const isAuthenticated = computed(() => loginStore.isAuthenticated)
const user = computed(() =>
  loginStore.user || { username: 'کاربر مهمان', image: '/default-avatar.jpg', role: 'کاربر' }
)

const profileMenu = [
  { label: 'تغییر رمز عبور', action: 'changePassword' },
  { label: 'خروج', action: 'logout' },
]


const menuItems = [
  { name: 'پروفایل', path: '/user/profile/info', icon: ['fas', 'user'] }, // مسیر info
  { name: 'سبد خرید', path: '/user/shop-cart', icon: ['fas', 'shopping-cart'] },
  { name: 'کیف پول', path: '/user/wallet', icon: ['fas', 'wallet'] },
  { name: 'سفارش‌ها', path: '/user/orders', icon: ['fas', 'box'] },
]


onMounted(() => {
  if (!isAuthenticated.value) router.push('/login')
  else if (router.currentRoute.value.path === '/user/profile') {
   
    router.replace('/user/profile/info')
  }
})


function goTo(path) {
  router.push(path)
}

function logout() {
  loginStore.logout()
  router.push('/login')
}

function goToLogin() {
  router.push('/login')
}

function goHome() {
  router.push('/')
}

function handleProfileAction(action) {
  if (action === 'logout') logout()
  if (action === 'changePassword') console.log('تغییر رمز عبور کلیک شد')
}
</script>

<style scoped>
.user-dashboard {
  display: flex;
  min-height: 100vh;
  direction: rtl;
}

.main-content {
  flex: 1;
  background: #f9f9f9;
  padding: 20px;
  margin-right: 250px;
  min-height: 100vh;
}

.unauthorized {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  text-align: center;
  background: #f8f8f8;
}

.unauthorized p {
  font-size: 1.2rem;
  margin-bottom: 1rem;
}

.unauthorized button {
  background: #f9c710;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
}
</style>
