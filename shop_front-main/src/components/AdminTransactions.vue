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

h2 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 22px;
  margin-bottom: 20px;
}


.transactions-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.transactions-table th,
.transactions-table td {
  padding: 12px;
  text-align: center;
  border-bottom: 1px solid #eee;
  font-size: 0.95rem;
}

.transactions-table th {
  background: #ffd700;
  font-weight: 700;
  color: #222;
}

.transactions-table tr:hover td {
  background: #fcfcfc;
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
  background: #28a745;
  color: #fff;
}
.status-badge.failed {
  background: #dc3545;
  color: #fff;
}
.status-badge.pending {
  background: #ffc107;
  color: #222;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 25px;
  gap: 10px;
}

.pagination button {
  padding: 6px 12px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  background: #ffd700;
  color: #222;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.pagination button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.pagination span {
  font-weight: bold;
  color: #444;
}
</style>


