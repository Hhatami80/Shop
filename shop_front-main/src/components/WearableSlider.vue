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
.static-products > *,
.product-swiper .swiper-slide > * {
  max-width: 372px;
  width: 100%;
  min-height: 460px; /* increased to fit taller 473x710 images */
  display: flex;
  flex-direction: column;
}

.product-slider-container {
  padding: 60px 5%; /* slightly more padding for taller cards */
  background-color: #f8f8f8;
  direction: rtl;
}

.product-swiper {
  padding-bottom: 60px; /* more space for pagination bullets */
}

.product-swiper .swiper-slide {
  display: flex !important;
  justify-content: center !important;
  align-items: flex-start !important; /* allow cards to expand vertically */
}

.product-swiper .swiper-slide > * {
  max-width: 372px;
  width: 100%;
  min-height: 460px; /* matches static-products for consistency */
  display: flex;
  flex-direction: column;
}



.swiper-pagination-bullet {
  background: #ccc;
  opacity: 1;
}

.swiper-pagination-bullet-active {
  background: #2563eb;
  transform: scale(1.2);
  transition: 0.3s;
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
