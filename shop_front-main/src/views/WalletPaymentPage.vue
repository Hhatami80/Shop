<template>
  <div class="wallet-payment-page">
    <h2>شارژ کیف پول</h2>

    <div class="payment-card">
      <div class="amount-row">
        <span>مبلغ قابل شارژ:</span>
        <strong>{{ amount.toLocaleString() }} تومان</strong>
      </div>

      <div class="gateway-row">
        <span>درگاه پرداخت:</span>
        <strong>زرین‌پال</strong>
      </div>

      <button class="btn-gold" @click="processPayment" :disabled="loading">
        پرداخت آنلاین
      </button>

      <p v-if="loading" class="loading-text">در حال اتصال به درگاه...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useWalletStore } from "@/stores/useWalletStore";
import { toast } from "vue3-toastify";

const walletStore = useWalletStore();
const router = useRouter();
const route = useRoute();
const loading = ref(false);

const amount = computed(() => walletStore.pendingAmount || 0);

onMounted(() => {
  if (route.query.success === "true") {
    toast.success("کیف پول با موفقیت شارژ شد ");
    walletStore.pendingAmount = 0;
    router.replace({ name: "wallet" });
  }
});

const processPayment = async () => {
  if (!amount.value || amount.value <= 0) return toast.error("مبلغ معتبر نیست");

  loading.value = true;
  try {
    const res = await walletStore.createPayment({
      amount: amount.value,
      gateway: "zarinpal",
    });

    if (res.paymentUrl) {
      window.location.href = res.paymentUrl;
    } else {
      toast.error("خطا در دریافت لینک پرداخت");
    }
  } catch (err) {
    console.error(err);
    toast.error("خطا در ایجاد پرداخت");
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
body {
  background-color: white !important;
}
.wallet-payment-page {
  max-width: 480px;
  margin: 60px auto;
  padding: 40px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  text-align: center;
  font-family: "Vazirmatn", sans-serif;
}

h2 {
  font-size: 1.8rem;
  margin-bottom: 30px;
  color: #222;
  border-bottom: 3px solid #f9c710;
  display: inline-block;
  padding-bottom: 6px;
  font-weight: 600;
}

.payment-card {
  background: linear-gradient(145deg, #fdfdfd, #f4f6fb);
  border-radius: 20px;
  padding: 36px 28px;
  box-shadow: 5px 5px 20px rgba(0, 0, 0, 0.08), -5px -5px 15px rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  gap: 24px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.payment-card:hover {
  transform: translateY(-3px);
  box-shadow: 8px 8px 28px rgba(0, 0, 0, 0.12), -8px -8px 20px rgba(255, 255, 255, 0.85);
}

.amount-row,
.gateway-row {
  font-size: 1.15rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 18px;
  border-radius: 14px;
  background: #fafafa;
  box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.03);
  font-weight: 500;
}

.amount-row strong,
.gateway-row strong {
  color: #111;
  font-weight: 700;
}

.btn-gold {
  background: linear-gradient(135deg, #ffe670, #f9c710);
  color: #1a1a1a;
  border: none;
  border-radius: 14px;
  padding: 16px 32px;
  font-weight: 700;
  font-size: 1.15rem;
  cursor: pointer;
  transition: 0.3s;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.btn-gold:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.btn-gold:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-text {
  color: #555;
  font-size: 0.95rem;
  font-weight: 500;
}
</style>
