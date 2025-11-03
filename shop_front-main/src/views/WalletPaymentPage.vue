<template>
  <div class="wallet-payment-page">
    <h2>شارژ کیف پول</h2>

    <div class="payment-card">
      <div class="payment-row">
        <div class="amount-row">
          <span>مبلغ قابل شارژ:</span>
          <strong>{{ amount.toLocaleString() }} تومان</strong>
        </div>

        <div class="gateway-selection">
          <span>انتخاب درگاه:</span>
          <div class="gateway-cards">
            <label
              v-for="gateway in gateways"
              :key="gateway.id"
              class="gateway-card"
              :class="{ selected: selectedGateway === gateway.id }"
            >
              <input type="radio" v-model="selectedGateway" :value="gateway.id" />
              <img :src="gateway.icon" :alt="gateway.name" />
              <span>{{ gateway.name }}</span>
            </label>
          </div>
        </div>
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

import zarinpalIcon from "@/assets/image/zarinpal.jpg";
import idpayIcon from "@/assets/image/idpay.jpg";
import payirIcon from "@/assets/image/PAYEER.png";

const walletStore = useWalletStore();
const router = useRouter();
const route = useRoute();
const loading = ref(false);

const amount = computed(() => walletStore.pendingAmount || 0);

const gateways = ref([
  { id: "zarinpal", name: "زرین‌پال", icon: zarinpalIcon },
  { id: "idpay", name: "آیدی‌پی", icon: idpayIcon },
  { id: "payir", name: "پی‌یر", icon: payirIcon },
]);

const selectedGateway = ref(gateways.value[0].id);

onMounted(() => {
  if (route.query.success === "true") {
    toast.success("کیف پول با موفقیت شارژ شد");
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
      gateway: selectedGateway.value,
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
.wallet-payment-page {
  max-width: 520px;
  margin: 60px auto;
  padding: 40px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  font-family: "Yekan", sans-serif;
  direction: rtl;
  text-align: right;
}

h2 {
  font-size: 1.8rem;
  margin-bottom: 30px;
  color: #222;
  border-bottom: 3px solid #f9c710;
  display: inline-block;
  padding-bottom: 6px;
  font-weight: 600;
  text-align: center;
}

.payment-card {
  background: linear-gradient(145deg, #fdfdfd, #f4f6fb);
  border-radius: 20px;
  padding: 36px 28px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.payment-row {
  display: flex;
  justify-content: flex-start;
  gap: 24px;
  flex-wrap: wrap;
  align-items: center;
}

.amount-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.15rem;
  padding: 14px 0px;
  border-radius: 14px;
  background: #fafafa;
  box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.03);
  font-weight: 500;
  flex: 1 1 200px;
  min-width: 180px;
}

.amount-row strong {
  color: #111;
  font-weight: 700;
}

.gateway-selection {
  flex: 2 1 280px;
}

.gateway-selection span {
  font-weight: 500;
  display: block;
  margin-bottom: 8px;
}

.gateway-cards {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: flex-start;
}

.gateway-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px 14px;
  border: 2px solid #ddd;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100px;
  text-align: center;
}

.gateway-card img {
  width: 50px;
  height: 50px;
  object-fit: contain;
  margin-bottom: 6px;
}

.gateway-card.selected {
  border-color: #f9c710;
  background: #fffde7;
}

.gateway-card input[type="radio"] {
  display: none;
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
  align-self: center;
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
  text-align: center;
}
</style>
