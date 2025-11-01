<template>
  <div class="order-success-page">
    <div class="success-card">
      <fa-icon :icon="['fas', 'check-circle']" class="success-icon" />
      <h1>سفارش شما با موفقیت ثبت شد!</h1>
      <p>
        شماره سفارش شما: <strong>#{{ order?.id }}</strong>
      </p>
      <p>
        جمع کل: <strong>{{ order?.total_price.toLocaleString() }} تومان</strong>
      </p>

      <button class="btn-view-orders" @click="goToOrders">مشاهده سفارش‌ها</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import orderService from "@/services/orderService";

const route = useRoute();
const router = useRouter();
const order = ref(null);

const fetchOrder = async () => {
  try {
    const response = await orderService.getAllOrders();
    order.value = response.data.find((o) => o.id == route.query.id);
  } catch (err) {
    console.error(err);
  }
};

onMounted(() => {
  fetchOrder();
});

const goToOrders = () => router.push({ name: "user" });
const goToHome = () => router.push({ name: "HomePage" });
</script>

<style scoped>
.order-success-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
  background: #f9f9f9;
  font-family: "Vazirmatn", sans-serif;
}

.success-card {
  background: #fff;
  border-radius: 20px;
  padding: 40px;
  text-align: center;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.success-icon {
  font-size: 50px;
  color: #28a745;
  margin-bottom: 20px;
}

h1 {
  font-size: 24px;
  margin-bottom: 10px;
  color: #222;
}

p {
  font-size: 16px;
  margin-bottom: 15px;
  color: #555;
}

button {
  padding: 12px 20px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  margin: 5px;
  transition: 0.3s;
}

.btn-view-orders {
  background: #ffd700;
  color: #1a1a1a;
}

.btn-view-orders:hover {
  background: #e5c100;
}

.btn-continue-shopping {
  background: #6c757d;
  color: #fff;
}

.btn-continue-shopping:hover {
  background: #5a6268;
}
</style>
