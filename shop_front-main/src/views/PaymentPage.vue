<template>
  <div class="payment-page">
    <h2>پرداخت سفارش</h2>

    <div class="payment-card">
      <p>
        مبلغ کل سفارش:
        <strong>{{ total.toLocaleString() }} تومان</strong>
      </p>
      <p>
        روش پرداخت انتخابی:
        <strong>{{ methodText }}</strong>
      </p>

      <div v-if="method === 'online'" class="online-section">
        <p>
          درگاه انتخابی: <strong>{{ gatewayName }}</strong>
        </p>
        <p v-if="loading">در حال اتصال به درگاه پرداخت...</p>
        <button class="btn gold-btn" @click="processOnline" :disabled="loading">
          پرداخت آنلاین
        </button>
      </div>

      <div v-else class="cod-section">
        <p>سفارش شما در محل پرداخت خواهد شد</p>
        <button class="btn gold-btn" @click="confirmCOD" :disabled="loading">
          تأیید و ثبت سفارش
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useCartStore } from "@/stores/useCartStore";
import { useOrderStore } from "@/stores/useOrderStore";
import { toast } from "vue3-toastify";

const router = useRouter();
const route = useRoute();
const cart = useCartStore();
const orderStore = useOrderStore();

const method = route.query.method || "online";
const gateway = route.query.gateway || "zarinpal";
const loading = ref(false);

const total = computed(() =>
  (cart.items || []).reduce(
    (acc, i) => acc + i.quantity * (i.product.final_price || i.product.price),
    0
  )
);

const methodText = method === "online" ? "پرداخت آنلاین" : "پرداخت در محل";
const gatewayName = computed(() => (gateway === "zarinpal" ? "زرین‌پال" : "نامشخص"));

onMounted(async () => {
  if (!cart.items.length) {
    await cart.fetchCart();
  }
});

const processOnline = async () => {
  if (!cart.items.length) {
    await cart.fetchCart();
  }

  loading.value = true;

  try {
    const payload = {
      payment_method: "online",
      gateway: gateway,
      items: cart.items.map((i) => ({
        product_id: i.product.id,
        quantity: i.quantity,
      })),
    };

    const res = await orderStore.submitOrder(payload);

    if (res?.paymentUrl) {
      window.location.href = res.paymentUrl;
    } else {
      toast.error("خطا در دریافت لینک پرداخت");
    }
  } catch (err) {
    console.error(err);
    toast.error("خطا در ثبت سفارش یا دریافت لینک پرداخت");
  } finally {
    loading.value = false;
  }
};

const confirmCOD = async () => {
  if (!cart.items.length) {
    await cart.fetchCart();
  }

  loading.value = true;

  try {
    const payload = {
      payment_method: "cod",
      items: cart.items.map((i) => ({
        product_id: i.product.id,
        quantity: i.quantity,
      })),
    };

    const res = await orderStore.submitOrder(payload);
    if (res?.orderId) {
      toast.success("سفارش با موفقیت ثبت شد ");
      router.push({ name: "user" });
    }
  } catch (err) {
    console.error(err);
    toast.error("خطا در ثبت سفارش");
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.payment-page {
  
  max-width: 100vw;
  margin: 50px auto;
  background: #fff;
  padding: 30px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.05);
  text-align: center;
}

h2 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 25px;
}

.payment-card {
  background: #fffef7;
  padding: 25px;
  border-radius: 14px;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.08);
}

p {
  margin: 10px 0;
  

  font-size: 1rem;
}

.btn.gold-btn {
  background: linear-gradient(135deg, #f9c710, #f8b900);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 10px 22px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 20px;
  transition: 0.2s;
}

.btn.gold-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
