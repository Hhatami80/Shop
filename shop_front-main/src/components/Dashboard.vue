<template>
  <div class="dashboard">
    <h1>داشبورد</h1>
    <div class="cards">
      <InfoBox
        label="تعداد سفارشات"
        :value="ordersCount"
        icon-class="fas fa-shopping-cart"
        color="#3498db"
      />
      <InfoBox
        label="موجودی کیف پول"
        :value="walletBalance + ' تومان'"
        icon-class="fas fa-wallet"
        color="#2ecc71"
      />
    </div>
  </div>
</template>

<script>
import InfoBox from './InfoBox.vue'

export default {
  components: { InfoBox },
  data() {
    return {
      ordersCount: 12,
      walletBalance: 500000,
    }
  },
}
</script>

<style>
.cards {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}
</style>
