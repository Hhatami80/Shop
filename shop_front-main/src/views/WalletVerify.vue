<template>
  <div class="verify-page">
    <h2>تایید پرداخت کیف پول</h2>

    <p v-if="loading">در حال بررسی وضعیت پرداخت...</p>

    <p v-else-if="success" class="success">
      پرداخت با موفقیت انجام شد. موجودی کیف پول شما به‌روز شد.
      <br />
      هدایت به صفحه کیف پول...
    </p>

    <p v-else class="error">پرداخت ناموفق بود یا توسط کاربر لغو شد.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useWalletStore } from "@/stores/useWalletStore";
import { toast } from "vue3-toastify";

const route = useRoute();
const router = useRouter();
const wallet = useWalletStore();

const loading = ref(true);
const success = ref(false);

onMounted(async () => {
  try {
    const authority = route.query.Authority;
    const payment_id = route.query.payment_id;
    const status = route.query.Status;
    console.log(authority, payment_id, status);
    if (!authority || !status) {
      throw new Error("پارامترهای پرداخت ناقص هستند");
    }

    if (status !== "OK") {
      toast.error("پرداخت توسط کاربر لغو شد");
      success.value = false;
      return;
    }

    const verified = await wallet.verifyWallet({
      payment_id: payment_id,
      authority: authority,
      zarinpal_status: status,
    });

    success.value = verified.success;

    if (verified) {
      if (verified.success) toast.success("پرداخت با موفقیت انجام شد ");
      setTimeout(() => router.push({ name: "Wallet" }), 2500);
    } else {
      toast.error("پرداخت ناموفق بود");
    }
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.verify-page {
  max-width: 600px;
  margin: 80px auto;
  background: #fff;
  padding: 40px;
  border-radius: 20px;
  text-align: center;
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.08);
}

h2 {
  font-size: 1.6rem;
  margin-bottom: 24px;
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
