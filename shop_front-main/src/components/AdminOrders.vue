<template>
  <div class="admin-orders-page">
    <h1>
      <fa-icon :icon="['fas', 'clipboard-list']" class="title-icon" />
      مدیریت سفارش‌ها
    </h1>

    <div v-if="orderStore.loading" class="loading-state">
      <fa-icon :icon="['fas', 'spinner']" pulse /> در حال بارگذاری سفارش‌ها...
    </div>

    <table v-else class="orders-table" v-if="orderStore.orders.length">
      <thead>
        <tr>
          <th>شماره سفارش</th>
          <th>تاریخ</th>
          <th>جمع کل</th>
          <th>وضعیت</th>
          <th>عملیات</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="order in orderStore.orders" :key="order.id">
          <td>#{{ order.id }}</td>
          <td>{{ new Date(order.created_at).toLocaleDateString() }}</td>
          <td>{{ order.total_price.toLocaleString() }} تومان</td>
          <td>
            <select v-model="order.status" @change="changeStatus(order)">
              <option value="pending">در انتظار</option>
              <option value="paid">پرداخت شده</option>
              <option value="shipped">ارسال شد</option>
              <option value="canceled">لغو شد</option>
            </select>
          </td>
          <td>
            <button class="btn-delete" @click="deleteOrder(order.id)">
              <fa-icon :icon="['fas', 'trash']" /> حذف
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-else class="empty-state">سفارشی برای نمایش وجود ندارد.</div>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useOrderStore } from "@/stores/useOrderStore";
import { toast } from "vue3-toastify";

const orderStore = useOrderStore();

const changeStatus = async (order) => {
  await orderStore.updateOrderStatus(order.id, order.status);
};

const deleteOrder = async (orderId) => {
  if (!confirm("آیا از حذف این سفارش مطمئن هستید؟")) return;
  await orderStore.deleteOrder(orderId);
};

onMounted(() => {
  orderStore.fetchOrders();
});
</script>

<style scoped>
.admin-orders-page {
  max-width: 1200px;
  margin: 40px auto;
  font-family: "Vazirmatn", sans-serif;
  background: #fff;
  padding: 25px;
  border-radius: 16px;
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.08);
}

h1 {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 24px;
  margin-bottom: 20px;
  color: #222;
}

.title-icon {
  color: #f9c710;
  font-size: 1.5rem;
}

.orders-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.orders-table th,
.orders-table td {
  padding: 12px;
  text-align: center;
  border-bottom: 1px solid #eee;
}

.orders-table th {
  background: #ffd700;
  color: #1a1a1a;
  font-weight: 700;
}

.orders-table tr:hover td {
  background: #fcfcfc;
}

select {
  padding: 6px 10px;
  border-radius: 6px;
  border: 1px solid #ddd;
  cursor: pointer;
}

.btn-delete {
  background: #dc3545;
  color: #fff;
  border: none;
  padding: 6px 10px;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.3s;
}

.btn-delete:hover {
  background: #c82333;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 30px;
  color: #777;
  font-size: 16px;
}

.loading-state .fa-icon {
  color: #ffd700;
  margin-left: 6px;
}
</style>
