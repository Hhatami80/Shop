<template>
  <transition name="fade">
    <div v-if="visible" :class="['header-sticky', { blurred: useScrollBlur && isBlurred }]">
      <div class="icons">
        
        <div class="cart-icon-wrapper">
          <i
            class="fas fa-shopping-cart"
            @click="handleCartClick"
            v-if="loginStore.user.role !== 'admin'"
          ></i>
          <span v-if="cartStore.totalQuantity > 0" class="cart-badge">
            {{ cartStore.totalQuantity }}
          </span>
        </div>
        
        <i v-if="loginStore.isAuthenticated" class="fas fa-heart"></i>
        <router-link
        v-if="loginStore.isAuthenticated && loginStore.isAdmin"
          to="/admin/dashboard"
          class="user-icon"
          >
          <i class="fas fa-user"></i>
        </router-link>
        <router-link v-else-if="loginStore.isAuthenticated" to="/user/dashboard" class="user-icon">
          <i class="fas fa-user"></i>
        </router-link>
        <router-link v-else to="/login" class="user-icon">
          <i class="fas fa-user"></i>
        </router-link>
        <router-link to="/"><i class="fas fa-home"></i></router-link>
      </div>
      
      <button ref="stickyMenuBtn" class="menu-btn" @click="toggleMenu">☰</button>
    </div>
  </transition>

  <transition name="drawer-slide">
    <div v-if="drawerOpen" class="sticky-menu-box" @click.self="drawerOpen = false">
      <button class="sticky-close-btn" @click="drawerOpen = false">×</button>
      <ul>
        <li v-for="item in headerStore.menuItems" :key="item.id">
          <template v-if="item.url?.startsWith?.('#')">
            <a href="#" @click.prevent="scrollToSection(item.url)">{{ item.title }}</a>
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
import router from '@/router'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

const props = defineProps({
  visible: { type: Boolean, default: true },
  useScrollBlur: { type: Boolean, default: true },
  showOnScroll: { type: Boolean, default: false },
})

const cartStore = useCartStore()
const loginStore = useLoginStore()
const headerStore = useHeaderStore()
const drawerOpen = ref(false)
const isBlurred = ref(false)
const isVisible = ref(!props.showOnScroll)

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

function handleCartClick() {
  if (!loginStore.isAuthenticated) {
    toast.warn('لطفاً وارد حساب کاربری خود شوید')
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } else {
    router.push('/user/shop-cart')
  }
}

const handleScroll = () => {
  if (props.useScrollBlur) isBlurred.value = window.scrollY > 50
  if (props.showOnScroll && window.scrollY > 50) isVisible.value = true
}

onMounted(() => {
  if (props.useScrollBlur || props.showOnScroll) window.addEventListener('scroll', handleScroll)
  loginStore.loadFromCookies()
  cartStore.fetchCart()
})

onUnmounted(() => {
  if (props.useScrollBlur || props.showOnScroll) window.removeEventListener('scroll', handleScroll)
})
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
  transition: all 0.3s ease-in-out;
}

.header-sticky.blurred {
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.7);
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
  font-size: 1.3rem;
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

.menu-btn {
  position: absolute;
  top: 50%;
  right: 20px;
  transform: translateY(-50%);
  font-size: 26px;
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
  min-width: 240px;
  direction: rtl;
  transition: all 0.3s ease;
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
  transition: color 0.2s ease;
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
  transition: 0.3s;
}
.sticky-close-btn:hover {
  color: #e63946;
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
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
.drawer-slide-enter-active,
.drawer-slide-leave-active {
  transition:
    transform 0.3s ease,
    opacity 0.25s ease;
}
.drawer-slide-enter-from {
  transform: translateX(100%);
  opacity: 0;
}
.drawer-slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
.cart-icon-wrapper {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.cart-badge {
  position: absolute;
  bottom: 0;
  left: 0;

  background: #ff3547;
  color: #fff;

  font-size: 8px;
  font-weight: 700;

  padding: 1px 3px;
  border-radius: 50%;

  min-width: 12px;
  height: 12px;

  display: flex;
  align-items: center;
  justify-content: center;

  line-height: 1;
  pointer-events: none;

  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

@media (max-width: 768px) {
  .sticky-menu-box {
    top: 0;
    right: 0;
    height: 100dvh;
    width: 40%;
    border-radius: 0;
    border: none;
    box-shadow: none;
    padding: 70px 25px 25px;
    overflow-y: auto;
  }

  .sticky-close-btn {
    top: 14px;
    left: 20px;
    font-size: 28px;
  }

  .icons {
    left: 14px;
    gap: 12px;
  }

  .menu-btn {
    right: 14px;
    font-size: 24px;
  }
}
</style>
