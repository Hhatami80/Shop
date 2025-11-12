<template>
  <div class="product-slider-container">
    <h2 class="section-title">{{ title }}</h2>

    <Swiper
      v-if="discounted_product?.length"
      :modules="[Autoplay, Pagination]"
      :slides-per-view="1"
      :space-between="20"
      :loop="discounted_product.length > 1"
      :autoplay="{ delay: 4500, disableOnInteraction: false }"
      :pagination="{ clickable: discounted_product.length > 1 }"
      :breakpoints="{
        480: { slidesPerView: Math.min(discounted_product.length, 2), spaceBetween: 16 },
        768: { slidesPerView: Math.min(discounted_product.length, 3), spaceBetween: 20 },
        1024: { slidesPerView: Math.min(discounted_product.length, 4), spaceBetween: 24 },
      }"
      class="product-swiper"
    >
      <SwiperSlide v-for="product in discounted_product" :key="product.id">
        <DiscountedProductCard :product="product" @open-modal="openModal" />
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
  padding: 50px 20px;
  background: linear-gradient(to bottom, #000 45%, #fff 55%);
  direction: rtl;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.section-title {
  text-align: center;
  font-size: 26px;
  margin-bottom: 35px;
  color: #fff;
  font-weight: bold;
  position: relative;
  z-index: 1;
}

.product-swiper {
  padding-bottom: 45px;
  position: relative;
  z-index: 1;
}

.swiper-pagination-bullet {
  background: rgba(255, 255, 255, 0.6);
  opacity: 1;
}

.swiper-pagination-bullet-active {
  background: #f9c710;
  transform: scale(1.2);
  transition: 0.3s;
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
    padding: 40px 15px;
    background: linear-gradient(to bottom, #111 50%, #fff 50%);
  }
  .section-title {
    font-size: 22px;
    margin-bottom: 25px;
  }
  .product-swiper {
    padding-bottom: 35px;
  }
}

@media (max-width: 768px) {
  .product-slider-container {
    padding: 30px 10px;
    background: linear-gradient(to bottom, #111 55%, #fff 45%);
  }
  .section-title {
    font-size: 20px;
    margin-bottom: 20px;
  }
  .product-swiper {
    padding-bottom: 30px;
  }
}

@media (max-width: 480px) {
  .product-slider-container {
    padding: 25px 5px;
    background: linear-gradient(to bottom, #000 60%, #fff 40%);
  }
  .section-title {
    font-size: 18px;
    margin-bottom: 15px;
  }
  .product-swiper {
    padding-bottom: 25px;
  }
}
</style>
