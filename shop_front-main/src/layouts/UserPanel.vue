<template>
  <div class="admin-panel">
    <aside :class="['sidebar', { collapsed: isCollapsed }]">
      <div class="top-bar">
        <div class="logo" v-if="!isCollapsed"><i class="fas fa-store"></i> فروشگاه</div>
        <button class="toggle-btn" @click="isCollapsed = !isCollapsed">
          <i class="fas fa-bars"></i>
        </button>
      </div>

      <button class="home-btn" @click="goHome">
        <i class="fas fa-home"></i> صفحه اصلی
      </button>

      <nav>
        <ul>
          <li :class="{ active: activeTab === 'profile' }" @click="activeTab = 'profile'">
            <i class="fas fa-user"></i>
            <span v-if="!isCollapsed">پروفایل</span>
          </li>

          <li :class="{ active: activeTab === 'cart' }" @click="activeTab = 'cart'">
            <i class="fas fa-shopping-cart"></i>
            <span v-if="!isCollapsed">سبد خرید</span>
          </li>

          <li :class="{ active: activeTab === 'wallet' }" @click="activeTab = 'wallet'">
            <i class="fas fa-wallet"></i>
            <span v-if="!isCollapsed">کیف پول</span>
          </li>

          <li :class="{ active: activeTab === 'orders' }" @click="activeTab = 'orders'">
            <i class="fas fa-box"></i>
            <span v-if="!isCollapsed">سفارش‌های من</span>
          </li>

          <li @click="logout">
            <i class="fas fa-sign-out-alt"></i>
            <span v-if="!isCollapsed">خروج</span>
          </li>
        </ul>
      </nav>
    </aside>

    <main class="main-content">
      <header class="header">
        <h2>{{ pageTitle }}</h2>
      </header>

      <section v-if="activeTab === 'profile'">
        <UserProfile />
      </section>

      <section v-if="activeTab === 'cart'">
        <ShoppingCart />
      </section>

      <section v-if="activeTab === 'wallet'" class="wallet-section">
        <Wallet />
      </section>

      <section v-if="activeTab === 'orders'">
        <UserOrders />
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { toast } from "vue3-toastify";
import { useWalletStore } from "@/stores/useWalletStore";
import { useUserStore } from "@/stores/useUserStore";

import ShoppingCart from "@/components/ShoppingCart.vue";
import UserProfile from "@/components/UserProfile.vue";
import Wallet from "@/components/Wallet.vue";
import UserOrders from "@/components/UserOrders.vue";
import { useLoginStore } from "@/stores/useLoginStore";

import { useRouter } from "vue-router";
const loginStore = useLoginStore();

const isCollapsed = ref(false);
const activeTab = ref("profile");
const walletStore = useWalletStore();
const userStore = useUserStore();
const router = useRouter();

onMounted(async () => {
  await walletStore.fetchBalance();
  await walletStore.fetchTransactions();
  await userStore.fetchBankAccounts();
});

const goHome = () => {
  router.push("/");
};

const pageTitle = computed(() => {
  switch (activeTab.value) {
    case "profile":
      return "پروفایل کاربر";
    case "cart":
      return "سبد خرید";
    case "wallet":
      return "کیف پول من";
    case "orders":
      return "سفارش‌های من";
    default:
      return "";
  }
});
const logout = () => {
  loginStore.logout();
  toast.info("شما از حساب خارج شدید!");
  router.push("/login");
};
</script>

<style scoped>
.admin-panel {
  font-family: "Yekan";
  display: flex;
  min-height: 100vh;
  direction: rtl;
  background: #f5f5f5;
}

.sidebar {
  width: 220px;
  background: #111;
  color: white;
  display: flex;
  flex-direction: column;
  padding: 20px;
  transition: width 0.3s;
  position: relative;
}
.sidebar.collapsed {
  width: 60px;
}

.home-btn {
  margin: 10px 0;
  padding: 8px 12px;
  background: #f9c710;
  border: none;
  border-radius: 8px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}
.home-btn i {
  margin-left: 5px;
}
.home-btn:hover {
  background: #f8b900;
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2);
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.toggle-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
}

.sidebar nav ul {
  list-style: none;
  padding: 0;
}
.sidebar li {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 10px;
  margin: 5px 0;
  cursor: pointer;
  border-radius: 8px;
  transition: 0.2s;
}
.sidebar li:hover {
  background: #5c482a;
}
.sidebar li.active {
  background: #f9c710;
  color: #fff;
  font-weight: bold;
}

.main-content {
  flex: 1;
  padding: 20px;
}
.header {
  background: white;
  padding: 15px 20px;
  border-radius: 10px;
  margin-bottom: 20px;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.1);
}

.wallet-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 25px;
  margin-top: 20px;
}
</style>
