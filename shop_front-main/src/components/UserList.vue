<template>
  <div class="user-list-container">
    <h2 class="title">مدیریت کاربران</h2>

    <div v-if="store.loading" class="loading">در حال بارگذاری...</div>

    <table v-else class="user-table">
      <thead>
        <tr>
          <th>شناسه</th>
          <th>نام کاربری</th>
          <th>ایمیل</th>
          <th>شماره تلفن</th>
          <th>ادرس</th>
          <th>عملیات</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in paginatedUsers" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.phone }}</td>
          <!-- <td>{{ user.address || '-' }}</td> -->
          <td>
            <button class="btn-details" @click="openModal(user)">
              <fa-icon :icon="['fas', 'eye']" /> مشاهده
            </button>
          </td>
          <td>
            <button class="btn btn-delete" @click="handleDelete(user.id)">حذف</button>
          </td>
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
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <h3>جزئیات آدرس{{ selectedUser.username }}</h3>
        <table class="modal-table">
          <thead>
            <tr>
              <th>استان</th>
              <th>شهر</th>
              <th>محله</th>
              <th>خیابان</th>
              <th>پلاک</th>
              <th>کد پستی</th>
              <th>آدرس کامل</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="address in selectedUser.address || []" :key="address.id">
              <td>{{ address.province.name || '-' }}</td>
              <td>{{ address.city.name || '-' }}</td>
              <td>{{ address.neighborhood || '-' }}</td>
              <td>{{ address.street || '-' }}</td>
              <td>{{ address.plate || '-' }}</td>
              <td>{{ address.postal_code || '-' }}</td>
              <td>{{ address.full_address || '-' }}</td>
            </tr>
            <tr v-if="!selectedUser.address.length">
              <td colspan="7" style="text-align: center">هیچ آدرسی برای این کاربر موجود نیست</td>
            </tr>
          </tbody>
        </table>

        <div class="modal-actions">
          <button class="btn-close" @click="closeModal">بستن</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useUserStore } from '@/stores/useUserStore'
import Swal from 'sweetalert2'

const store = useUserStore()
const showModal = ref(false)
const selectedUser = ref({})

const currentPage = ref(1)
const pageSize = 5

const totalPages = computed(() => Math.ceil(store.users.length / pageSize))

const paginatedUsers = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return store.users.slice(start, start + pageSize)
})

function nextPage() {
  if (currentPage.value < totalPages.value) currentPage.value++
}

function prevPage() {
  if (currentPage.value > 1) currentPage.value--
}

onMounted(() => {
  store.fetchUsers()
})

const handleDelete = (id) => {
  Swal.fire({
    title: '<span style="font-weight:bold; font-size:20px;">آیا مطمئنی؟</span>',
    html: '<p style="font-size:16px;">با حذف این کاریر دیگر قابل بازیابی نیست!</p>',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#e63946',
    cancelButtonColor: '#adb5bd',
    confirmButtonText: '<i class="fa fa-trash"></i> حذف کاریر',
    cancelButtonText: '<i class="fa fa-times"></i> لغو',
    buttonsStyling: false,
    customClass: {
      popup: 'my-swal-popup',
      confirmButton: 'my-swal-confirm',
      cancelButton: 'my-swal-cancel',
    },
  }).then((result) => {
    if (result.isConfirmed) {
      store.deleteUser(id)
      Swal.fire({
        title: '<span style="font-weight:bold; font-size:20px;">حذف شد!</span>',
        html: '<p style="font-size:16px;">کاریر موردنظر با موفقیت حذف شد.</p>',
        icon: 'success',
        confirmButtonText: 'باشه',
        buttonsStyling: false,
        customClass: {
          popup: 'my-swal-popup',
          confirmButton: 'my-swal-confirm',
        },
      })
    }
  })
}

const openModal = (user) => {
  selectedUser.value = user
  showModal.value = true
}
const closeModal = () => {
  showModal.value = false
}
</script>

<style scoped>
.user-list-container {
  --gold: #f9c710;
  --gold-hover: #e6b800;
  --gold-light: #fff9e6;
  --dark: #1a1a1a;
  --gray-100: #f8f9fa;
  --gray-200: #e9ecef;
  --gray-600: #6c757d;
  --danger: #dc3545;
  --danger-hover: #c82333;
  --info: #0dcaf0;
  --success: #10b981;

  font-family: 'IRANSansX', sans-serif;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ed 100%);
  min-height: 100vh;
  padding: 3rem 2rem;
  direction: rtl;
}


.title {
  font-size: 2.4rem;
  font-weight: 900;
  color: var(--dark);
  text-align: center;
  margin-bottom: 3rem;
  position: relative;
}

.title::after {
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


.loading {
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


.user-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: #fff;
  border-radius: 28px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.14);
  margin-bottom: 2rem;
}

.user-table thead {
  background: linear-gradient(135deg, var(--gold), var(--gold-hover));
  color: #111;
}

.user-table th {
  padding: 1.6rem 1.2rem;
  font-weight: 900;
  font-size: 1.15rem;
  text-align: center;
  letter-spacing: 0.5px;
}

.user-table tbody tr {
  transition: all 0.35s ease;
  border-bottom: 1px solid #eee;
}

.user-table tbody tr:hover {
  background: var(--gold-light);
  transform: translateY(-4px);
  box-shadow: 0 12px 35px rgba(249, 199, 16, 0.18);
}

.user-table td {
  padding: 1.4rem 1.2rem;
  text-align: center;
  font-size: 1rem;
  color: var(--dark);
}


.btn {
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
  min-width: 100px;
  justify-content: center;
}


.btn-details {
  background: linear-gradient(135deg, #17a2b8, #138496);
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
  box-shadow: 0 8px 25px rgba(23, 162, 184, 0.35);
}

.btn-details:hover {
  background: linear-gradient(135deg, #138496, #0d6efd);
  transform: translateY(-4px);
  box-shadow: 0 15px 35px rgba(23, 162, 184, 0.5);
}

.btn-details svg {
  font-size: 1.15rem;
}

.btn-delete {
  background: var(--danger);
  color: white;
}

.btn-delete:hover {
  background: var(--danger-hover);
  transform: translateY(-4px);
  box-shadow: 0 10px 25px rgba(220, 53, 69, 0.45);
}


.btn svg {
  font-size: 1.1rem;
}


.pagination {
  display: center;
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


.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(10px);
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
  font-size: 1.7rem;
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

.modal-table tbody tr:last-child td {
  border-bottom: none;
}

.modal-table td:empty::before,
.modal-table td:has(span:empty)::before {
  content: '—';
  color: #999;
  font-style: italic;
}

.modal-actions {
  padding: 1.8rem 2rem;
  background: #f8f9fa;
  border-top: 1px solid #eee;
  text-align: center;
}

.btn-close {
  padding: 1rem 3rem;
  background: linear-gradient(135deg, var(--gold), var(--gold-hover));
  color: #111;
  border: none;
  border-radius: 20px;
  font-size: 1.15rem;
  font-weight: 900;
  cursor: pointer;
  transition: all 0.4s ease;
  box-shadow: 0 10px 30px rgba(249, 199, 16, 0.4);
}

.btn-close:hover {
  transform: translateY(-5px);
  box-shadow: 0 18px 40px rgba(249, 199, 16, 0.5);
}


tr td[colspan="7"] {
  padding: 3rem !important;
  font-size: 1.2rem;
  color: var(--gray-600);
  font-style: italic;
}


@media (max-width: 992px) {
  .user-table {
    font-size: 0.92rem;
  }
  .user-table th,
  .user-table td {
    padding: 1rem 0.8rem;
  }
}

@media (max-width: 768px) {
  .title {
    font-size: 2rem;
  }

  .user-table {
    display: block;
    overflow-x: auto;
    white-space: nowrap;
  }

  .pagination {
    flex-direction: column;
    gap: 1rem;
  }

  .modal {
    margin: 1rem;
 
    border-radius: 20px;
  }
}
</style>
