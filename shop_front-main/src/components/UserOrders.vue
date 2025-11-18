<template>
  <div class="user-orders">
    <h2>
      <fa-icon :icon="['fas', 'box']" class="title-icon" />
      سفارش‌های من
    </h2>

    <div class="filters">
      <label>
        وضعیت سفارش:
        <select v-model="filterStatus">
          <option value="">همه</option>
          <option value="pending">در انتظار پرداخت</option>
          <option value="paid">پرداخت شده</option>
          <option value="completed">ارسال شده</option>
          <option value="canceled">لغو شده</option>
        </select>
      </label>

      <label>
        از تاریخ:
        <component
          :is="DatePicker"
          v-if="datePickerLoaded"
          v-model="filterStartDate"
          format="jYYYY/jMM/jDD"
          display-format="jYYYY/jMM/jDD"
          placeholder="انتخاب تاریخ"
          color="#f9c710"
          position="bottom"
        />
      </label>

      <label>
        تا تاریخ:
        <component
          :is="DatePicker"
          v-if="datePickerLoaded"
          v-model="filterEndDate"
          format="jYYYY/jMM/jDD"
          display-format="jYYYY/jMM/jDD"
          placeholder="انتخاب تاریخ"
          color="#f9c710"
          position="bottom"
        />
      </label>

      <button class="btn btn-filter" @click="applyFilters">اعمال فیلتر</button>
      <button class="btn btn-reset" @click="resetFilters">پاک‌سازی</button>
    </div>

    <div v-if="orderStore.loading" class="loading">
      <fa-icon :icon="['fas', 'spinner']" pulse /> در حال دریافت سفارش‌ها...
    </div>

    <div v-else-if="!orderStore.orders.length" class="empty">
      <fa-icon :icon="['fas', 'inbox']" /> هنوز سفارشی ثبت نکرده‌اید.
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
            <th>عملیات</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in orderStore.orders" :key="order.id">
            <td>#{{ order.id }}</td>
            <td>{{ formatDate(order.created_at) }}</td>
            <td>{{ formatPrice(order.total_price) }} تومان</td>
            <td>
              <span :class="['status', getStatusClass(order.status)]">
                {{ getStatusText(order.status) }}
              </span>
            </td>
            <td>
              <button class="btn-details" @click="openModal(order)">مشاهده</button>
            </td>
            <td>
              <button
                class="btn-cancel"
                :disabled="order.status !== 'pending'"
                @click="cancelOrder(order)"
              >
                لغو سفارش
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div class="pagination" v-if="orderStore.totalOrders > orderStore.perPage">
        <button @click="prevPage" :disabled="orderStore.page === 1">
          <fa-icon :icon="['fas', 'chevron-right']" />
        </button>
        <span>صفحه {{ orderStore.page }} از {{ totalPages }}</span>
        <button @click="nextPage" :disabled="orderStore.page === totalPages">
          <fa-icon :icon="['fas', 'chevron-left']" />
        </button>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <div class="modal-header">
          <h3>جزییات سفارش #{{ selectedOrder.id }}</h3>
          <button class="close-btn" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <table class="modal-table">
            <thead>
              <tr>
                <th>محصول</th>
                <th>تعداد</th>
                <th>قیمت واحد</th>
                <th>جمع</th>
                <th>روش پرداخت</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in selectedOrder.items" :key="item.id">
                <td>{{ item.product_detail.title }}</td>
                <td>{{ item.quantity }}</td>
                <td>{{ formatPrice(item.price) }}</td>
                <td>{{ formatPrice(item.price * item.quantity) }} تومان</td>
                <td>{{ selectedOrder.payment.payment_method }}</td>
              </tr>
              <tr v-if="!selectedOrder.items.length">
                <td colspan="5" class="empty-items">این سفارش محصولی ندارد.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useOrderStore } from '@/stores/useOrderStore'
import jalaali from 'jalaali-js'
import { toast } from 'vue3-toastify'

const orderStore = useOrderStore()
const showModal = ref(false)
const selectedOrder = ref({})

const DatePicker = ref(null)
const datePickerLoaded = ref(false)

const filterStatus = ref('')
const filterStartDate = ref('')
const filterEndDate = ref('')

const totalPages = computed(() => Math.ceil(orderStore.totalOrders / orderStore.perPage))

const fetchOrders = async (page = 1) => {
  await orderStore.fetchOrders({
    page,
    perPage: orderStore.perPage,
    status: filterStatus.value || 'all',
    forUser: true,
    startDate: filterStartDate.value || undefined,
    endDate: filterEndDate.value || undefined,
  })
}

const applyFilters = async () => fetchOrders(1)

const resetFilters = async () => {
  filterStatus.value = ''
  filterStartDate.value = ''
  filterEndDate.value = ''
  await fetchOrders(1)
}

const nextPage = () => {
  if (orderStore.page < totalPages.value) fetchOrders(orderStore.page + 1)
}
const prevPage = () => {
  if (orderStore.page > 1) fetchOrders(orderStore.page - 1)
}

const openModal = (order) => {
  selectedOrder.value = order
  showModal.value = true
}
const closeModal = () => {
  showModal.value = false
}
const cancelOrder = async (order) => {
  if (!confirm('آیا مطمئن هستید می‌خواهید این سفارش را لغو کنید؟')) return
  await orderStore.cancelUserOrder(order.id)
  await fetchOrders(orderStore.page)
}

const formatDate = (dateStr) => new Intl.DateTimeFormat('fa-IR').format(new Date(dateStr))
const formatPrice = (price) => Number(price)?.toLocaleString('fa-IR') || '0'
const getStatusText = (status) =>
  ({
    pending: 'در انتظار پرداخت',
    paid: 'پرداخت‌شده',
    completed: 'ارسال‌شده',
    canceled: 'لغو‌شده',
  })[status] || ''
const getStatusClass = (status) =>
  ({
    pending: 'status-pending',
    paid: 'status-paid',
    completed: 'status-completed',
    canceled: 'status-canceled',
  })[status] || ''

onMounted(async () => {
  const dp = await import('vue3-persian-datetime-picker')
  DatePicker.value = dp.default
  datePickerLoaded.value = true
  fetchOrders()
})
</script>

<style scoped>
.user-orders {
  max-width: 900px;
  margin: 40px auto;

  background: #fff;
  padding: 25px;
  border-radius: 16px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
  direction: rtl;
}

h2 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 22px;
  margin-bottom: 20px;
  color: #222;
}
.title-icon {
  color: #f9c710;
}

.orders-table {
  width: 100%;
  border-collapse: collapse;
}
.orders-table th,
.orders-table td {
  padding: 12px;
  border-bottom: 1px solid #eee;
  text-align: center;
}
.orders-table th {
  background: #ffd700;
  font-weight: 700;
}

.status {
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: bold;
  color: #fff;
}
.status-pending {
  background: #ffc107;
}
.status-paid {
  background: #28a745;
}
.status-completed {
  background: #007bff;
}
.status-canceled {
  background: #dc3545;
}

.btn-details {
  background: #007bff;
  color: #fff;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
}
.btn-details:hover {
  background: #0056b3;
}

.btn-cancel {
  background: #dc3545;
  color: #fff;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
}
.btn-cancel:disabled {
  background: #aaa;
  cursor: not-allowed;
}

.loading,
.empty {
  text-align: center;
  font-size: 16px;
  padding: 30px;
  color: #777;
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
  max-width: 700px;
  width: 90%;
  padding: 20px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
}

.modal-table {
  width: 100%;
  border-collapse: collapse;
}
.modal-table th,
.modal-table td {
  border: 1px solid #eee;
  padding: 8px;
  text-align: center;
}
.modal-table th {
  background-color: #ffd700;
}
.empty-items {
  text-align: center;
  color: #777;
  font-style: italic;
}
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
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
}
.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 24px;
  align-items: center;
  background: #fff7cc;
  padding: 12px 16px;
  border: 1px solid #ffe28a;
  border-radius: 8px;
}

.filters label {
  display: flex;
  flex-direction: column;
  font-size: 14px;
  gap: 4px;
  color: #333;
}

.filters input[type='date'],
.filters select {
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: #fff;
  font-size: 14px;
  width: 180px;
  outline: none;
  transition: all 0.2s ease;
}

.filters input[type='date']:focus,
.filters select:focus {
  border-color: #f9c710;
}

.filters button {
  margin-top: 22px;
  padding: 8px 16px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-filter {
  background: #28a745;
  color: white;
}

.btn-filter:hover {
  background: #218838;
}

.btn-reset {
  background: #dc3545;
  color: white;
}

.btn-reset:hover {
  background: #c82333;
}

@media (max-width: 600px) {
  .filters {
    flex-direction: column;
  }

  .filters label {
    width: 100%;
  }

  .filters input[type='date'],
  .filters select {
    width: 100%;
  }

  .filters button {
    width: 100%;
  }
}
</style>
