<template>
  <div class="admin-panel">
    <aside :class="['sidebar', { collapsed: isCollapsed }]">
      <div class="top-bar">
        <div class="logo" v-if="!isCollapsed"><i class="fas fa-store"></i> فروشگاه</div>
        <button class="toggle-btn" @click="isCollapsed = !isCollapsed">
          <i class="fas fa-bars"></i>
        </button>
      </div>

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
        <BankCard
          card-number="6037991234567890"
          sheba-number="IR123456789012345678901234"
          amount="1200000"
        />
        <Wallet />
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { toast } from "vue3-toastify";

import ShoppingCart from "@/components/ShoppingCart.vue";
import UserProfile from "@/components/UserProfile.vue";
import Wallet from "@/components/Wallet.vue";
import BankCard from "@/components/BankCard.vue";

const isCollapsed = ref(false);
const activeTab = ref("profile");

const logout = () => {
  toast.info("شما از حساب خارج شدید!");
};

const pageTitle = computed(() => {
  switch (activeTab.value) {
    case "profile":
      return "پروفایل کاربر";
    case "cart":
      return "سبد خرید";
    case "wallet":
      return "کیف پول من";
    default:
      return "";
  }
});
</script>

<style scoped>
.admin-panel {
  display: flex;
  min-height: 100vh;
  direction: rtl;
  font-family: sans-serif;
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
}
.sidebar.collapsed {
  width: 60px;
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
