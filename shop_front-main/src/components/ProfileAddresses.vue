<template>
  <div class="addresses-section">
    <h3>آدرس‌ها</h3>

    <!-- فرم افزودن آدرس -->
    <div class="address-form">
      <div class="form-group">
        <label>استان:</label>
        <select v-model="newAddress.province_id" @change="updateCities">
          <option disabled value="">انتخاب کنید</option>
          <option
            v-for="province in store.provinces"
            :key="province.id"
            :value="province.id"
          >
            {{ province.name }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label>شهر:</label>
        <select v-model="newAddress.city_id" :disabled="!newAddress.province_id">
          <option disabled value="">انتخاب کنید</option>
          <option v-for="city in store.cities" :key="city.id" :value="city.id">
            {{ city.name }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label>محله:</label>
        <input
          v-model="newAddress.neighborhood"
          type="text"
          placeholder="مثلاً نیاوران"
        />
      </div>

      <div class="form-group">
        <label>کوچه:</label>
        <input v-model="newAddress.street" type="text" placeholder="مثلاً کوچه گلستان" />
      </div>

      <div class="form-group">
        <label>پلاک:</label>
        <input v-model="newAddress.plate" type="text" placeholder="مثلاً ۲۳" />
      </div>

      <div class="form-group full">
        <label>آدرس کامل:</label>
        <textarea
          v-model="newAddress.full_address"
          rows="2"
          placeholder="مثلاً تهران، نیاوران، کوچه گلستان، پلاک ۲۳..."
        ></textarea>
      </div>

      <button class="btn gold-btn" @click="addAddress">افزودن آدرس</button>
    </div>

    <!-- جدول آدرس‌ها -->
    <table class="addresses-table" v-if="store.addresses.length">
      <thead>
        <tr>
          <th>استان</th>
          <th>شهر</th>
          <th>محله</th>
          <th>کوچه</th>
          <th>پلاک</th>
          <th>آدرس کامل</th>
          <th>عملیات</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(addr, idx) in store.addresses" :key="idx">
          <td>{{ addr.province.name }}</td>
          <td>{{ addr.city.name }}</td>
          <td>{{ addr.neighborhood }}</td>
          <td>{{ addr.street }}</td>
          <td>{{ addr.plate }}</td>
          <td>{{ addr.full_address }}</td>
          <td>
            <button class="delete-btn" @click="deleteAddress(idx)">🗑</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { reactive, onMounted, watch } from "vue";
import { useUserStore } from "@/stores/useUserStore";
import { toast } from "vue3-toastify";

const store = useUserStore();

const newAddress = reactive({
  province_id: "",
  city_id: "",
  neighborhood: "",
  street: "",
  plate: "",
  full_address: "",
});

onMounted(async () => {
  await store.fetchProvinces();
  await store.fetchAddresses();
});

watch(
  () => newAddress.province_id,
  async (val) => {
    newAddress.city_id = "";
    if (val) await store.fetchCities(val);
  }
);

const addAddress = async () => {
  if (!newAddress.province_id || !newAddress.city_id) {
    return toast.error("لطفاً استان و شهر را انتخاب کنید");
  }

  const addressToAdd = {
    province_id: newAddress.province_id,
    city_id: newAddress.city_id,
    neighborhood: newAddress.neighborhood,
    street: newAddress.street,
    plate: newAddress.plate,
    full_address: newAddress.full_address,
  };

  try {
    await store.addAddress(addressToAdd);

    // پاک‌کردن فرم
    newAddress.province_id = "";
    newAddress.city_id = "";
    newAddress.neighborhood = "";
    newAddress.street = "";
    newAddress.plate = "";
    newAddress.full_address = "";

    toast.success("آدرس با موفقیت افزوده شد ✅");
  } catch (error) {
    console.error(error.response?.data);
    toast.error("خطا در افزودن آدرس");
  }
};

const deleteAddress = async (idx) => {
  try {
    await store.deleteAddress(idx);
  } catch {
    toast.error("خطا در حذف آدرس");
  }
};
</script>

<style scoped>
.addresses-section {
  display: flex;
  flex-direction: column;
  gap: 25px;
  font-family: IRANSans, sans-serif;
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
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid #ddd;
  font-size: 0.9rem;
  height: 42px;
  box-sizing: border-box;
}

textarea {
  resize: none;
}

input:focus,
select:focus,
textarea:focus {
  border-color: #f8b900;
  box-shadow: 0 0 0 3px rgba(249, 199, 16, 0.2);
  outline: none;
}

.btn {
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.gold-btn {
  background: linear-gradient(135deg, #f9c710, #f8b900);
  color: white;
  padding: 10px 0;
  box-shadow: 0 4px 10px rgba(191, 162, 52, 0.4);
}

.gold-btn:hover {
  background: linear-gradient(135deg, #ffd740, #f9c710);
  transform: translateY(-2px);
  box-shadow: 0 6px 14px rgba(191, 162, 52, 0.5);
}

.addresses-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.addresses-table th,
.addresses-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
  font-size: 0.9rem;
}

.addresses-table th {
  background: linear-gradient(135deg, #f9c710, #f8b900);
  color: white;
  border-radius: 6px;
}

.delete-btn {
  background: transparent;
  border: none;
  color: #d33;
  font-size: 18px;
  cursor: pointer;
  transition: 0.3s;
}

.delete-btn:hover {
  transform: scale(1.2);
}
</style>
