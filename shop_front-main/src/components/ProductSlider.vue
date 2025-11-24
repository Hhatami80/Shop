<template>
  <div class="product-slider-container">
    <h2 class="section-title">{{ title }}</h2>

    <div v-if="new_products?.length && new_products.length < 4" class="product-grid">
      <ProductCard
        v-for="product in new_products"
        :key="product.id"
        :product="product"
        @open-modal="openModal"
      />
    </div>

    <Swiper
      v-else-if="new_products?.length"
      :modules="[Autoplay, Pagination]"
      :slides-per-view="1"
      :space-between="20"
      :centered-slides="true"
      :centeredSlidesBounds="true"
      :loop="new_products.length > 1"
      :autoplay="{ delay: 4500, disableOnInteraction: false }"
      :pagination="{ clickable: new_products.length > 1 }"
      :breakpoints="{
        480: { slidesPerView: Math.min(new_products.length, 2), spaceBetween: 16 },
        768: { slidesPerView: Math.min(new_products.length, 3), spaceBetween: 18 },
        1024: { slidesPerView: Math.min(new_products.length, 4), spaceBetween: 20 },
      }"
      class="product-swiper"
    >
      <SwiperSlide v-for="product in new_products" :key="product.id">
        <ProductCard :product="product" @open-modal="openModal" />
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

import ProductModal from './ProductModal.vue'
import ProductCard from './ProductCard.vue'

defineProps({
  title: { type: String, default: 'محصولات' },
  new_products: { type: Array, default: () => [] },
})

const selectedProduct = ref(null)
const openModal = (product) => {
  selectedProduct.value = product
}
</script>

<style scoped>
.product-slider-container {
  padding: 40px 5%;
  background-color: #f8f8f8;
  direction: rtl;
  overflow: hidden;
}

.section-title {
  font-size: 1.6rem;
  text-align: center;
  margin-bottom: 2rem;
  font-weight: 800;
  color: #222;
}

.product-grid {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 2%;
}

.product-grid > * {
  flex: 0 0 calc(25% - 2%);
  max-width: 372px;
  min-width: 220px;
}

.product-swiper {
  padding-bottom: 45px;
}

.product-swiper .swiper-slide {
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
}

.product-swiper .swiper-slide > * {
  max-width: 372px;
  width: 100%;
}

.swiper-pagination-bullet {
  background: #ccc;
  opacity: 1;
}

.swiper-pagination-bullet-active {
  background: #facc15;
  transform: scale(1.3);
  transition: 0.3s;
}

.loading {
  text-align: center;
  color: #666;
  font-size: 1rem;
  padding: 1rem 0;
}

@media (max-width: 1024px) {
  .product-grid > * {
    flex: 0 0 calc(33% - 2%);
  }
}

@media (max-width: 768px) {
  .product-grid > * {
    flex: 0 0 calc(50% - 2%);
  }
}

@media (max-width: 480px) {
  .product-grid > * {
    flex: 0 0 100%;
  }
}
</style>
