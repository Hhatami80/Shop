<template>
  <div class="product-slider-container">
    <h2 class="section-title">{{ title }}</h2>

    <Swiper
      v-if="new_products?.length"
      :modules="[Autoplay, Pagination]"
      :slides-per-view="1"
      :space-between="20"
      :breakpoints="{
        480: { slidesPerView: Math.min(new_products.length, 2), spaceBetween: 16 },
        768: { slidesPerView: Math.min(new_products.length, 3), spaceBetween: 18 },
        1024: { slidesPerView: Math.min(new_products.length, 4), spaceBetween: 20 },
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

const openModal = (product) => {
  selectedProduct.value = product
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
  font-size: 26px;
  margin-bottom: 30px;
  color: #222;
  font-weight: 800;
}

.product-swiper {
  padding-bottom: 45px;
}

.swiper-pagination-bullet {
  background: #ccc;
  opacity: 1;
  transition: all 0.3s ease;
}

.swiper-pagination-bullet-active {
  background: #facc15;
  transform: scale(1.3);
}

.loading {
  text-align: center;
  font-size: 18px;
  color: #666;
  padding: 20px 0;
}

@media (max-width: 1024px) {
  .section-title {
    font-size: 22px;
    margin-bottom: 25px;
  }
  .product-slider-container {
    padding: 30px 15px;
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
    padding-bottom: 35px;
  }
  .swiper-pagination-bullet {
    width: 10px;
    height: 10px;
  }
}

@media (max-width: 480px) {
  .section-title {
    font-size: 18px;
    margin-bottom: 15px;
  }
  .product-slider-container {
    padding: 20px 8px;
  }
  .product-swiper {
    padding-bottom: 25px;
  }
  .swiper-pagination-bullet {
    width: 12px;
    height: 12px;
    margin: 0 6px !important;
  }
}
</style>
