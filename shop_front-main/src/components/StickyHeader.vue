<template>
  <transition name="fade">
    <div v-if="visible" :class="['header-sticky', { blurred: isBlurred }]">
      <div class="icons">
        <router-link to="/">
          <i class="fas fa-home"></i>
        </router-link>
        <router-link to="/shop-cart" class="cart-icon">
          <i class="fas fa-shopping-cart"></i>
          <transition name="badge-pop" mode="out-in">
            <span
              v-if="cartStore.totalQuantity > 0"
              class="cart-badge"
              :key="cartStore.totalQuantity"
            >
              {{ cartStore.totalQuantity }}
            </span>
          </transition>
        </router-link>

        <i class="fas fa-heart"></i>
        <template v-if="loginStore.isAuthenticated">
          <router-link v-if="loginStore.isAdmin" to="/admin" class="user-icon" title="پنل ادمین">
            <i class="fas fa-crown"></i>
          </router-link>

          <router-link v-else to="/user" class="user-icon" title="پروفایل کاربری">
            <i class="fas fa-user-circle"></i>
          </router-link>
        </template>
        <router-link v-else to="/login">
          <i class="fas fa-sign-in-alt"></i>
        </router-link>
      </div>

      <button ref="stickyMenuBtn" class="menu-btn" @click="toggleMenu">☰</button>
    </div>
  </transition>
  <transition name="sticky-slide-fade">
    <div v-if="drawerOpen" class="sticky-menu-box" @click.self="drawerOpen = false">
      <button class="sticky-close-btn" @click="drawerOpen = false">×</button>
      <ul>
        <li v-for="item in headerStore.menuItems" :key="item.id">
          <template v-if="item.url?.startsWith?.('#')">
            <a href="#" @click.prevent="scrollToSection(item.url)">
              {{ item.title }}
            </a>
          </template>
          <template v-else>
            <router-link :to="item.url">{{ item.title }}</router-link>
          </template>
        </li>
      </ul>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useHeaderStore } from '@/stores/useHeaderStore'
import { useLoginStore } from '@/stores/useLoginStore'
import { useCartStore } from '@/stores/useCartStore'

const cartStore = useCartStore()

const props = defineProps({
  visible: { type: Boolean, default: false },
})

const drawerOpen = ref(false)
const headerStore = useHeaderStore()
const loginStore = useLoginStore()
const isBlurred = ref(false)

function toggleMenu() {
  drawerOpen.value = !drawerOpen.value
}

function scrollToSection(selector) {
  const el = document.querySelector(selector)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth' })
    drawerOpen.value = false
  }
}

const handleScroll = () => {
  isBlurred.value = window.scrollY > 50
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  loginStore.loadFromCookies()
  cartStore.fetchCart()
})
onUnmounted(() => window.removeEventListener('scroll', handleScroll))
</script>

<style scoped>
.header-sticky {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  z-index: 1500;
  direction: rtl;
  display: block;
  transition: all 0.3s ease-in-out;
}

.header-sticky.blurred {
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.5);
}

.icons {
  position: absolute;
  top: 50%;
  left: 20px;
  transform: translateY(-50%);
  display: flex;
  gap: 18px;
  align-items: center;
}

.icons a,
.icons i {
  color: #222;
  font-size: 1.2rem;
  cursor: pointer;
  transition:
    color 0.2s ease,
    transform 0.15s ease;
}

.icons a:hover,
.icons i:hover {
  color: #f9c710;
  transform: scale(1.08);
}

.user-icon i {
  color: #444;
  font-size: 1.25rem;
}
.user-icon:hover i {
  color: #f9c710;
}

.menu-btn {
  position: absolute;
  top: 50%;
  right: 20px;
  transform: translateY(-50%);
  font-size: 24px;
  background: none;
  border: none;
  cursor: pointer;
  z-index: 1600;
}

.sticky-menu-box {
  position: fixed;
  top: 65px;
  right: 20px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 12px 16px;
  z-index: 3000;
  min-width: 220px;
  direction: rtl;
}

.sticky-menu-box ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.sticky-menu-box ul li {
  margin-bottom: 10px;
}
.sticky-menu-box ul li:last-child {
  margin-bottom: 0;
}
.sticky-menu-box ul li a {
  text-decoration: none;
  color: #333;
  font-weight: 600;
}
.sticky-menu-box ul li a:hover {
  color: #f9c710;
}
.sticky-close-btn {
  position: absolute;
  top: 8px;
  left: 8px;
  font-size: 20px;
  background: none;
  border: none;
  cursor: pointer;
}
.sticky-close-btn:hover {
  color: #e63946;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.sticky-slide-fade-enter-active,
.sticky-slide-fade-leave-active {
  transition:
    transform 0.25s ease,
    opacity 0.25s ease;
}
.sticky-slide-fade-enter-from {
  transform: translateY(-8px);
  opacity: 0;
}
.sticky-slide-fade-leave-to {
  transform: translateY(-8px);
  opacity: 0;
}
.cart-icon {
  position: relative;
  display: inline-block;
}

.cart-badge {
  position: absolute;
  top: -6px;
  left: -6px;
  background-color: #dc3545;
  color: #fff;
  font-size: 12px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  transform-origin: center;
}


.badge-pop-enter-active,
.badge-pop-leave-active {
  transition:
    transform 0.2s ease,
    opacity 0.2s ease;
}
.badge-pop-enter-from {
  transform: scale(0.5);
  opacity: 0;
}
.badge-pop-enter-to {
  transform: scale(1);
  opacity: 1;
}
.badge-pop-leave-from {
  transform: scale(1);
  opacity: 1;
}
.badge-pop-leave-to {
  transform: scale(0.5);
  opacity: 0;
}

@media (max-width: 768px) {
  .sticky-menu-box {
    left: 0;
    right: 0;
    width: 85%;
    max-width: 420px;
    margin: 0 8px;
    height: calc(100% - 60px);
    overflow-y: auto;
    border-radius: 8px;
  }

  .icons {
    right: 14px;
    gap: 12px;
  }

  .menu-btn {
    left: 14px;
  }
}
</style>
