<template>
  <div class="dashboard">
    <h1 class="title">داشبورد مدیریت</h1>
    <div class="info-boxes">
      <InfoBox
        label="نظرات تایید نشده"
        :value="unapprovedCommentsCount"
        iconClass="fas fa-comments"
      />
      <InfoBox
        label="تعداد کاربران"
        :value="usersCount"
        iconClass="fas fa-users"
      />
      <InfoBox
        label="تعداد سفارشات"
        :value="ordersCount"
        iconClass="fas fa-shopping-cart"
      />
      <InfoBox
        label="درآمد کلی"
        :value="totalRevenue"
        iconClass="fas fa-money-bill-wave"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
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
    commentStore.fetchAllComments({ status: 'pending' }), 
  ])
})


const unapprovedCommentsCount = computed(
  () => commentStore.comments.length || 0
)


const usersCount = computed(() => userStore.users.length || 0)


const ordersCount = computed(() => orderStore.orders.length || 0)

const totalRevenue = computed(() => transactionStore.totalRevenue)
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 30px;
}
.title {
  font-size: 1.8rem;
  font-weight: bold;
  color: #444;
}
.info-boxes {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: space-between;
}
</style>
