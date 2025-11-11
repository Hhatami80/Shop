<template>
  <div class="app-container">
    <TheSidebar
      :menu-items="sidebarMenuItems"
      :user="user"
      @go-to="goTo"
      @toggle-submenu="toggleSubmenu"
      @logout="logout"
    />

    <main class="app-main">
      <TheHeader
        :title="headerTitle"
        :user="user"
        :profileMenu="profileMenu"
        @go-home="goHome"
        @profileAction="handleProfileAction"
      />

      <section class="content">
        <router-view />
      </section>
    </main>

    <ChangePasswordModal v-if="showPasswordModal" @close="showPasswordModal = false" />
    <ConfirmLogoutModal
      v-if="showLogoutConfirm"
      @confirm="confirmLogout"
      @cancel="showLogoutConfirm = false"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

import TheSidebar from '@/components/TheSidebar.vue'
import TheHeader from '@/components/TheHeader.vue'
import ChangePasswordModal from '@/components/ChangePasswordModal.vue'
import ConfirmLogoutModal from '@/components/ConfirmLogoutModal.vue'

import { useLoginStore } from '@/stores/useLoginStore'

const router = useRouter()
const route = useRoute()
const loginStore = useLoginStore()
const showLogoutConfirm = ref(false)
const showPasswordModal = ref(false)

loginStore.loadFromCookies()
const user = computed(() => loginStore.user || { name: 'کاربر مهمان', role: 'user' })

const headerTitle = computed(() => (user.value.role === 'admin' ? 'پنل ادمین' : 'پنل کاربری'))

const profileMenu = computed(() =>
  user.value.role === 'admin'
    ? [
        { label: 'تغییر رمز عبور', action: 'changePassword' },
        { label: 'خروج', action: 'logout' },
      ]
    : [{ label: 'خروج', action: 'logout' }],
)

const menuStatus = ref({ '/admin/dashboard': false })

const sidebarMenuItems = computed(() => {
  const isActiveRoute = (path) => route.path.startsWith(path)
  const isAdmin = user.value.role === 'admin'

  if (isAdmin) {
    return [
      {
        name: 'داشبورد',
        icon: ['fas', 'tachometer-alt'],
        path: '/admin/dashboard',
        submenuOpen: menuStatus.value['/admin/dashboard'],
        submenu: [
          { name: 'مدیریت هدر', path: '/admin/header' },
          { name: 'مدیریت فوتر', path: '/admin/footer' },
        ],
        active: isActiveRoute('/admin/header') || isActiveRoute('/admin/footer'),
      },
      {
        name: 'مدیریت مقالات',
        icon: ['fas', 'feather-alt'],
        path: '/admin/articles',
        active: isActiveRoute('/admin/articles'),
      },
      {
        name: 'مدیریت درباره ما',
        icon: ['fas', 'info-circle'],
        path: '/admin/aboutusmanager',
        active: isActiveRoute('/admin/aboutusmanager'),
      },
      {
        name: 'مدیریت بنر',
        icon: ['fas', 'image'],
        path: '/admin/bannermanager',
        active: isActiveRoute('/admin/bannermanager'),
      },
      {
        name: 'مدیریت محصولات',
        icon: ['fas', 'box-open'],
        path: '/admin/productmanager',
        active: isActiveRoute('/admin/productmanager'),
      },
      {
        name: 'مدیریت دسته بندی‌ها',
        icon: ['fas', 'tags'],
        path: '/admin/categorymanager',
        active: isActiveRoute('/admin/categorymanager'),
      },
      {
        name: 'لیست سفارشات',
        icon: ['fas', 'receipt'],
        path: '/admin/orderlist',
        active: isActiveRoute('/admin/orderlist'),
      },
      {
        name: 'مدیریت تراکنش‌ها',
        icon: ['fas', 'wallet'],
        path: '/admin/transactions',
        active: isActiveRoute('/admin/transactions'),
      },
      {
        name: 'لیست کاربران',
        icon: ['fas', 'users'],
        path: '/admin/userslist',
        active: isActiveRoute('/admin/userslist'),
      },
      {
        name: 'مدیریت نظرات',
        icon: ['fas', 'comments'],
        path: '/admin/comments',
        active: isActiveRoute('/admin/comments'),
      },
    ]
  } else {
    return [
      {
        name: 'خانه',
        path: '/user/dashboard',
        icon: ['fas', 'home'],
        active: isActiveRoute('/user/dashboard'),
      },
      {
        name: 'سفارشات من',
        path: '/user/orders',
        icon: ['fas', 'receipt'],
        active: isActiveRoute('/user/orders'),
      },
      {
        name: 'کیف پول',
        path: '/user/wallet',
        icon: ['fas', 'wallet'],
        active: isActiveRoute('/user/wallet'),
      },
    ]
  }
})

function goTo(path) {
  router.push(path)
}

function toggleSubmenu(path) {
  menuStatus.value[path] = !menuStatus.value[path]
}

function goHome() {
  router.push('/')
}

function handleProfileAction(action) {
  if (action === 'logout') logout()
  else if (action === 'changePassword') showPasswordModal.value = true
}

function logout() {
  
  showLogoutConfirm.value = true
}
function confirmLogout() {
  showLogoutConfirm.value = false
  loginStore.logout()
  toast.info('شما از حساب خارج شدید!')
  router.push('/login')
}
</script>

<style scoped>
.app-container {
  display: flex;
  direction: rtl;
  height: 100vh;
  font-family: 'IRANSansX', sans-serif;
}

.app-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #f9f9f9;
  margin-right: 250px;
  overflow: hidden;
}

.content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}
</style>
