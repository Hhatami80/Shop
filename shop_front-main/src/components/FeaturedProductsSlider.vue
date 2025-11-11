<template>
  <div class="product-slider-container">
    <h2 class="section-title">{{ title }}</h2>

   
    <Swiper
      v-if="discounted_product?.length"
      :modules="[Autoplay, Pagination]"
      :slides-per-view="1"
      :space-between="30"
      :breakpoints="{
        640: { slidesPerView: 2 },
        960: { slidesPerView: 3 },
        1280: { slidesPerView: 4 }
      }"
      loop
      :autoplay="{ delay: 4500, disableOnInteraction: false }"
      :pagination="{ clickable: true }"
      class="product-swiper"
    >
      <SwiperSlide v-for="product in discounted_product" :key="product.id">
        <discountedProductCard :product="product" @open-modal="openModal" />
      </SwiperSlide>
    </Swiper>

    <p v-else class="loading">در حال بارگذاری محصولات...</p>

    
    <ProductModal
      v-if="selectedProduct"
      :show="!!selectedProduct"
      :product="selectedProduct"
      @close="selectedProduct = null"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Autoplay, Pagination } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/pagination'
import 'swiper/css/autoplay'

import DiscountedProductCard from '@/components/DiscountedProductCard.vue'
import ProductModal from './ProductModal.vue'

defineProps({
  title: { type: String, default: 'محصولات تخفیف‌خورده' },
  discounted_product: { type: Array, default: () => [] },
})

const selectedProduct = ref(null)
const openModal = (product) => {
  selectedProduct.value = product
}
</script>


<style scoped>
.product-slider-container {
  padding: 40px 20px;
  background: linear-gradient(to bottom, #000 50%, #fff 50%);
  direction: rtl;
  transition: all 0.3s ease;
}

.section-title {
  text-align: center;
  font-size: 24px;
  margin-bottom: 30px;
  color: #fff;
  font-weight: bold;
  position: relative;
  z-index: 1;
}

.product-swiper {
  padding-bottom: 40px;
  position: relative;
  z-index: 1;
}

.loading {
  text-align: center;
  font-size: 18px;
  color: #ddd;
  position: relative;
  z-index: 1;
}

@media (max-width: 1024px) {
  .product-slider-container {
    padding: 30px 15px;
  }
  .section-title {
    font-size: 22px;
    margin-bottom: 25px;
  }
  .product-swiper {
    padding-bottom: 30px;
  }
}

@media (max-width: 768px) {
  .product-slider-container {
    padding: 25px 10px;
  }
  .section-title {
    font-size: 20px;
    margin-bottom: 20px;
  }
  .product-swiper {
    padding-bottom: 25px;
  }
}

@media (max-width: 480px) {
  .product-slider-container {
    padding: 20px 5px;
  }
  .section-title {
    font-size: 18px;
    margin-bottom: 15px;
  }
  .product-swiper {
    padding-bottom: 20px;
  }
}

</style>
