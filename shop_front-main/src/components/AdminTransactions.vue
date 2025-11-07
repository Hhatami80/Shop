<template>
  <div class="admin-transactions">
    <h2>مدیریت تراکنش‌ها</h2>

    <div v-if="loading">در حال بارگذاری...</div>
    <div class="empty-state " v-else-if="!transactions.length">تراکنشی یافت نشد</div>

    <table v-else class="transactions-table">
      <thead>
        <tr>
          <th>کاربر</th>
          <th>مقدار</th>
          <th>نوع تراکنش</th>
          <th>وضعیت</th>
          <th>تاریخ</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="t in transactions" :key="t.id">
          <td>{{ t.user?.name || t.user_id }}</td>
          <td>{{ t.amount }}</td>
          <td>{{ t.type }}</td>
          <td>{{ t.status }}</td>
          <td>{{ new Date(t.created_at).toLocaleString('fa-IR') }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useWalletStore } from '@/stores/useWalletStore'

const store = useWalletStore()
const transactions = ref([])
const loading = ref(true)

onMounted(async () => {
  loading.value = true
  try {
    await store.fetchTransactions()  
    transactions.value = store.transactions
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.admin-transactions{
  max-width: 1200px;
  margin: 40px auto;
  font-family: "Yekan", sans-serif;
  background: #fff;
  padding: 25px;
  border-radius: 16px;
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.08);
  direction: rtl;
}
.transactions-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.transactions-table th,
.transactions-table td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}

.transactions-table th {
  background-color: #f9c710;
  color: white;
}
.empty-state {
  text-align: center;
  padding: 30px;
  color: #777;
}
</style>
