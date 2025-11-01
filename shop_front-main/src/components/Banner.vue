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
        <div class="banner-content">
          <h2 class="banner-title">{{ banner.title }}</h2>
          <p class="banner-subtitle">{{ banner.subtitle }}</p>
        </div>
      </swiper-slide>
    </swiper>
  </div>
</template>

<script setup>
import { Swiper, SwiperSlide } from "swiper/vue";
import { Autoplay, Pagination, EffectFade } from "swiper/modules";
import "swiper/css";
import "swiper/css/effect-fade";
import "swiper/css/pagination";

const banners = [
  {
    image: "/src/assets/image/download1.jpg",
    title: "قهوه‌ای با عطر زندگی",
    subtitle: "لحظه‌هات رو با طعم واقعی قهوه تازه شروع کن ☕️",
  },
  {
    image: "/src/assets/image/download2.jpg",
    title: "طعمی از آرامش و انرژی",
    subtitle: "قهوه، الهام‌بخش شروعی دوباره در هر روز توست.",
  },
  {
    image: "/src/assets/image/download3.jpg",
    title: "از دانه تا فنجان، با عشق",
    subtitle: "با بهترین دانه‌های عربیکا، تجربه‌ای خاص از طعم ناب.",
  },
];
</script>

<style scoped>
.category-banner {
  width: 100%;
  height: 100vh;
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

.banner-content {
  text-align: center;
  color: #fff;
  z-index: 10;
  position: relative;
  background: rgba(0, 0, 0, 0.45);
  padding: 25px 40px;
  border-radius: 16px;
  backdrop-filter: blur(6px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
  animation: fadeIn 1.2s ease forwards;
}

.banner-title {
  font-size: 2.6rem;
  font-weight: 900;
  margin-bottom: 10px;
  letter-spacing: -0.5px;
}

.banner-subtitle {
  font-size: 1.2rem;
  opacity: 0.95;
  font-weight: 400;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

:deep(.swiper-pagination-bullet) {
  background: #f9c710;
  opacity: 0.8;
}

:deep(.swiper-pagination-bullet-active) {
  background: #fff;
}
</style>
