<template>
  <div class="product-slider-container">
    <h2 class="section-title">پوشینه ها</h2>

    <!-- Static Grid برای 1 یا 2 محصول -->

    <!-- Desktop Grid -->
    <div v-if="isDesktop && products.length > 0 && products.length < 4" class="static-grid">
      <WearableCard
        v-for="product in products"
        :key="product.id"
        :product="product"
        @openModal="openModal"
      />
    </div>

    <!-- Swiper -->
    <Swiper
      v-else-if="products.length > 0"
      :modules="[Autoplay, Pagination]"
      :slides-per-view="1"
      :space-between="20"
      :centered-slides="true"
      :loop="products.length > 1"
      :autoplay="{ delay: 4500, disableOnInteraction: false }"
      :pagination="{ clickable: true, dynamicBullets: true }"
      :breakpoints="swiperBreakpoints"
      class="tall-product-swiper"
    >
      <SwiperSlide v-for="product in products" :key="product.id">
        <WearableCard :product="product" @openModal="openModal" />
      </SwiperSlide>
    </Swiper>
    <ProductModal
      v-if="selectedProduct"
      :show="!!selectedProduct"
      :product="selectedProduct"
      @close="selectedProduct = null"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, defineProps } from 'vue'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Autoplay, Pagination } from 'swiper/modules'

import WearableCard from './WearableCard.vue'
import ProductModal from './ProductModal.vue'

const props = defineProps({
  products: { type: Array, default: () => [] },
})

const selectedProduct = ref(null)
const openModal = (product) => (selectedProduct.value = product)

// تشخیص دسکتاپ
const windowWidth = ref(window.innerWidth)
const handleResize = () => (windowWidth.value = window.innerWidth)
onMounted(() => window.addEventListener('resize', handleResize))
onUnmounted(() => window.removeEventListener('resize', handleResize))
const isDesktop = computed(() => windowWidth.value >= 1024)

// ساخت پویا breakpoints با تعداد محصولات
const swiperBreakpoints = computed(() => ({
  320: { slidesPerView: 1, spaceBetween: 15, centeredSlides: true },
  480: { slidesPerView: 1, spaceBetween: 20, centeredSlides: true },
  768: { slidesPerView: 1, spaceBetween: 25, centeredSlides: true },
  1024: {
    slidesPerView: Math.min(props.products.length, 2),
    spaceBetween: 30,
    centeredSlides: false,
  },
  1280: {
    slidesPerView: Math.min(props.products.length, 3),
    spaceBetween: 32,
    centeredSlides: false,
  },
  1440: {
    slidesPerView: Math.min(props.products.length, 4),
    spaceBetween: 40,
    centeredSlides: false,
  },
  1780: {
    slidesPerView: Math.min(props.products.length, 4),
    spaceBetween: 50,
    centeredSlides: false,
  },
}))
</script>

<style scoped>
.product-slider-container {
  padding: 80px 5%;
  background: linear-gradient(135deg, #f8f9fa 0%, #f0f2f5 100%);
  direction: rtl;
  overflow: hidden;
}

.section-title {
  text-align: center;
  font-size: 1.6rem;
  font-weight: 900;
  color: #1a1a1a;
  margin-bottom: 50px;
  position: relative;
}

/* Grid برای محصولات کمتر از 4 روی دسکتاپ */
.static-grid {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 40px;
  flex-wrap: wrap;
  padding: 20px 0;
}

/* Swiper */
.tall-product-swiper {
  padding: 40px 0 80px 0;
  overflow: visible !important;
}
.tall-product-swiper .swiper-slide {
  height: auto !important;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.4s ease;
}
.tall-product-swiper :deep(.swiper-pagination-bullet) {
  width: 12px;
  height: 12px;
  background: #ddd;
  opacity: 0.7;
  transition: all 0.3s ease;
}
.tall-product-swiper :deep(.swiper-pagination-bullet-active) {
  background: #f9c710;
  opacity: 1;
  transform: scale(1.4);
  box-shadow: 0 0 15px rgba(249, 199, 16, 0.6);
}

.loading {
  text-align: center;
  font-size: 1.3rem;
  color: #666;
  padding: 60px 0;
  font-weight: 500;
}

/* ریسپانسیو */
@media (max-width: 1280px) {
  .static-grid {
    gap: 30px;
  }
}

@media (max-width: 1024px) {
  .product-slider-container {
    padding: 60px 4%;
  }
  .section-title {
    font-size: 1.5rem;
    margin-bottom: 40px;
  }
  /* Grid روی موبایل به ستون تبدیل می‌شود */
  .static-grid {
    flex-direction: column;
    align-items: center;
  }
}

@media (max-width: 480px) {
  .product-slider-container {
    padding: 50px 3%;
  }
  .section-title {
    font-size: 1.3rem;
    margin-bottom: 30px;
  }
}
</style>
