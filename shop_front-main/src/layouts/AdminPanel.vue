<template>
  <div class="admin-container">
    <TheSidebar
      :menu-items="sidebarMenuItems"
      @logout="logout"
      @go-to="goTo"
      @toggle-submenu="toggleSubmenu"
    />

    <main class="admin-main">
      <TheHeader
        @go-home="goHome"
        @logout="logout"
        @open-change-password-modal="openChangePasswordModal"
      />

      <section class="content">
        <router-view />
      </section>
    </main>

    <ChangePasswordModal v-if="showPasswordModal" @close="showPasswordModal = false" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { toast } from 'vue3-toastify'
import TheSidebar from '@/components/TheSidebar.vue'
import TheHeader from '@/components/TheHeader.vue'
import ChangePasswordModal from '@/components/ChangePasswordModal.vue'

import { useLoginStore } from '@/stores/useLoginStore'

const router = useRouter()
const route = useRoute()
const loginStore = useLoginStore()
const showPasswordModal = ref(false)

const menuStatus = ref({
  '/admin/dashboard': false,
})

const sidebarMenuItems = computed(() => {
  const isActiveRoute = (path) => route.path.startsWith(path)

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
      name: 'مدیریت دسته بندی ها',
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
      active: route.path.startsWith('/admin/transactions'),
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
})

function goTo(path) {
  router.push(path)
}

function toggleSubmenu(path) {
  menuStatus.value[path] = !menuStatus.value[path]
}

function openChangePasswordModal() {
  showPasswordModal.value = true
}

function goHome() {
  router.push('/')
}

const logout = () => {
  loginStore.logout()
  toast.info('شما از حساب خارج شدید!')
  router.push('/login')
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;700;800&display=swap');

.admin-container {
  direction: rtl;
  display: flex;
  height: 100vh;
  font-family: 'IRANSansX',sans-serif;
}

.admin-main {
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
