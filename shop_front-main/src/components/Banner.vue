<template>
  <div class="category-banner">
    <swiper
      :modules="[Autoplay, Pagination, EffectFade]"
      :autoplay="{ delay: 4000, disableOnInteraction: false }"
      :pagination="{ clickable: true }"
      effect="fade"
      loop
      class="banner-swiper"
    >
      <swiper-slide
        v-for="(banner, index) in banners"
        :key="index"
        class="banner-slide"
        :style="{ backgroundImage: `url(${banner.image})` }"
      >
        
      </swiper-slide>
    </swiper>
  </div>
</template>

<script setup>
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Autoplay, Pagination, EffectFade } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/effect-fade'
import 'swiper/css/pagination'


const banners = [
  {
    image: '/src/assets/image/download1.jpg',
  },
  {
    image: '/src/assets/image/download2.jpg',
  },
  {
    image: '/src/assets/image/download3.jpg',
  },
]
</script>

<style scoped>
.category-banner {
  width: 100%;
  height: 60vh;
  position: relative;
  overflow: hidden;
}

.banner-swiper,
.banner-slide {
  width: 100%;
  height: 100%;
}

.banner-slide {
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.banner-title {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 10px;
}

.banner-subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
}

:deep(.swiper-pagination-bullet) {
  background: #ffd700;
  opacity: 0.8;
}

:deep(.swiper-pagination-bullet-active) {
  background: #fff;
}
</style>
