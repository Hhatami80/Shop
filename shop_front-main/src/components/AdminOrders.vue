<template>
  <div class="admin-orders-page">
    <h1>
      <fa-icon :icon="['fas', 'clipboard-list']" class="title-icon" />
      مدیریت سفارش‌ها
    </h1>

    <div class="filter">
      <label>فیلتر بر اساس وضعیت:</label>
      <select v-model="statusFilter" @change="filterOrders">
        <option value="all">همه</option>
        <option value="pending">در انتظار</option>
        <option value="paid">پرداخت شده</option>
        <option value="completed">ارسال شد</option>
        <option value="canceled">لغو شد</option>
      </select>

      <label>تعداد در هر صفحه:</label>
      <select v-model.number="perPageFilter" @change="changePerPage">
        <option :value="5">5</option>
        <option :value="10">10</option>
        <option :value="20">20</option>
        <option :value="50">50</option>
      </select>
    </div>

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
    <th>نام کاربر</th>
    <th>نام و نام خانوادگی</th>
    <th>تاریخ</th>
    <th>جمع کل</th>
    <th>روش پرداخت</th>
    <th>وضعیت</th>          
    <th>تعیین وضعیت</th>   
    <th>جزئیات</th>
  </tr>
</thead>
<tbody>
  <tr v-for="order in orderStore.orders" :key="order.id">
    <td>#{{ order.id }}</td>
    <td>{{ order.user?.username || '---' }}</td>
    <td>{{ order.user?.fullname || '---' }}</td>
    <td>{{ formatDate(order.created_at) }}</td>
    <td>{{ formatPrice(order.total_price) }} تومان</td>
    <td>{{ order.payment.payment_method }}</td>

    
    <td>
      <span :class="['status-badge', getStatusClass(order.status)]">
        {{ translateStatus(order.status) }}
      </span>
    </td>

    
    <td>
      <select
        :value="order.status"
        @change="changeStatus(order, $event)"
        class="status-select"
      >
        <option value="pending">در انتظار</option>
        <option value="paid">پرداخت شده</option>
        <option value="completed">ارسال شد</option>
        <option value="canceled">لغو شد</option>
      </select>
    </td>

    <td>
      <button class="btn-details" @click="openModal(order)">
        مشاهده
      </button>
    </td>
  </tr>
</tbody>
      </table>

      <div class="pagination">
        <button @click="prevPage" :disabled="orderStore.page === 1">
          <fa-icon :icon="['fas', 'chevron-right']" />
        </button>
        <span> صفحه {{ orderStore.page }} از {{ totalPages }} </span>
        <button @click="nextPage" :disabled="orderStore.page === totalPages">
          <fa-icon :icon="['fas', 'chevron-left']" />
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
              <td colspan="4" style="text-align: center">هیچ محصولی در این سفارش موجود نیست.</td>
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
import { ref, computed, onMounted } from 'vue'
import { useOrderStore } from '@/stores/useOrderStore'
import { toast } from 'vue3-toastify'

const orderStore = useOrderStore()
const showModal = ref(false)
const selectedOrder = ref({})
const statusFilter = ref('all')
const perPageFilter = ref(orderStore.perPage)

const totalPages = computed(() => Math.ceil(orderStore.totalOrders / perPageFilter.value))

const fetchOrders = async (page = 1) => {
  await orderStore.fetchOrders({
    page,
    perPage: perPageFilter.value,
    status: statusFilter.value,
    forUser: false,
  })
}

const nextPage = () => {
  if (orderStore.page < totalPages.value) fetchOrders(orderStore.page + 1)
}
const prevPage = () => {
  if (orderStore.page > 1) fetchOrders(orderStore.page - 1)
}

const changePerPage = () => {
  fetchOrders(1)
}

const filterOrders = () => {
  fetchOrders(1)
}

const changeStatus = async (order, event) => {
  const newStatus = event.target.value
  try {
    await orderStore.updateOrderStatus(order.id, newStatus)
    order.status = newStatus
    toast.success('وضعیت سفارش با موفقیت تغییر کرد')
  } catch {
    toast.error('خطا در تغییر وضعیت سفارش')
    event.target.value = order.status 
  }
}
const openModal = (order) => {
  selectedOrder.value = order
  showModal.value = true
}
const closeModal = () => {
  showModal.value = false
}

const deleteOrder = async (orderId) => {
  if (!confirm('آیا از حذف این سفارش مطمئن هستید؟')) return
  try {
    await orderStore.deleteOrder(orderId)
    toast.success('سفارش حذف شد')
    closeModal()
    fetchOrders(orderStore.page)
  } catch {
    toast.error('خطا در حذف سفارش')
  }
}

const formatDate = (dateStr) => (dateStr ? new Date(dateStr).toLocaleDateString('fa-IR') : '-')
const formatPrice = (price) => (price ? Number(price).toLocaleString('fa-IR') : 0)

const translateStatus = (status) => {
  const map = {
    pending: 'در انتظار',
    paid: 'پرداخت شده',
    completed: 'ارسال شد',
    canceled: 'لغو شد'
  }
  return map[status] || status
}

const getStatusClass = (status) => {
  switch (status) {
    case 'pending':   return 'warning'   
    case 'paid':      return 'success'   
    case 'completed': return 'info'      
    case 'canceled':  return 'danger'    
    default:          return 'default'
  }
}

onMounted(() => {
  fetchOrders()
})
</script>

<style scoped>
.admin-orders-page {
  --gold: #f9c710;
  --gold-hover: #e6b800;
  --gold-light: #fff9e6;
  --dark: #1a1a1a;
  --gray-100: #f8f9fa;
  --gray-200: #e9ecef;
  --danger: #ef4444;
  --danger-hover: #dc2626;
  --info: #0dcaf0;
  --success: #10b981;

  font-family: 'IRANSansX', sans-serif;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ed 100%);
  min-height: 100vh;
  padding: 3rem 2rem;
  direction: rtl;
}


h1 {
  font-size: 2.6rem;
  font-weight: 900;
  color: var(--dark);
  text-align: center;
  margin: 0 0 3.5rem 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.title-icon {
  color: var(--gold);
  font-size: 2.8rem;
}

h1::after {
  content: '';
  flex: 1;
  height: 6px;
  background: linear-gradient(90deg, transparent, var(--gold), transparent);
  border-radius: 6px;
  margin-right: 2rem;
}

h1::before {
  content: '';
  flex: 1;
  height: 6px;
  background: linear-gradient(90deg, transparent, var(--gold), transparent);
  border-radius: 6px;
  margin-left: 2rem;
}


.filter {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  background: #fff;
  padding: 1.8rem;
  border-radius: 24px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1);
  margin-bottom: 2.5rem;
  border: 1px solid rgba(249, 199, 16, 0.15);
}

.filter label {
  font-weight: 700;
  color: var(--dark);
  font-size: 1.05rem;
  margin-left: 12px;
}

.filter select {
  padding: 0.9rem 1.2rem;
  border: 2.2px solid #e0e0e0;
  border-radius: 16px;
  background: #fdfdfd;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.35s ease;
}

.filter select:focus {
  outline: none;
  border-color: var(--gold);
  box-shadow: 0 0 0 5px rgba(249, 199, 16, 0.22);
  transform: translateY(-2px);
}


.loading-state,
.empty-state {
  text-align: center;
  padding: 5rem 2rem;
  font-size: 1.5rem;
  color: var(--gray-600);
  background: #fff;
  border-radius: 28px;
  box-shadow: 0 15px 45px rgba(0, 0, 0, 0.1);
  margin: 3rem auto;
  max-width: 700px;
  font-weight: 600;
}

.loading-state svg {
  color: var(--gold);
  font-size: 2.2rem;
  margin-left: 12px;
}


.orders-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: #fff;
  border-radius: 28px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.14);
  margin-bottom: 2rem;
}

.orders-table thead {
  background: linear-gradient(135deg, var(--gold), var(--gold-hover));
  color: #111;
}

.orders-table th {
  padding: 1.6rem 1.2rem;
  font-weight: 900;
  font-size: 1.15rem;
  text-align: center;
}

.orders-table tbody tr {
  transition: all 0.35s ease;
  border-bottom: 1px solid #eee;
}

.orders-table tbody tr:hover {
  background: var(--gold-light);
  transform: translateY(-4px);
  box-shadow: 0 12px 35px rgba(249, 199, 16, 0.18);
}

.orders-table td {
  padding: 1.4rem 1.2rem;
  text-align: center;
  font-size: 1rem;
  color: var(--dark);
}


.orders-table select {
  padding: 0.7rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 14px;
  background: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.orders-table select:focus {
  border-color: var(--gold);
  box-shadow: 0 0 0 4px rgba(249, 199, 16, 0.2);
}


.btn-details {
  background: linear-gradient(135deg, var(--info), #0aa8c9);
  color: white;
  padding: 0.75rem 1.4rem;
  border: none;
  border-radius: 16px;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.35s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-width: 110px;
  justify-content: center;
  box-shadow: 0 8px 25px rgba(13, 202, 240, 0.35);
}

.btn-details:hover {
  background: linear-gradient(135deg, #0aa8c9, #0d6efd);
  transform: translateY(-4px);
  box-shadow: 0 15px 35px rgba(13, 202, 240, 0.5);
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

.pagination button {
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

.pagination button:hover:not(:disabled) {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(249, 199, 16, 0.45);
}

.pagination button:disabled {
  background: #ccc;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}


.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(12px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1rem;
}

.modal {
  background: #fff;
  border-radius: 28px;
  width: 100%;
  max-width: 900px;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
}

.modal h3 {
  padding: 1.8rem 2rem 1.2rem;
  margin: 0;
  font-size: 1.8rem;
  font-weight: 900;
  text-align: center;
  background: linear-gradient(135deg, var(--gold), var(--gold-hover));
  color: #111;
}

.modal-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.98rem;
}

.modal-table th {
  background: var(--gold-light);
  padding: 1.2rem 1rem;
  font-weight: 700;
  color: var(--dark);
  border-bottom: 3px solid var(--gold);
}

.modal-table td {
  padding: 1rem;
  border-bottom: 1px solid #eee;
  background: #fff;
}

.modal-table tbody tr:hover {
  background: var(--gold-light);
}

.modal-actions {
  padding: 1.8rem 2rem;
  background: #f8f9fa;
  border-top: 1px solid #eee;
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn-delete {
  background: var(--danger);
  color: white;
  padding: 1rem 2rem;
  border: none;
  border-radius: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.35s ease;
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn-delete:hover {
  background: var(--danger-hover);
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(239, 68, 68, 0.4);
}

.btn-close {
  background: linear-gradient(135deg, var(--gold), var(--gold-hover));
  color: #111;
  padding: 1rem 2.5rem;
  border: none;
  border-radius: 16px;
  font-weight: 900;
  cursor: pointer;
  transition: all 0.35s ease;
  box-shadow: 0 10px 30px rgba(249, 199, 16, 0.4);
}

.btn-close:hover {
  transform: translateY(-5px);
  box-shadow: 0 18px 40px rgba(249, 199, 16, 0.5);
}

.status-badge-in-table {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 700;
  min-width: 90px;
  text-align: center;
  margin-bottom: 0.5rem;
  transition: all 0.3s ease;
}


.status-badge {
  display: inline-block;
  padding: 0.65rem 1.3rem;
  border-radius: 30px;
  font-size: 0.95rem;
  font-weight: 700;
  min-width: 110px;
  text-align: center;
  color: white;
  text-shadow: 0 1px 2px rgba(0,0,0,0.3);
}

.status-badge.warning  { background: #f59e0b; }  
.status-badge.success  { background: #10b981; }  
.status-badge.info     { background: #0dcaf0; }  
.status-badge.danger   { background: #ef4444; }  


.status-select {
  padding: 0.6rem 1rem;
  border: 2.2px solid #e0e0e0;
  border-radius: 14px;
  background: white;
  font-size: 0.92rem;
  font-weight: 600;
  cursor: pointer;
  width: 100%;
  transition: all 0.3s ease;
  color: #333;
}

.status-select:focus {
  outline: none;
  border-color: var(--gold);
  box-shadow: 0 0 0 5px rgba(249,199,16,0.25);
  transform: translateY(-2px);
}

.status-select option {
  padding: 0.5rem;
}


.modal-table th,
.modal-table td {
  text-align: center !important;
  vertical-align: middle !important;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.modal-table th:nth-child(1),
.modal-table td:nth-child(1) { width: 45%; } 

.modal-table th:nth-child(2),
.modal-table td:nth-child(2) { width: 15%; } 

.modal-table th:nth-child(3),
.modal-table td:nth-child(3) { width: 20%; }

.modal-table th:nth-child(4),
.modal-table td:nth-child(4) { width: 20%; } 


@media (max-width: 992px) {
  .filter {
    grid-template-columns: 1fr;
  }
  .orders-table {
    font-size: 0.92rem;
  }
}

@media (max-width: 768px) {
  h1 {
    font-size: 2.2rem;
    flex-direction: column;
    gap: 12px;
  }
  h1::before,
  h1::after {
    display: none;
  }

  .orders-table {
    display: block;
    overflow-x: auto;
    white-space: nowrap;
  }

  .modal {
    margin: 1rem;
    border-radius: 20px;
  }
}
</style>
