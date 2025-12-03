<template>
  <div class="product-slider-container">
    <h2 class="section-title">پرفروش‌ترین‌ها</h2>

    <div v-if="products.length > 0 && products.length < 4" class="static-products">
      <BestSellerCard
        v-for="product in products"
        :key="product.id"
        :product="product"
        @openModal="openModal"
      />
    </div>

    <Swiper
      v-else-if="products?.length"
      :modules="[Autoplay, Pagination]"
      :slides-per-view="1"
      :space-between="20"
      :centered-slides="true"
      :centeredSlidesBounds="true"
      :loop="products.length > 1"
      :autoplay="{ delay: 5000, disableOnInteraction: false }"
      :pagination="{ clickable: products.length > 1 }"
      :breakpoints="{
        480: { slidesPerView: Math.min(products.length, 2), spaceBetween: 16 },
        768: { slidesPerView: Math.min(products.length, 3), spaceBetween: 20 },
        1024: { slidesPerView: Math.min(products.length, 4), spaceBetween: 24 }
      }"
      class="product-swiper"
    >
      <SwiperSlide v-for="product in products" :key="product.id">
        <BestSellerCard :product="product" @openModal="openModal" />
      </SwiperSlide>
    </Swiper>

    <p v-else class="loading">در حال بارگذاری پرفروش‌ها...</p>

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

import BestSellerCard from './BestSellerCard.vue'
import ProductModal from './ProductModal.vue'

defineProps({
  products: { type: Array, default: () => [] }
})

const selectedProduct = ref(null)
const openModal = (product) => (selectedProduct.value = product)
</script>


<style scoped>
.product-slider-container {
  padding: 50px 5%;
  background-color: #f8f8f8;
  direction: rtl;
}

.section-title {
  font-size: 1.5rem;
  text-align: center;
  margin-bottom: 2rem;
  font-weight: bold;
  color: #222;
}


.static-products {
  display: flex;
  flex-wrap: wrap;
  justify-content: center !important;
  gap: 2%;
}

.static-products > * {
  flex: 1 1 calc(25% - 2%);
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


.product-swiper :deep(.swiper-pagination) {
  bottom: 15px !important;
  display: flex;
  justify-content: center;
  align-items: center;
  
}

.product-swiper :deep(.swiper-pagination-bullet) {
  width: 12px;
  height: 12px;
  background: #ddd;
  opacity: 0.7;
  transition: all 0.3s ease;
}

.product-swiper :deep(.swiper-pagination-bullet-active) {
  background: #f9c710;
  opacity: 1;
  transform: scale(1.4);
  box-shadow: 0 0 15px rgba(249, 199, 16, 0.6);
}

.loading {
  text-align: center;
  color: #666;
  padding: 1rem 0;
}


@media (max-width: 1024px) {
  .static-products > * {
    flex: 1 1 calc(33% - 2%);
  }
}

@media (max-width: 768px) {
  .static-products > * {
    flex: 1 1 calc(50% - 2%);
  }
}

@media (max-width: 480px) {
  .static-products > * {
    flex: 1 1 100%;
  }
}

</style>
