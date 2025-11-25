<template>
  <div class="dashboard">
    <h1>داشبورد</h1>
    <div class="cards">
      <InfoBox
        label="تعداد سفارشات"
        :value="ordersCount"
        icon-class="fas fa-shopping-cart"
        route="/user/orders"
      />

      <InfoBox
        label="محصولات سبد خرید"
        :value="cartCount"
        icon-class="fas fa-boxes"
        route="/user/shop-cart"
      />

      <InfoBox
        label="موجودی کیف پول"
        :value="walletBalance + ' تومان'"
        icon-class="fas fa-wallet"
        route="/user/wallet"
      />

      <InfoBox
        label="اطلاعات کاربر"
        :value="userInfo"
        icon-class="fas fa-user"
        route="/user/profile/info"
      >
        
        <template v-if="isUserInfoIncomplete">
          <button @click.stop="goToUpdateProfile" class="complete-profile-btn">
            تکمیل اطلاعات
          </button>
        </template>
      </InfoBox>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useOrderStore } from '@/stores/useOrderStore'
import { useCartStore } from '@/stores/useCartStore'
import { useWalletStore } from '@/stores/useWalletStore'
import { useUserStore } from '@/stores/useUserStore'
import { useRouter } from 'vue-router'
import InfoBox from './InfoBox.vue'

const orderStore = useOrderStore()
const cartStore = useCartStore()
const walletStore = useWalletStore()
const userStore = useUserStore()
const router = useRouter()

onMounted(async () => {
  await Promise.all([
    orderStore.fetchOrders({ forUser: true }),
    cartStore.fetchCart(),
    walletStore.fetchBalance(),
    userStore.fetchProfile()
  ])
})

const ordersCount = computed(() => orderStore.totalOrders)
const cartCount = computed(() => cartStore.totalQuantity)
const walletBalance = computed(() => walletStore.balance)
const userInfo = computed(() => `${userStore.profile.fullname || '-'}\n${userStore.profile.phone || '-'}`)

const isUserInfoIncomplete = computed(() => {
  const { fullname, phone } = userStore.profile
  return !fullname || !phone
})

const goToUpdateProfile = () => {
  router.push('/user/profile/info')
}
</script>

<style scoped>
.dashboard {
  padding: 30px;
  background: linear-gradient(135deg, #fdf6e3 0%, #fff9e6 100%);
  min-height: 100vh;
}
h1 {
  font-size: 2rem;
  margin-bottom: 30px;
  color: #ffd700;
  font-weight: bold;
}
.cards {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  padding: 10px 0;
}


.complete-profile-btn {
  margin-top: 10px;
  background-color: #ff9800;
  color: white;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 0.9rem;
  cursor: pointer;
  border: none;
  transition: background-color 0.3s ease;
}
.complete-profile-btn:hover {
  background-color: #fb8c00;
}

@media (max-width: 700px) {
  .complete-profile-btn {
    font-size: 0.8rem;
    padding: 5px 10px;
  }
}
</style>
