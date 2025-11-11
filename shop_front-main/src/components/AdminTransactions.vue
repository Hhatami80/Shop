<template>
  <div class="admin-transactions">
    <h2>مدیریت تراکنش‌ها</h2>

    <div v-if="store.loading">در حال بارگذاری...</div>
    <div class="empty-state" v-else-if="!store.transactions.length">تراکنشی یافت نشد</div>

    <table v-else class="transactions-table">
      <thead>
        <tr>
          <th>نام کاربری</th>
          <th>نام و نام خانوادگی</th>
          <th>مبلغ</th>
          <th>نوع تراکنش</th>
          <th>کد رهگیری</th>
          <th>وضعیت</th>
          <th>تاریخ</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="t in paginatedTransactions" :key="t.id">
          <td>{{ t.user?.username || t.id || '—' }}</td>
          <td>{{ t.user?.fullname || '—'}}</td>
          <td>{{ t.amount?.toLocaleString('fa-IR') }} تومان</td>
          <td>{{ t.type }}</td>
          <td>{{ t.internal_tracking_id }}</td>
          <td>
            <span
              :class="[
                'status-badge',
                t.status === 'success' ? 'success' : t.status === 'failed' ? 'failed' : 'pending',
              ]"
            >
              {{ translateStatus(t.status) }}
            </span>
          </td>
          <td>{{ formatDate(t.created_at) }}</td>
        </tr>
      </tbody>
    </table>

    <div v-if="totalPages > 1" class="pagination">
      <button class="pagination-btn" :disabled="currentPage === 1" @click="prevPage">قبلی</button>
      <span>صفحه {{ currentPage }} از {{ totalPages }}</span>
      <button class="pagination-btn" :disabled="currentPage === totalPages" @click="nextPage">
        بعدی
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useTransactionStore } from '@/stores/useTransactionStore'

const store = useTransactionStore()

const currentPage = ref(1)
const pageSize = 5

const totalPages = computed(() => Math.ceil(store.transactions.length / pageSize))

const paginatedTransactions = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return store.transactions.slice(start, start + pageSize)
})

function nextPage() {
  if (currentPage.value < totalPages.value) currentPage.value++
}

function prevPage() {
  if (currentPage.value > 1) currentPage.value--
}

const formatDate = (dateStr) => {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleString('fa-IR')
}

const translateStatus = (status) => {
  switch (status) {
    case 'success':
      return 'موفق'
    case 'failed':
      return 'ناموفق'
    case 'pending':
      return 'در انتظار'
    default:
      return status
  }
}

onMounted(async () => {
  await store.fetchAll()
})
</script>

<style scoped>
.admin-transactions {
  max-width: 1200px;
  margin: 40px auto;
  background: #fff;
  padding: 25px;
  border-radius: 16px;
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.08);
  direction: rtl;
  font-family: 'IRANSansX';
}

.transactions-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.transactions-table th,
.transactions-table td {
  border: 1px solid #eee;
  padding: 12px;
  text-align: center;
  font-size: 0.9rem;
}

.transactions-table th {
  background-color: #f9c710;
  color: #fff;
  font-weight: 600;
}

.empty-state {
  text-align: center;
  padding: 30px;
  color: #777;
  font-size: 1rem;
}

.status-badge {
  display: inline-block;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.status-badge.success {
  background: #4caf50;
  color: #fff;
}
.status-badge.failed {
  background: #e53935;
  color: #fff;
}
.status-badge.pending {
  background: #ffb300;
  color: #fff;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-top: 25px;
  font-size: 14px;
  font-weight: 600;
}

.pagination-btn {
  background-color: #ffd700;
  color: #1a1a1a;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.3s;
}

.pagination-btn:hover:not(:disabled) {
  background-color: #e5c100;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
