<template>
  <div class="container py-4">
    <div class="title">
      <h4>مدیریت نظرات کاربران</h4>
    </div>

    <div class="row g-3 mb-4">
      <div class="col-12">
        <div class="d-flex flex-wrap gap-4 align-items-end">
          <div class="filters-row">
            <div class="filter-group">
              <label class="form-label fw-bold mb-1">جستجو</label>
              <input
                v-model="commentStore.q"
                @input="handleSearch"
                type="text"
                class="form-control-comment"
                placeholder="جستجو در متن نظر..."
              />
            </div>

            <div class="filter-group">
              <label class="form-label fw-bold mb-1">وضعیت نظرات</label>
              <select
                v-model="commentStore.status"
                @change="
                  () => {
                    commentStore.page = 1
                    commentStore.fetchAllComments()
                  }
                "
                class="form-select-comment"
              >
                <option value="all">همه وضعیت‌ها</option>
                <option value="approved">تایید شده</option>
                <option value="unapproved">در انتظار تایید</option>
              </select>
            </div>

            <div class="filter-group">
              <label class="form-label fw-bold mb-1">تعداد در صفحه</label>
              <select
                v-model="commentStore.per_page"
                @change="
                  () => {
                    commentStore.page = 1
                    commentStore.fetchAllComments()
                  }
                "
                class="form-select-comment"
              >
                <option :value="5">۵ در صفحه</option>
                <option :value="10">۱۰ در صفحه</option>
                <option :value="20">۲۰ در صفحه</option>
              </select>
            </div>
          </div>
        </div>

        <div class="text-center mt-3 d-flex justify-content-center gap-3">
          <button
            class="btn accept-btn btn-sm"
            @click="handleApproveSelected"
            :disabled="commentStore.selectedComments.length === 0"
          >
            تایید انتخاب‌شده‌ها
          </button>

          <button
            class="btn delete-btn btn-sm"
            @click="deleteSelectedComments"
            :disabled="commentStore.selectedComments.length === 0"
          >
            حذف انتخاب‌شده‌ها
          </button>
        </div>
      </div>
    </div>

    <div v-if="commentStore.loading" class="text-center my-5">
      <div class="spinner-border text-primary"></div>
      <p class="mt-3">در حال بارگذاری نظرات...</p>
    </div>

    <div v-else-if="commentStore.error" class="alert alert-danger">
      {{ commentStore.error }}
    </div>

    <div v-else>
      <div class="table-responsive">
        <table class="table table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th scope="col">
                <input type="checkbox" @change="toggleAll" />
              </th>
              <th>نام کاربر</th>
              <th>نام محصول</th>
              <th scope="col">متن نظر</th>
              <th scope="col">وضعیت</th>
              <th scope="col" class="text-center">عملیات</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="comment in commentStore.comments" :key="comment.id">
              <td>
                <input
                  type="checkbox"
                  :value="comment.id"
                  v-model="commentStore.selectedComments"
                />
              </td>
              <td>{{ comment.user?.username }}</td>
              <td>{{ comment.product?.title }}</td>
              <td>{{ comment.text }}</td>
              <td>
                <span
                  :class="['badge', comment.is_approved ? 'bg-success' : 'bg-warning text-dark']"
                >
                  {{ comment.is_approved ? 'تایید شده' : 'در انتظار تایید' }}
                </span>
              </td>
              <td class="text-center">
                <button
                  v-if="!comment.is_approved"
                  class="btn btn-sm btn-success me-2"
                  @click="handleApprove(comment.id)"
                >
                  تایید
                </button>
                <button class="btn btn-sm btn-danger" @click="handleDelete(comment.id)">حذف</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <Pagination
      :page="commentStore.page"
      :totalPages="commentStore.totalPages"
      :maxPages="5"
      @page-change="changePage"
    />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAdminCommentStore } from '@/stores/adminCommentStore'
import Pagination from '@/components/Paginator.vue'
import Swal from 'sweetalert2'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

const commentStore = useAdminCommentStore()

onMounted(() => {
  commentStore.fetchAllComments()
})

function toggleAll(e) {
  if (e.target.checked) {
    commentStore.selectedComments = commentStore.comments.map((c) => c.id)
  } else {
    commentStore.selectedComments = []
  }
}

const handleDelete = async (id) => {
  Swal.fire({
    title: '<span style="font-weight:bold; font-size:20px;">آیا مطمئنی؟</span>',
    html: '<p style="font-size:16px;">با حذف این نظرات دیگر قابل بازیابی نیست!</p>',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#e63946',
    cancelButtonColor: '#adb5bd',
    confirmButtonText: '<i class="fa fa-trash"></i> حذف نظرات',
    cancelButtonText: '<i class="fa fa-times"></i> لغو',
    buttonsStyling: false,
    customClass: {
      popup: 'my-swal-popup',
      confirmButton: 'my-swal-confirm',
      cancelButton: 'my-swal-cancel',
    },
  }).then((result) => {
    if (result.isConfirmed) {
      commentStore.deleteComment(id)
      Swal.fire({
        title: '<span style="font-weight:bold; font-size:20px;">حذف شد!</span>',
        html: '<p style="font-size:16px;">نظرات موردنظر با موفقیت حذف شد.</p>',
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

const handleApprove = async (id) => {
  await commentStore.approveComment(id)
  toast.success('نظر تایید شد')
}

const handleApproveSelected = async () => {
  await commentStore.approveSelected()
  const comment = commentStore.comments.find((c) => c.id === id)
  if (comment) comment.is_approved = true
  toast.success('نظرات انتخاب شده تایید شدند')
}

const deleteSelectedComments = async () => {
  Swal.fire({
    title: '<span style="font-weight:bold; font-size:20px;">آیا مطمئنی؟</span>',
    html: '<p style="font-size:16px;">با حذف این نظرات دیگر قابل بازیابی نیست!</p>',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#e63946',
    cancelButtonColor: '#adb5bd',
    confirmButtonText: '<i class="fa fa-trash"></i> حذف نظرات',
    cancelButtonText: '<i class="fa fa-times"></i> لغو',
    buttonsStyling: false,
    customClass: {
      popup: 'my-swal-popup',
      confirmButton: 'my-swal-confirm',
      cancelButton: 'my-swal-cancel',
    },
  }).then((result) => {
    if (result.isConfirmed) {
      commentStore.deleteSelectedComments()
      Swal.fire({
        title: '<span style="font-weight:bold; font-size:20px;">حذف شد!</span>',
        html: '<p style="font-size:16px;">نظرات موردنظر با موفقیت حذف شد.</p>',
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

function changePage(p) {
  commentStore.page = p
  commentStore.fetchAllComments()
}

let debounceTimeout
function handleSearch() {
  clearTimeout(debounceTimeout)
  debounceTimeout = setTimeout(() => {
    commentStore.page = 1
    commentStore.fetchAllComments()
  }, 500)
}
</script>

<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
button,
.form-select-comment,
.form-control-comment,
.container,
h4,
.table {
  font-family: 'IRANSansX', sans-serif !important;
  direction: rtl;
  
}
.title{
  display: flex;
  justify-content: center;
  text-align: center;
}

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2.5rem 1.5rem;
  background-color: #f8f9fa;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

h4 {
  font-size: 2rem;
  font-weight: 800;
  color: #212529;
  margin-bottom: 2rem !important;
  padding-bottom: 0.75rem;
  border-bottom: 4px solid #ffc107;
  text-align: right;
}

.d-flex.flex-wrap.gap-4 {
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #e9ecef;
}

.filters-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  align-items: flex-end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  min-width: 180px;
}

.form-label {
  font-size: 0.95rem;
  font-weight: 600;
  color: #495057;
  margin-bottom: 0.5rem !important;
  text-align: right;
}

.form-select-comment,
.form-control-comment {
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 0.9rem;
  border: 1px solid #ced4da;
  border-radius: 8px;
  background-color: #ffffff;
  color: #343a40;
  transition: all 0.3s ease-in-out;
}

.form-select-comment:focus,
.form-control-comment:focus {
  outline: none;
  background-color: #fff;
}

.text-center.mt-3.d-flex {
  justify-content: center !important;
  gap: 1rem !important;
  margin-top: 1.5rem !important;
  padding-bottom: 1rem;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 600 !important;
  border: none !important;
  cursor: pointer;
  transition:
    background-color 0.3s ease,
    transform 0.2s ease,
    opacity 0.3s ease;
  white-space: nowrap;
}

.btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15) !important;
}

.btn:disabled {
  background-color: #cccccc !important;
  color: #6c757d !important;
  cursor: not-allowed;
  opacity: 0.7;
  transform: none;
  box-shadow: none !important;
}

.accept-btn,
.delete-btn {
  padding: 0.6rem 1.5rem !important;
  font-size: 1rem !important;
  border-radius: 10px !important;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1) !important;
}

.accept-btn {
  background-color: #4caf50 !important;
  color: white !important;
}

.accept-btn:hover:not(:disabled) {
  background-color: #43a047 !important;
}

.delete-btn {
  background-color: #f44336 !important;
  color: white !important;
}

.delete-btn:hover:not(:disabled) {
  background-color: #e53935 !important;
}

.table-responsive {
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
  margin-top: 1rem;
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  text-align: right;
}

.table thead.table-light {
  background-color: #ffc300 !important;
}

.table thead th {
  font-weight: 700 !important;
  font-size: 0.95rem;
  color: #212529 !important;
  padding: 1rem 1.2rem;
  border-bottom: 3px solid #ffaa00 !important;
}

.table th,
.table td {
  padding: 1rem 1.2rem;
  vertical-align: middle;
  border-bottom: 1px solid #e0e0e0;
  color: #343a40;
}

.table-hover tbody tr:hover {
  background-color: #f0f4f7 !important;
}

input[type='checkbox'] {
  transform: scale(1.2);
  accent-color: #4caf50;
}

.badge {
  display: inline-block;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  min-width: max-content;
  text-align: center;
}

.bg-success {
  background-color: #4caf50 !important;
  color: #fff !important;
}

.bg-warning {
  background-color: #ffc107 !important;
  color: #333 !important;
}
.text-center .btn-sm {
  padding: 0.4rem 0.75rem !important;
  font-size: 0.8rem !important;
  font-weight: 600 !important;
  border-radius: 50px !important;
  margin: 0 0.3rem !important;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
}

.text-center .btn-sm.btn-success {
  background-color: #388e3c !important;
  color: #fff !important;
}

.text-center .btn-sm.btn-success:hover {
  background-color: #2e7d32 !important;
}

.text-center .btn-sm.btn-danger {
  background-color: #d32f2f !important;
  color: #fff !important;
}

.text-center .btn-sm.btn-danger:hover {
  background-color: #c62828 !important;
}

@media (max-width: 768px) {
  .page-title {
    font-size: 1.5rem;
  }
  .filters-row {
    flex-direction: column;
    align-items: stretch;
  }
  .bulk-actions-container {
    flex-direction: column;
    gap: 0.8rem;
  }
  .accept-btn,
  .delete-btn {
    width: 100%;
  }
  .table {
    display: block;
    width: max-content;
  }
  .table thead tr {
    position: absolute;
    top: -9999px;
    left: -9999px;
  }
  .table tr {
    margin-bottom: 1rem;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
  }
  .table td {
    border: none;
    position: relative;
    padding-left: 50% !important;
    text-align: right;
  }
  .table td:before {
    content: attr(data-label);
    position: absolute;
    right: 1.2rem;
    width: 45%;
    font-weight: 700;
    color: #495057;
  }
  .actions-cell {
    display: flex;
    flex-direction: row;
    justify-content: flex-end;
    gap: 0.5rem;
    padding-top: 0.5rem;
  }
}
</style>
