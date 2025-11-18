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
        <tr v-for="user in store.users" :key="user.id">
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
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <h3>جزئیات آدرس{{ selectedUser.usrename }}</h3>
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
            <tr v-for="address in selectedUser.address" :key="address.id">
              <td>{{ address.province.name || "-" }}</td>
              <td>{{ address.city.name || "-" }}</td>
              <td>{{ address.neighborhood || "-" }}</td>
              <td>{{ address.street || "-" }}</td>
              <td>{{ address.plate || "-" }}</td>
              <td>{{ address.postal_code || "-" }}</td>
              <td>{{ address.full_address || "-" }}</td>
            </tr>
            <tr v-if="!selectedUser.address.length">
              <td colspan="7" style="text-align: center">هیچ آدرسی برای این کاربر موجود نیست.</td>
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
import { onMounted, ref } from "vue";
import { useUserStore } from "@/stores/useUserStore";
import Swal from "sweetalert2";

const store = useUserStore();
const showModal = ref(false)
const selectedUser = ref({})

onMounted(() => {
  store.fetchUsers();
});

const handleDelete = (id) => {
  Swal.fire({
    title: '<span style="font-weight:bold; font-size:20px;">آیا مطمئنی؟</span>',
    html: '<p style="font-size:16px;">با حذف این کاریر دیگر قابل بازیابی نیست!</p>',
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#e63946",
    cancelButtonColor: "#adb5bd",
    confirmButtonText: '<i class="fa fa-trash"></i> حذف کاریر',
    cancelButtonText: '<i class="fa fa-times"></i> لغو',
    buttonsStyling: false,
    customClass: {
      popup: "my-swal-popup",
      confirmButton: "my-swal-confirm",
      cancelButton: "my-swal-cancel",
    },
  }).then((result) => {
    if (result.isConfirmed) {
      store.deleteUser(id);
      Swal.fire({
        title: '<span style="font-weight:bold; font-size:20px;">حذف شد!</span>',
        html: '<p style="font-size:16px;">کاریر موردنظر با موفقیت حذف شد.</p>',
        icon: "success",
        confirmButtonText: "باشه",
        buttonsStyling: false,
        customClass: {
          popup: "my-swal-popup",
          confirmButton: "my-swal-confirm",
        },
      });
    }
  });
};

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
  --primary-color: #ffd700;
  --primary-color-hover: #e6c200;
  --secondary-color: #34495e;
  --danger-color: #dc3545;
  --bg-light: #f8f9fa;
  --border-light: #e9ecef;
  --shadow-color: rgba(0, 0, 0, 0.08);

  max-width: 1000px;
  margin: 30px auto;
  padding: 30px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 20px var(--shadow-color);
  direction: rtl;
  font-family: "Vazirmatn", sans-serif;
}

.title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 30px;
  color: var(--secondary-color);
  text-align: right;
  border-bottom: 2px solid var(--border-light);
  padding-bottom: 10px;
}

.loading,
.error {
  text-align: center;
  font-size: 1.1rem;
  padding: 30px;
  border-radius: 8px;
  background-color: var(--bg-light);
  color: var(--secondary-color);
  box-shadow: 0 2px 5px var(--shadow-color);
}
.error {
  color: var(--danger-color);
  background-color: #ffebeb;
}

.user-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 15px var(--shadow-color);
}

.user-table th,
.user-table td {
  padding: 15px;
  text-align: center;
  font-size: 15px;
  border-bottom: 1px solid var(--border-light);
}

.user-table thead tr {
  background: var(--primary-color);
  color: var(--secondary-color);
}

.user-table th {
  font-weight: 700;
  border-right: 1px solid rgba(0, 0, 0, 0.1);
}

.user-table tbody tr:nth-child(even) {
  background: var(--bg-light);
}

.user-table tbody tr:hover {
  background: #fffbe6;
  transition: background 0.3s;
}

.btn {
  padding: 10px 18px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 500;
  transition: 0.3s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-delete {
  background: var(--danger-color);
  color: #fff;
}

.btn-delete:hover {
  background: #b91c1c;
  box-shadow: 0 4px 8px rgba(220, 53, 69, 0.3);
  transform: translateY(-1px);
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


/* modal styles */
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

:global(.my-swal-popup) {
  font-family: "Vazirmatn", sans-serif;
  border-radius: 12px;
  direction: rtl;
}
:global(.my-swal-confirm) {
  background-color: #dc3545 !important;
  color: white !important;
  padding: 10px 20px;
  border-radius: 8px;
  box-shadow: none !important;
  margin: 0 5px;
  transition: background-color 0.3s;
}
:global(.my-swal-cancel) {
  background-color: #34495e !important;
  color: white !important;
  padding: 10px 20px;
  border-radius: 8px;
  box-shadow: none !important;
  margin: 0 5px;
  transition: background-color 0.3s;
}
</style>
