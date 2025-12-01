<template>
  <div class="dashboard">
    <h1 class="title">داشبورد مدیریت</h1>
    <div class="info-boxes">
      <InfoBox
        label="نظرات تایید نشده"
        :value="commentStore.unapproved_count"
        iconClass="fas fa-comments"
        route="/admin/comments"
      />
      <InfoBox
        label="تعداد کاربران"
        :value="usersCount"
        iconClass="fas fa-users"
        route="/admin/userslist"
      />
      <InfoBox
        label="تعداد سفارشات"
        :value="ordersCount"
        iconClass="fas fa-shopping-cart"
        route="/admin/orderlist"
      />
      <InfoBox
        label="تعداد تراکنش ها"
        :value="totalRevenue"
        iconClass="fas fa-money-bill-wave"
        route="/admin/transactions"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue'
import InfoBox from '@/components/InfoBox.vue'
import { useUserStore } from '@/stores/useUserStore'
import { useTransactionStore } from '@/stores/useTransactionStore'
import { useAdminCommentStore } from '@/stores/adminCommentStore'
import { useOrderStore } from '@/stores/useOrderStore'

const userStore = useUserStore()
const transactionStore = useTransactionStore()
const commentStore = useAdminCommentStore()
const orderStore = useOrderStore()


onMounted(async () => {
  await Promise.all([
    userStore.fetchUsers(),
    transactionStore.fetchAll(),
    orderStore.fetchOrders(),
    commentStore.fetchAllComments(), 
  ])
})





const usersCount = computed(() => userStore.users.length || 0)


const ordersCount = computed(() => orderStore.orders.length || 0)

const totalRevenue = computed(() => transactionStore.transactions.length)
</script>

<style scoped>
.dashboard {
  --gold: #f9c710;
  --gold-hover: #e6b800;
  --gold-light: #fff9e6;
  --dark: #1a1a1a;
  --gray-100: #f8f9fa;
  --gray-600: #6c757d;

  font-family: 'IRANSansX', sans-serif;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ed 100%);
  min-height: 100vh;
  padding: 3rem 2rem;
  direction: rtl;
}


.title {
  font-size: 2.8rem;
  font-weight: 900;
  color: var(--dark);
  text-align: center;
  margin: 0 0 4rem 0;
  position: relative;
  letter-spacing: 1px;
}

.title::after {
  content: '';
  position: absolute;
  bottom: -18px;
  left: 50%;
  transform: translateX(-50%);
  width: 200px;
  height: 8px;
  background: linear-gradient(90deg, transparent, var(--gold), transparent);
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(249, 199, 16, 0.4);
}


.info-boxes {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1rem;
}


@media (min-width: 768px) {
  .info-boxes {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1200px) {
  .info-boxes {
    grid-template-columns: repeat(4, 1fr);
    gap: 2.5rem;
  }
}


.info-boxes::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(249,199,16,0.05), transparent);
  animation: shimmer 3s infinite;
  pointer-events: none;
  border-radius: 28px;
  opacity: 0.3;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.dashboard:empty::after {
  content: 'در حال بارگذاری داشبورد...';
  display: block;
  text-align: center;
  font-size: 1.4rem;
  color: var(--gray-600);
  padding: 6rem;
  font-weight: 600;
}
</style>