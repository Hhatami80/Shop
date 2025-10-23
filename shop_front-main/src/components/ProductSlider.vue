<template>
  <div class="product-slider-container">
    <h2 class="section-title">{{ title }}</h2>

    <Swiper
      v-if="new_products?.length"
      :modules="[Autoplay, Pagination]"
      :slides-per-view="1"
      :space-between="20"
      :breakpoints="{
        640: { slidesPerView: Math.min(new_products.length, 2) },
        960: { slidesPerView: Math.min(new_products.length, 3) },
        1280: { slidesPerView: Math.min(new_products.length, 4) }
      }"
      :loop="new_products.length > 1"
      :autoplay="{ delay: 4500, disableOnInteraction: false }"
      :pagination="{ clickable: new_products.length > 1 }"
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
import { useCartStore } from '@/stores/useCartStore'

defineProps({
  title: { type: String, default: 'محصولات' },
  new_products: { type: Array, default: () => [] },
})

const cartStore = useCartStore()
const selectedProduct = ref(null)
const showModal = ref(false)

const openModal = (product) => {
  selectedProduct.value = product
  showModal.value = true
}
</script>

<style scoped>
.product-slider-container {
  padding: 40px 20px;
  background-color: #f8f8f8;
  direction: rtl;
}

.section-title {
  text-align: center;
  font-size: 24px;
  margin-bottom: 30px;
  color: #222;
  font-weight: bold;
}

.product-swiper {
  padding-bottom: 40px;
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
  font-size: 18px;
  color: #666;
}
</style>
