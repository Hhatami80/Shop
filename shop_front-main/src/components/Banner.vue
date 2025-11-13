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


import img1 from "@/assets/image/download1.jpg";
import img2 from "@/assets/image/download2.jpg";
import img3 from "@/assets/image/download3.jpg";

const banners = [
  {
    image: img1,
    title: "قهوه‌ای با عطر زندگی",
    subtitle: "لحظه‌هات رو با طعم واقعی قهوه تازه شروع کن ☕️",
  },
  {
    image: img2,
    title: "طعمی از آرامش و انرژی",
    subtitle: "قهوه، الهام‌بخش شروعی دوباره در هر روز توست.",
  },
  {
    image: img3,
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
  text-align: left;
  color: #fff;
  z-index: 10;
  position: absolute;
  top: 60%;
  left: 5%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.35);
  padding: 20px 30px;
  border-radius: 12px;
  backdrop-filter: blur(6px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  animation: fadeIn 0.8s ease-in-out;
}

.banner-title {
  font-size: 2rem;
  font-weight: 900;
  margin-bottom: 8px;
  letter-spacing: -0.5px;
}

.banner-subtitle {
  font-size: 1rem;
  opacity: 0.9;
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

@media (max-width: 768px) {
  .category-banner {
    height: 60vh;
  }
  .banner-content {
    left: 50%;
    top: 65%;
    transform: translate(-50%, -50%);
    text-align: center;
    padding: 15px 20px;
  }
  .banner-title {
    font-size: 1.4rem;
  }
  .banner-subtitle {
    font-size: 0.9rem;
  }
}
</style>
