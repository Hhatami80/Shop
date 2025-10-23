<template>
  <aside class="admin-sidebar">
    <div class="logo-area">
      <h2 class="logo">
        <fa-icon :icon="['fas', 'crown']" class="logo-icon" />
        <span>پنل ادمین</span>
      </h2>
    </div>

    <div class="user-profile-sidebar">
      <div class="user-avatar"></div>
      <div class="user-info">
        <p class="user-name">{{ userStore.profile.username }} </p>
        <p class="user-role">Super Admin</p>
      </div>
    </div>

    <nav class="sidebar-menu-nav">
      <ul class="main-menu">
        <li v-for="item in menuItems" :key="item.path">
          <div
            class="sidebar-item"
            :class="{ active: item.active }"
            @click="item.submenu ? $emit('toggleSubmenu', item.path) : $emit('goTo', item.path)"
          >
            <span>
              <fa-icon :icon="item.icon" class="menu-icon" />
              {{ item.name }}
            </span>
            <fa-icon
              v-if="item.submenu"
              :icon="['fas', item.submenuOpen ? 'chevron-up' : 'chevron-down']"
              class="arrow-icon"
            />
          </div>

          <ul v-if="item.submenu && item.submenuOpen" class="submenu-list">
            <li
              v-for="sub in item.submenu"
              :key="sub.path"
              :class="{ active: $route.path.startsWith(sub.path) }"
              @click="$emit('goTo', sub.path)"
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
import { defineProps, defineEmits , onMounted} from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/useUserStore'
const userStore = useUserStore()

const props = defineProps({
  menuItems: {
    type: Array,
    required: true,
  },
})
const emit = defineEmits(['logout', 'goTo', 'toggleSubmenu'])

onMounted(async () => {
    await userStore.fetchProfile(); 
});

const $route = useRoute()
</script>

<style scoped>
.admin-sidebar {
  width: 250px;
  background-color: #1a1a1a;
  color: #ffffff;
  position: fixed;
  top: 0;
  right: 0;
  height: 100%;
  padding: 0;
  overflow-y: auto;
  z-index: 1001;
  box-shadow: 4px 0 10px rgba(0, 0, 0, 0.2);
}

.logo-area {
  background-color: #2c2c2c;
  padding: 20px 25px;
  border-bottom: 1px solid #3a3a3a;
}

.logo {
  font-size: 24px;
  font-weight: 700;
  color: #ffd700;
  margin: 0;
  display: flex;
  align-items: center;
}

.logo-icon {
  font-size: 28px;
  margin-left: 10px;
}

.user-profile-sidebar {
  display: flex;
  align-items: center;
  padding: 20px 25px;
  border-bottom: 1px solid #3a3a3a;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background-color: #ffd700;
  border-radius: 50%;
  margin-left: 10px;
}

.user-info .user-name {
  font-weight: bold;
  font-size: 15px;
  margin-bottom: 2px;
}

.user-info .user-role {
  font-size: 12px;
  color: #aaaaaa;
}

.main-menu {
  list-style: none;
  padding: 15px 0;
}

.sidebar-item {
  padding: 12px 25px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #ffffff;
  transition: background 0.3s, color 0.3s;
  font-size: 15px;
}

.sidebar-item:hover {
  background-color: #2c2c2c;
  color: #ffd700;
}

.sidebar-item.active {
  background-color: #ffd700;
  color: #1a1a1a;
  border-right: 4px solid #ffffff;
  padding-right: 21px;
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
  transition: background-color 0.2s, color 0.2s;
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
.menu-icon {
  font-size: 18px;
  margin-left: 15px;
  width: 20px;
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