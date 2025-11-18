<template>
  <div class="dashboard">
    <h1>داشبورد</h1>
    <div class="cards">
      <InfoBox
        label="تعداد سفارشات"
        :value="ordersCount"
        icon-class="fas fa-shopping-cart"
      />
      <InfoBox
        label="محصولات سبد خرید"
        :value="cartCount"
        icon-class="fas fa-boxes"
      />
      <InfoBox
        label="موجودی کیف پول"
        :value="walletBalance + ' تومان'"
        icon-class="fas fa-wallet"
      />
      <InfoBox
        label="اطلاعات کاربر"
        :value="userInfo"
        icon-class="fas fa-user"
      />
    </div>
  </div>
</template>

<script>
import { computed, onMounted } from 'vue'
import { useOrderStore } from '@/stores/useOrderStore'
import { useCartStore } from '@/stores/useCartStore'
import { useWalletStore } from '@/stores/useWalletStore'
import { useUserStore } from '@/stores/useUserStore'
import InfoBox from './InfoBox.vue'

export default {
  components: { InfoBox },
  setup() {
    const orderStore = useOrderStore()
    const cartStore = useCartStore()
    const walletStore = useWalletStore()
    const userStore = useUserStore()

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
    const userInfo = computed(() => `${userStore.profile.username || '-'}\n${userStore.profile.phone || '-'}`)

    return { ordersCount, cartCount, walletBalance, userInfo }
  },
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
  display: flex;
  gap: 20px;
  overflow-x: auto;
  padding-bottom: 10px;
  -webkit-overflow-scrolling: touch;
}
.cards::-webkit-scrollbar {
  height: 6px;
}
.cards::-webkit-scrollbar-thumb {
  background: rgba(0,0,0,0.2);
  border-radius: 3px;
}
.cards::-webkit-scrollbar-track {
  background: transparent;
}

.info-box {
  flex: 0 0 250px; 
  background: #fff;
  border-radius: 15px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.08);
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  border-top: 5px solid #f1c40f; 
  transition: transform 0.3s, box-shadow 0.3s;
  min-height: 100px;
}
.info-box:hover {
  transform: translateY(-6px);
  box-shadow: 0 15px 30px rgba(0,0,0,0.12);
}


.icon {
  font-size: 2.5rem;
  color: #000; 
  min-width: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
}


.content {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.label {
  font-size: 0.95rem;
  color: #7f8c8d;
  margin-bottom: 4px;
  font-weight: 500;
}
.value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2c3e50;
  white-space: pre-line; 
  line-height: 1.4;
}

@media (max-width: 1000px) {
  .info-box {
    flex: 0 0 220px;
  }
}
@media (max-width: 700px) {
  .info-box {
    flex: 0 0 180px;
    padding: 15px;
  }
  .icon {
    font-size: 2rem;
  }
  .value {
    font-size: 1.2rem;
  }
}
</style>

