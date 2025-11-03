<template>
  <div class="admin-orders-page">
    <h1>
      <fa-icon :icon="['fas', 'clipboard-list']" class="title-icon" />
      مدیریت سفارش‌ها
    </h1>

    <div v-if="orderStore.loading" class="loading-state">
      <fa-icon :icon="['fas', 'spinner']" pulse /> در حال بارگذاری سفارش‌ها...
    </div>

    <div v-else-if="!orderStore.orders.length" class="empty-state">
      سفارشی برای نمایش وجود ندارد.
    </div>

    <div v-else>
      <table class="orders-table">
        <thead>
          <tr>
            <th>شماره سفارش</th>
            <th>تاریخ</th>
            <th>جمع کل</th>
            <th>وضعیت</th>
            <th>جزئیات</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in paginatedOrders" :key="order.id">
            <td>#{{ order.id }}</td>
            <td>{{ formatDate(order.created_at) }}</td>
            <td>{{ formatPrice(order.total_price) }} تومان</td>
            <td>
              <select v-model="order.status" @change="changeStatus(order)">
                <option value="pending">در انتظار</option>
                <option value="paid">پرداخت شده</option>
                <option value="completed">ارسال شد</option>
                <option value="canceled">لغو شد</option>
              </select>
            </td>
            <td>
              <button class="btn-details" @click="openModal(order)">
                <fa-icon :icon="['fas', 'eye']" /> مشاهده
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div class="pagination">
        <button @click="prevPage" :disabled="currentPage === 1">
          <fa-icon :icon="['fas', 'chevron-left']" />
        </button>
        <span>صفحه {{ currentPage }} از {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages">
          <fa-icon :icon="['fas', 'chevron-right']" />
        </button>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <h3>جزئیات سفارش #{{ selectedOrder.id }}</h3>
        <table class="modal-table">
          <thead>
            <tr>
              <th>نام محصول</th>
              <th>تعداد</th>
              <th>قیمت واحد</th>
              <th>جمع</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in selectedOrder.items" :key="item.id">
              <td>{{ item.product_detail.title }}</td>
              <td>{{ item.quantity }}</td>
              <td>{{ formatPrice(item.price) }} تومان</td>
              <td>{{ formatPrice(item.quantity * item.price) }} تومان</td>
            </tr>
            <tr v-if="!selectedOrder.items.length">
              <td colspan="4" style="text-align: center">
                هیچ محصولی در این سفارش موجود نیست.
              </td>
            </tr>
          </tbody>
        </table>
        <div class="modal-actions">
          <button class="btn-delete" @click="deleteOrder(selectedOrder.id)">
            <fa-icon :icon="['fas', 'trash']" /> حذف سفارش
          </button>
          <button class="btn-close" @click="closeModal">بستن</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useOrderStore } from "@/stores/useOrderStore";
import { toast } from "vue3-toastify";

const orderStore = useOrderStore();
const showModal = ref(false);
const selectedOrder = ref({});
const currentPage = ref(1);
const perPage = 5;

onMounted(() => {
  orderStore.fetchOrders();
});

const totalPages = computed(() => Math.ceil(orderStore.orders.length / perPage));

const paginatedOrders = computed(() => {
  const start = (currentPage.value - 1) * perPage;
  return orderStore.orders.slice(start, start + perPage);
});

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++;
};
const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--;
};

const formatDate = (dateStr) =>
  dateStr ? new Date(dateStr).toLocaleDateString("fa-IR") : "-";
const formatPrice = (price) => (price ? Number(price).toLocaleString("fa-IR") : 0);

const changeStatus = async (order) => {
  try {
    await orderStore.updateOrderStatus(order.id, order.status);
    toast.success("وضعیت سفارش به‌روزرسانی شد");
  } catch (error) {
    toast.error("خطا در تغییر وضعیت سفارش");
  }
};

const openModal = (order) => {
  selectedOrder.value = order;
  showModal.value = true;
};
const closeModal = () => {
  showModal.value = false;
};

const deleteOrder = async (orderId) => {
  if (!confirm("آیا از حذف این سفارش مطمئن هستید؟")) return;
  try {
    await orderStore.deleteOrder(orderId);
    toast.success("سفارش حذف شد");
    closeModal();
  } catch (err) {
    console.error(err);
    toast.error("خطا در حذف سفارش");
  }
};
</script>

<style scoped>
.admin-orders-page {
  max-width: 1200px;
  margin: 40px auto;
  font-family: "Yekan", sans-serif;
  background: #fff;
  padding: 25px;
  border-radius: 16px;
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.08);
  direction: rtl;
}

h1 {
  display: flex;
  align-items: center;
  gap: 8px;
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

.btn-details {
  background: #007bff;
  color: #fff;
  border: none;
  padding: 6px 10px;
  border-radius: 6px;
  cursor: pointer;
}
.btn-details:hover {
  background: #0056b3;
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
}
.pagination button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
.pagination span {
  font-weight: bold;
  color: #444;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  max-width: 600px;
  width: 90%;
}

.modal h3 {
  margin-bottom: 15px;
  text-align: center;
}

.modal-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 15px;
}
.modal-table th,
.modal-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
}

.btn-close {
  background: #6c757d;
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
}
.btn-close:hover {
  background: #5a6268;
}

.btn-delete {
  background: #dc3545;
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
}
.btn-delete:hover {
  background: #c82333;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 30px;
  color: #777;
}
</style>
