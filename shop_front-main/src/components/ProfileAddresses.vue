<template>
  <div class="addresses-section">
    <h3>مدیریت آدرس‌ها</h3>

  
    <div class="address-form">
      <div class="form-group">
        <label>استان:</label>
        <select v-model="form.province_id" @change="updateCities">
          <option disabled value="">انتخاب کنید</option>
          <option v-for="p in store.provinces" :key="p.id" :value="p.id">{{ p.name }}</option>
        </select>
      </div>

      <div class="form-group">
        <label>شهر:</label>
        <select v-model="form.city_id" :disabled="!form.province_id">
          <option disabled value="">انتخاب کنید</option>
          <option v-for="c in store.cities" :key="c.id" :value="c.id">{{ c.name }}</option>
        </select>
      </div>

      <div class="form-group">
        <label>محله:</label>
        <input v-model="form.neighborhood" type="text" placeholder="مثلاً نیاوران" />
      </div>

      <div class="form-group">
        <label>کوچه:</label>
        <input v-model="form.street" type="text" placeholder="مثلاً کوچه گلستان" />
      </div>

      <div class="form-group">
        <label>پلاک:</label>
        <input v-model="form.plate" type="text" placeholder="مثلاً ۱۲۳" />
      </div>

      <div class="form-group">
        <label>کد پستی:</label>
        <input v-model="form.postal_code" type="text" placeholder="مثلاً 1234567890" />
      </div>

      <div class="form-group full">
        <label>آدرس کامل:</label>
        <textarea v-model="form.full_address" placeholder="مثلاً تهران، نیاوران، کوچه گلستان، پلاک ۱۲۳"></textarea>
      </div>

      <button class="btn gold-btn" @click="saveAddress">
        {{ editMode ? "ویرایش آدرس" : "افزودن آدرس" }}
      </button>
    </div>

    
    <table class="addresses-table" v-if="store.addresses.length">
  <thead>
    <tr>
      <th>استان</th>
      <th>شهر</th>
      <th>محله</th>
      <th>کوچه</th>
      <th>پلاک</th>
      <th>کد پستی</th>
      <th>آدرس کامل</th>
      <th>عملیات</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="(addr, idx) in store.addresses" :key="addr.id">
      <td>{{ addr.province.name }}</td>
      <td>{{ addr.city.name }}</td>
      <td>{{ addr.neighborhood }}</td>
      <td>{{ addr.street }}</td>
      <td>{{ addr.plate }}</td>
      <td>{{ addr.postal_code }}</td>
      <td>{{ addr.full_address }}</td>
      <td>
        <div class="action-buttons">
          <button class="btn edit-btn" @click="editAddress(addr)"> ویرایش</button>
          <button class="btn delete-btn" @click="deleteAddress(addr.id, idx)"> حذف</button>
        </div>
      </td>
    </tr>
  </tbody>
</table>

  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from "vue";
import { useUserStore } from "@/stores/useUserStore";
import { toast } from "vue3-toastify";

const store = useUserStore();

const editMode = ref(false);
const editingId = ref(null);

const form = reactive({
  province_id: "",
  city_id: "",
  neighborhood: "",
  street: "",
  plate: "",
  postal_code: "",
  full_address: "",
});

const resetForm = () => {
  Object.assign(form, {
    province_id: "",
    city_id: "",
    neighborhood: "",
    street: "",
    plate: "",
    postal_code: "",
    full_address: "",
  });
  editMode.value = false;
  editingId.value = null;
};

const validateForm = () => {
  if (
    !form.province_id ||
    !form.city_id ||
    !form.neighborhood ||
    !form.street ||
    !form.plate ||
    !form.postal_code ||
    !form.full_address
  ) {
    toast.error("لطفاً همه فیلدها را پر کنید");
    return false;
  }
  if (!/^\d+$/.test(form.plate)) {
    toast.error("پلاک باید فقط عدد باشد");
    return false;
  }
  if (!/^\d{10}$/.test(form.postal_code)) {
    toast.error("کد پستی باید ۱۰ رقم باشد");
    return false;
  }
  return true;
};

const saveAddress = async () => {
  if (!validateForm()) return;

  try {
    if (editMode.value) {
      await store.updateAddress(editingId.value, { ...form });

    } else {
      await store.addAddress({ ...form });
      toast.success("آدرس جدید افزوده شد");
    }
    resetForm();
    await store.fetchAddresses();
  } catch (err) {
    toast.error("خطا در ذخیره آدرس");
  }
};

const editAddress = (addr) => {
  editMode.value = true;
  editingId.value = addr.id;
  Object.assign(form, {
    province_id: addr.province.id,
    city_id: addr.city.id,
    neighborhood: addr.neighborhood,
    street: addr.street,
    plate: addr.plate,
    postal_code: addr.postal_code,
    full_address: addr.full_address,
  });
};

const deleteAddress = async (id, idx) => {
  try {
    await store.deleteAddress(idx);
    toast.success("آدرس حذف شد");
  } catch {
    toast.error("خطا در حذف آدرس");
  }
};

const updateCities = async () => {
  if (form.province_id) {
    await store.fetchCities(form.province_id);
  }
};

onMounted(async () => {
  await store.fetchProvinces();
  await store.fetchAddresses();
});
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Vazirmatn&display=swap");

.addresses-section {
  font-family: "Vazirmatn", sans-serif;
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.address-form {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 15px 20px;
  background: #fafafa;
  padding: 25px;
  border-radius: 16px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full {
  grid-column: 1 / -1;
}

label {
  font-weight: 600;
  margin-bottom: 6px;
  color: #333;
  font-size: 0.9rem;
}

input,
select,
textarea {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 10px;
  font-size: 0.9rem;
}

.btn {
  padding: 8px 16px; 
  border: none;
  border-radius: 10px;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
  grid-column: auto;
  justify-self: start; 
}


.gold-btn {
  background: #f9c710;
  color: white;
  
}


.gold-btn:hover {
  background: #ffd740;
}


.addresses-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 25px;
  background: #fff;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 3px 15px rgba(0, 0, 0, 0.08);
}

.addresses-table thead {
  background: #f9c710;
  color: #fff;
}

.addresses-table th {
  padding: 14px 10px;
  text-align: center;
  font-weight: 600;
  font-size: 0.95rem;
  border-bottom: 2px solid #f1f1f1;
}

.addresses-table td {
  padding: 12px 10px;
  text-align: center;
  font-size: 0.9rem;
  color: #444;
  border-bottom: 1px solid #eee;
  background: #fff;
  transition: background 0.25s;
}

.addresses-table tbody tr:hover td {
  background: #fff8e1;
}

.addresses-table tbody tr:last-child td {
  border-bottom: none;
}


.action-buttons {
  display: flex;
  justify-content: center;
  gap: 8px;
}

.action-buttons .btn {
  border: none;
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
}

.action-buttons .edit-btn {
  background: #f9c710;
  color: white;
}

.action-buttons .edit-btn:hover {
  background: #ffd740;
}

.action-buttons .delete-btn {
  background: #e53935;
  color: white;
}

.action-buttons .delete-btn:hover {
  background: #c62828;
}
</style>

