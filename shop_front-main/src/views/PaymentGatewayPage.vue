<template>
  <div class="gateway-page">
    <h2>انتخاب درگاه پرداخت</h2>
    <div class="gateways">
      <div class="gateway-card" @click="selectGateway('zarinpal')">
        <img src="@/assets/image/logo.png" alt="Zarinpal" />
        <p>درگاه زرین‌پال</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
const router = useRouter();

function selectGateway(gateway) {
  router.push({ name: "payment", query: { method: "online", gateway } });
}
</script>

<style scoped>
.gateway-page {
  max-width: 100vw;
  margin: 60px auto;
  text-align: center;
  background: #fff;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
}

.gateways {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
}

.gateway-card {
  cursor: pointer;
  border: 2px solid #f1c40f;
  border-radius: 12px;
  padding: 20px;
  transition: 0.3s;
  background: #fffef7;
}

.gateway-card:hover {
  background: #fff3c4;
  transform: translateY(-5px);
}

.gateway-card img {
  width: 120px;
  margin-bottom: 10px;
}
</style>
