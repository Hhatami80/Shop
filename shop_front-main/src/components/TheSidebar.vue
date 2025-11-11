<template>
  <aside class="admin-sidebar" :class="{ admin: isAdmin }">
    <div class="logo-area">
      <h2 class="logo">
        <fa-icon :icon="logoIcon" class="logo-icon" />
        <span>{{ panelTitle }}</span>
      </h2>
    </div>

    <div class="user-profile-sidebar">
      <div class="avatar-wrapper">
        <transition name="avatar-fade" mode="out-in">
          <img
            :key="avatarUrl"
            class="user-avatar"
            :src="avatarUrl"
            alt="avatar"
            @error="onImageError"
          />
        </transition>
      </div>

      <div class="user-info">
        <p class="user-name">{{ user.username || 'کاربر مهمان' }}</p>
        <p class="user-role">
          {{ isAdmin ? 'مدیر سیستم' : user.role || 'کاربر عادی' }}
        </p>
      </div>
    </div>

    <nav class="sidebar-menu-nav">
      <ul class="main-menu">
        <li v-for="item in menuItems" :key="item.path">
          <div
            class="sidebar-item"
            :class="{ active: item.active }"
            @click="item.submenu ? toggleSubmenu(item.path) : goTo(item.path)"
          >
            <span>
              <fa-icon :icon="item.icon" class="menu-icon" />
              {{ item.name }}
            </span>
            <fa-icon
              v-if="item.submenu"
              :icon="item.submenuOpen ? ['fas', 'chevron-up'] : ['fas', 'chevron-down']"
              class="arrow-icon"
            />
          </div>

          <ul v-if="item.submenu && item.submenuOpen" class="submenu-list">
            <li
              v-for="sub in item.submenu"
              :key="sub.path"
              :class="{ active: sub.active }"
              @click="goTo(sub.path)"
            >
              {{ sub.name }}
            </li>
          </ul>
        </li>

        <li class="sidebar-item logout-item" @click="$emit('logout')">
          <fa-icon :icon="['fas', 'sign-out-alt']" class="menu-icon" /> خروج
        </li>
      </ul>
    </nav>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import defaultAvatar from '@/assets/image/icons/avatar1.jpg'
import { useUserStore } from '@/stores/useUserStore'

const props = defineProps({
  user: { type: Object, required: true },
  menuItems: { type: Array, default: () => [] },
  logoIcon: { type: Array, default: () => ['fas', 'crown'] },
})

const emit = defineEmits(['goTo', 'toggleSubmenu', 'logout'])
const store = useUserStore()

const isAdmin = computed(() => props.user.role === 'admin')
const panelTitle = computed(() => (isAdmin.value ? 'پنل ادمین' : 'پنل کاربری'))

const avatarUrl = computed(() => {
  let img = props.user?.image || store.profile?.image

  if (!img) return defaultAvatar

  if (img.startsWith('http://')) {
    img = img.replace('http://', window.location.protocol + '//')
  }

  if (!img.startsWith('http')) {
    const base = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
    img = `${base}${img.startsWith('/') ? '' : '/'}${img}`
  }

  return img
})

function onImageError(e) {
  e.target.src = defaultAvatar
}

function toggleSubmenu(path) {
  emit('toggleSubmenu', path)
}

function goTo(path) {
  emit('goTo', path)
}
</script>

<style scoped>
.admin-sidebar {
  width: 250px;
  background-color: #1a1a1a;
  color: #fff;
  position: fixed;
  top: 0;
  right: 0;
  height: 100%;
  display: flex;
  flex-direction: column;
  z-index: 1001;
  box-shadow: 4px 0 10px rgba(0, 0, 0, 0.2);
}

.admin-sidebar.admin {
  background-color: #111827;
}

.logo-area {
  background-color: #2c2c2c;
  padding: 20px 25px;
  border-bottom: 1px solid #3a3a3a;
  text-align: center;
}

.logo {
  font-size: 22px;
  font-weight: 700;
  color: #ffd700;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.logo-icon {
  font-size: 26px;
}

.user-profile-sidebar {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 25px 10px;
  border-bottom: 1px solid #3a3a3a;
  background-color: #222;
}

.avatar-wrapper {
  width: 85px;
  height: 85px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid #ffd700;
  margin-bottom: 10px;
}

.avatar-fade-enter-active,
.avatar-fade-leave-active {
  transition: all 0.5s ease;
}
.avatar-fade-enter-from {
  opacity: 0;
  transform: scale(0.9);
}
.avatar-fade-leave-to {
  opacity: 0;
  transform: scale(1.1);
}

.user-avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
  background-color: #fff8dc;
  transition: 0.3s ease;
}

.user-avatar:hover {
  transform: scale(1.05);
}

.user-info {
  text-align: center;
}

.user-name {
  font-weight: bold;
  font-size: 16px;
  margin-bottom: 4px;
}

.user-role {
  font-size: 13px;
  color: #bbbbbb;
}

.main-menu {
  list-style: none;
  padding: 15px 0;
  flex-grow: 1;
}

.sidebar-item {
  padding: 12px 25px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition:
    background 0.3s,
    color 0.3s;
  font-size: 15px;
}

.sidebar-item:hover,
.sidebar-item.active {
  background-color: #2c2c2c;
  color: #ffd700;
}

.sidebar-item span {
  display: flex;
  align-items: center;
}

.menu-icon {
  font-size: 18px;
  margin-left: 15px;
  width: 20px;
}

.arrow-icon {
  font-size: 12px;
}

.submenu-list {
  list-style: none;
  padding: 0 0 5px 0;
  margin: 0;
  background-color: #2c2c2c;
}

.submenu-list li {
  padding: 10px 25px 10px 50px;
  cursor: pointer;
  font-size: 14px;
  color: #aaaaaa;
  transition:
    background-color 0.2s,
    color 0.2s;
}

.submenu-list li:hover {
  background-color: #3a3a3a;
  color: #ffd700;
}

.submenu-list li.active {
  color: #ffd700;
  font-weight: 600;
}

.logout-item {
  margin-top: 20px;
  color: #ffd700;
  border-top: 1px solid #3a3a3a;
}

.logout-item:hover {
  background-color: #2c2c2c;
  color: #ffffff;
}

.logout-item .menu-icon {
  margin-left: 8px !important;
}
</style>
