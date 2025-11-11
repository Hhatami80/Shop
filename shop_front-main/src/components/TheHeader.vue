<template>
  <header class="admin-header ">
    <h1>{{ title }}</h1>
    <div class="topbar-actions">
      <button v-if="showHomeBtn" class="action-btn" @click="$emit('goHome')">
        <fa-icon :icon="['fas','home']" />
      </button>

      <div class="profile-dropdown-container" @click="toggleProfileMenu">
        <button class="action-btn">
          <fa-icon :icon="['fas','user-circle']" />
          <span>{{ user.name }}</span>
        </button>
        <div v-if="showProfileMenu" class="profile-dropdown">
          <ul>
            <li v-for="item in profileMenu" :key="item.label" @click="handleProfileItem(item)">
              {{ item.label }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  title: { type: String, default: 'پنل کاربری' },
  user: { type: Object, required: true },
  profileMenu: { type: Array, default: () => [] },
  showHomeBtn: { type: Boolean, default: true },
})

const emit = defineEmits(['goHome','profileAction'])

const showProfileMenu = ref(false)

function toggleProfileMenu() {
  showProfileMenu.value = !showProfileMenu.value
}

function handleProfileItem(item) {
  if(item.action) emit('profileAction', item.action)
  showProfileMenu.value = false
}
</script>




<style scoped>
.admin-header {
    background-color: #fff;
    padding: 15px 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #F0F0F0; 
    position: sticky; 
    top: 0;
    z-index: 500;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.admin-header h1 {
    font-size: 20px;
    color: #1A1A1A;
    font-weight: 600;
    margin: 0;
}

.topbar-actions {
    display: flex;
    align-items: center;
    gap: 15px;
}

.action-btn {
    background: #F0F0F0;
    color: #4A4A4A; 
    border: none;
    border-radius: 8px;
    padding: 10px 15px;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.action-btn:hover {
    background: #FFD700; 
    color: #1A1A1A; 
}

.profile-dropdown-container {
    position: relative;
    cursor: pointer;
    z-index: 600;
}

.profile-btn {
    background: #FFD700; 
    color: #1A1A1A;
    border: none;
    border-radius: 8px;
    padding: 10px 15px;
    font-size: 15px;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.profile-btn .fa-icon {
    font-size: 18px;
}

.profile-dropdown {
    position: absolute;
    top: 50px;
    left: 0; 
    background-color: #fff;
    border: 1px solid #FFD700; 
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    width: 180px;
    padding: 5px 0;
}

.profile-dropdown ul {
    list-style: none;
    margin: 0;
    padding: 0;
}

.profile-dropdown li {
    padding: 10px 16px;
    cursor: pointer;
    transition: background-color 0.2s;
    color: #333;
    font-size: 14px;
}

.profile-dropdown li:hover {
    background-color: #FFFBE5; 
    color: #1A1A1A;
}
</style>