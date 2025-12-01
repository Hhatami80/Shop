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
  --gold: #f9c710;
  --gold-hover: #e6b800;
  --gold-light: #fff9e6;
  --dark: #1a1a1a;
  --gray-100: #f8f9fa;
  --gray-200: #e9ecef;
  --gray-600: #6c757d;
  --success: #10b981;
  --danger: #dc3545;
  --warning: #ffc107;

  font-family: 'IRANSansX', sans-serif;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ed 100%);
  min-height: 100vh;
  padding: 3rem 2rem;
  direction: rtl;
}


h2 {
  font-size: 2.4rem;
  font-weight: 900;
  color: var(--dark);
  text-align: center;
  margin-bottom: 3rem;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

h2::after {
  content: '';
  position: absolute;
  bottom: -14px;
  left: 50%;
  transform: translateX(-50%);
  width: 160px;
  height: 7px;
  background: var(--gold);
  border-radius: 6px;
}


.admin-transactions > .loading {
  text-align: center;
  padding: 5rem 2rem;
  font-size: 1.5rem;
  color: var(--gray-600);
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 15px 45px rgba(0,0,0,0.1);
  margin: 3rem auto;
  max-width: 600px;
}


.empty-state {
  text-align: center;
  padding: 6rem 2rem;
  background: #fff;
  border-radius: 28px;
  box-shadow: 0 15px 45px rgba(0,0,0,0.1);
  margin: 3rem auto;
  max-width: 700px;
  color: var(--gray-600);
  font-size: 1.4rem;
  font-weight: 500;
}


.transactions-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: #fff;
  border-radius: 28px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.14);
  margin-bottom: 2rem;
}

.transactions-table thead {
  background: linear-gradient(135deg, var(--gold), var(--gold-hover));
  color: #111;
}

.transactions-table th {
  padding: 1.6rem 1.2rem;
  font-weight: 900;
  font-size: 1.15rem;
  text-align: center;
  letter-spacing: 0.5px;
}

.transactions-table tbody tr {
  transition: all 0.35s ease;
  border-bottom: 1px solid #eee;
}

.transactions-table tbody tr:hover {
  background: var(--gold-light);
  transform: translateY(-4px);
  box-shadow: 0 12px 35px rgba(249, 199, 16, 0.18);
}

.transactions-table td {
  padding: 1.4rem 1.2rem;
  text-align: center;
  font-size: 1rem;
  color: var(--dark);
}


.status-badge {
  display: inline-block;
  padding: 0.65rem 1.4rem;
  border-radius: 30px;
  font-size: 0.95rem;
  font-weight: 700;
  min-width: 90px;
  transition: all 0.3s ease;
}

.status-badge.success {
  background: var(--success);
  color: white;
  box-shadow: 0 6px 18px rgba(16, 185, 129, 0.3);
}

.status-badge.failed {
  background: var(--danger);
  color: white;
  box-shadow: 0 6px 18px rgba(220, 53, 69, 0.3);
}

.status-badge.pending {
  background: var(--warning);
  color: #111;
  box-shadow: 0 6px 18px rgba(255, 193, 7, 0.3);
}

.status-badge:hover {
  transform: translateY(-2px);
}


.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
  margin-top: 3rem;
  font-size: 1.1rem;
  font-weight: 600;
}

.pagination-btn {
  padding: 0.9rem 1.8rem;
  background: linear-gradient(135deg, var(--gold), var(--gold-hover));
  color: #111;
  border: none;
  border-radius: 18px;
  font-weight: 900;
  cursor: pointer;
  transition: all 0.35s ease;
  box-shadow: 0 8px 25px rgba(249, 199, 16, 0.35);
  min-width: 110px;
}

.pagination-btn:hover:not(:disabled) {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(249, 199, 16, 0.45);
}

.pagination-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}


@media (max-width: 992px) {
  .transactions-table {
    font-size: 0.92rem;
  }
  .transactions-table th,
  .transactions-table td {
    padding: 1rem 0.8rem;
  }
  .status-badge {
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
  }
}

@media (max-width: 768px) {
  h2 {
    font-size: 2rem;
  }
  
  .transactions-table {
    display: block;
    overflow-x: auto;
    white-space: nowrap;
    border-radius: 20px;
  }
  
  .pagination {
    flex-direction: column;
    gap: 1rem;
  }
  
  .empty-state {
    padding: 4rem 1rem;
    font-size: 1.2rem;
  }
}
</style>