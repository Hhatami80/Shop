<template>
  <div class="gateway-page">
    <h2>انتخاب درگاه پرداخت</h2>

    <div class="gateways">
      <div
        v-for="gateway in gateways"
        :key="gateway.id"
        class="gateway-card"
        @click="selectGateway(gateway.id)"
      >
        <img :src="gateway.logo" :alt="gateway.name" />
        <p>{{ gateway.label }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import zarinpal from "@/assets/image/zarinpal.jpg";
import idpay from "@/assets/image/idpay.jpg";

const router = useRouter();

const gateways = [
  {
    id: "zarinpal",
    name: "Zarinpal",
    label: "درگاه زرین‌پال",
    logo: zarinpal,
  },
  {
    id: "idpay",
    name: "IDPay",
    label: "درگاه IDPay",
    logo: idpay,
  },
];

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
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
}

.gateways {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
  flex-wrap: wrap;
}

.gateway-card {
  cursor: pointer;
  border: 2px solid #f1c40f;
  border-radius: 12px;
  padding: 20px;
  transition: 0.3s;
  background: #fffef7;
  width: 180px;
}
.gateway-card:hover {
  background: #fff3c4;
  transform: translateY(-5px);
}
.gateway-card img {
  width: 100px;
  margin-bottom: 10px;
}
.gateway-card p {
  font-weight: 600;
  color: #333;
}
</style>
