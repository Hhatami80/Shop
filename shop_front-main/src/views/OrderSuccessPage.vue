<template>
  <div class="order-success-page">
    <div class="success-card" v-if="order">
      <fa-icon :icon="['fas', 'check-circle']" class="success-icon" />
      <h1>سفارش شما با موفقیت ثبت شد!</h1>

      <p>
        شماره سفارش شما:
        <strong>#{{ order.id }}</strong>
      </p>

      <p v-if="order.total_price">
        جمع کل:
        <strong>{{ formatPrice(order.total_price) }} تومان</strong>
      </p>

      <button class="btn-view-orders" @click="goToOrders">مشاهده سفارش‌ها</button>
      <button class="btn-continue-shopping" @click="goToHome">بازگشت به فروشگاه</button>
    </div>

    <div v-else class="loading-message">در حال بارگذاری جزئیات سفارش...</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useOrderStore } from "@/stores/useOrderStore";

const route = useRoute();
const router = useRouter();
const orderStore = useOrderStore();

const order = ref(null);

const fetchOrder = async () => {
  const orderId = route.query.id || route.params.id;
  if (!orderId) return;

  const data = await orderStore.fetchOrderById(orderId);
  if (data) order.value = data;
};

onMounted(() => fetchOrder());

const formatPrice = (price) => {
  if (!price) return "—";
  const num = Number(price);
  return num.toLocaleString("fa-IR");
};

const goToOrders = () => router.push("/user/orders");
const goToHome = () => router.push("/");
</script>

<style scoped>
.order-success-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
  font-family: "Yekan", sans-serif;
  background: #f9f9f9;
}

.success-card {
  background: #fff;
  border-radius: 20px;
  padding: 40px;
  text-align: center;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  width: 90%;
  animation: fadeIn 0.5s ease-in-out;
}

.success-icon {
  font-size: 60px;
  color: #28a745;
  margin-bottom: 20px;
}

h1 {
  font-size: 22px;
  margin-bottom: 10px;
  color: #222;
}

p {
  font-size: 16px;
  margin-bottom: 10px;
  color: #555;
}

button {
  padding: 12px 20px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  margin: 8px;
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

.loading-message {
  font-size: 1.1rem;
  color: #777;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
