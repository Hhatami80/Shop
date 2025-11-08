<template>
  <div class="admin-transactions">
    <h2>مدیریت تراکنش‌ها</h2>

    <div v-if="store.loading">در حال بارگذاری...</div>
    <div class="empty-state" v-else-if="!store.transactions.length">
      تراکنشی یافت نشد
    </div>

    <table v-else class="transactions-table">
      <thead>
        <tr>
          <th>کاربر</th>
          <th>مبلغ</th>
          <th>نوع تراکنش</th>
          <th>وضعیت</th>
          <th>تاریخ</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="t in store.transactions" :key="t.id">
          <td>{{ t.user?.name || t.user_id || "—" }}</td>
          <td>{{ t.amount?.toLocaleString("fa-IR") }} تومان</td>
          <td>{{ t.type }}</td>
          <td>
            <span
              :class="[
                'status-badge',
                t.status === 'success'
                  ? 'success'
                  : t.status === 'failed'
                  ? 'failed'
                  : 'pending',
              ]"
            >
              {{ translateStatus(t.status) }}
            </span>
          </td>
          <td>{{ formatDate(t.created_at) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useTransactionStore } from "@/stores/useTransactionStore";

const store = useTransactionStore();

const formatDate = (dateStr) => {
  if (!dateStr) return "—";
  return new Date(dateStr).toLocaleString("fa-IR");
};

const translateStatus = (status) => {
  switch (status) {
    case "success":
      return "موفق";
    case "failed":
      return "ناموفق";
    case "pending":
      return "در انتظار";
    default:
      return status;
  }
};

onMounted(async () => {
  await store.fetchAll();
});
</script>

<style scoped>
.admin-transactions {
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
</style>
