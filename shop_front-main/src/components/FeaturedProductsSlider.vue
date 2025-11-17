<template>
  <div class="product-slider-container">
    <h2 class="section-title">{{ title }}</h2>

    <div v-if="discounted_product?.length && discounted_product.length < 4" class="product-grid">
      <DiscountedProductCard
        v-for="product in discounted_product"
        :key="product.id"
        :product="product"
        @open-modal="openModal"
      />
    </div>

    <Swiper
      v-else-if="discounted_product?.length"
      :modules="[Autoplay, Pagination]"
      :slides-per-view="1"
      :centered-slides="true"
      :centeredSlidesBounds="true"
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

import DiscountedProductCard from './DiscountedProductCard.vue'
import ProductModal from './ProductModal.vue'

defineProps({
  title: { type: String, default: 'محصولات تخفیف‌خورده' },
  discounted_product: { type: Array, default: () => [] },
})

const selectedProduct = ref(null)
const openModal = (product) => (selectedProduct.value = product)
</script>

<style scoped>
.product-slider-container {
  padding: 50px 5%;
  background: linear-gradient(to bottom, #000 45%, #fff 55%);
  direction: rtl;
  position: relative;
  overflow: hidden;
}

.section-title {
  font-size: 1.5rem;
  text-align: center;
  margin-bottom: 2rem;
  color: #fff;
  font-weight: bold;
}

.product-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2%;
}

.product-grid > * {
  flex: 1 1 calc(25% - 2%);
  max-width: 372px;
  min-width: 220px;
}

.product-swiper {
  padding-bottom: 45px;
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
}
.swiper-slide {
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
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
  color: #ddd;
  font-size: 1rem;
  padding: 1rem 0;
}

@media (max-width: 1024px) {
  .product-grid > * {
    flex: 1 1 calc(33% - 2%);
  }
}

@media (max-width: 768px) {
  .product-grid > * {
    flex: 1 1 calc(50% - 2%);
  }
}

@media (max-width: 480px) {
  .product-grid > * {
    flex: 1 1 100%;
    margin: 0 auto;
  }
  .swiper-slide > * {
    width: 100% !important;
    max-width: 90% !important;
  }
}
</style>
