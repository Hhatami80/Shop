<template>
  <div class="verify-page">
    <h2>تایید پرداخت</h2>

    <p v-if="loading">در حال بررسی وضعیت پرداخت...</p>

    <p v-else-if="success" class="success">
      پرداخت با موفقیت انجام شد. <br />
      شما به صفحه‌ی موفقیت هدایت می‌شوید...
    </p>

    <p v-else-if="success == false" class="error">
      ❌ پرداخت ناموفق بود یا توسط کاربر لغو شد.
    </p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useOrderStore } from "@/stores/useOrderStore";
import { toast } from "vue3-toastify";

const router = useRouter();
const route = useRoute();
const order = useOrderStore();

const loading = ref(true);
const success = ref(false);

onMounted(async () => {
  try {
    const authority = route.query.Authority;
    const orderId = route.query.order_id;
    const statusParam = route.query.Status;

    if (!authority || !orderId) {
      toast.error("پارامترهای پرداخت ناقص است");
      return;
    }

    if (statusParam !== "OK") {
      toast.error("پرداخت توسط کاربر لغو شد ");
      success.value = false;
      return;
    }

    const verified = await order.verifyPayment(authority, orderId, statusParam);
    success.value = verified;

    if (verified) {
      toast.success("پرداخت با موفقیت انجام شد ");
      setTimeout(() => router.push({ name: "OrderSuccess" }), 2000);
    }
  } catch (err) {
    console.log(err);
    toast.error("خطا");
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.verify-page {
  max-width: 600px;
  margin: 60px auto;
  background: #fff;
  padding: 40px;
  border-radius: 16px;
  text-align: center;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
}

h2 {
  font-size: 1.5rem;
  margin-bottom: 20px;
  color: #333;
}

.success {
  color: #28a745;
  font-weight: 600;
}

.error {
  color: #dc3545;
  font-weight: 600;
}
</style>
