<template>
  <div class="product-slider-container">
    <h2 class="section-title">پرفروش‌ترین‌ها</h2>

    <Swiper
      v-if="products?.length"
      :modules="[Autoplay, Pagination]"
      :slides-per-view="1"
      :space-between="20"
      :loop="products.length > 1"
      :autoplay="{ delay: 5000, disableOnInteraction: false }"
      :pagination="{ clickable: products.length > 1 }"
      :breakpoints="{
        480: { slidesPerView: Math.min(products.length, 2), spaceBetween: 16 },
        768: { slidesPerView: Math.min(products.length, 3), spaceBetween: 20 },
        1024: { slidesPerView: Math.min(products.length, 4), spaceBetween: 24 },
      }"
      class="product-swiper"
    >
      <SwiperSlide v-for="product in products" :key="product.id">
        <BestSellerCard :product="product" @open-modal="openModal" />
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
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Autoplay, Pagination } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/pagination'
import 'swiper/css/autoplay'

import BestSellerCard from './BestSellerCard.vue'
import ProductModal from './ProductModal.vue'
import { useCartStore } from '@/stores/useCartStore'
import { ref } from 'vue'

defineProps({
  products: { type: Array, default: () => [] },
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
  transition: all 0.3s ease;
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

@media (max-width: 1024px) {
  .section-title {
    font-size: 22px;
    margin-bottom: 25px;
  }
  .product-slider-container {
    padding: 30px 15px;
  }
  .product-swiper {
    padding-bottom: 35px;
  }
}

@media (max-width: 768px) {
  .section-title {
    font-size: 20px;
    margin-bottom: 20px;
  }
  .product-slider-container {
    padding: 25px 10px;
  }
  .product-swiper {
    padding-bottom: 30px;
  }
}
@media (max-width: 480px) {
  .section-title {
    font-size: 18px;
    margin-bottom: 15px;
  }
  .product-slider-container {
    padding: 20px 5px;
  }
  .product-swiper {
    padding-bottom: 25px;
  }
}
</style>
