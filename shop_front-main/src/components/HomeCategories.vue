<template>
  <div class="categories-section">
    <h2 class="section-title" @click="goToCategory">دسته‌بندی‌ها</h2>

    <div v-if="loading" class="loading">در حال بارگذاری...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else class="categories-swiper">
      <Swiper
        v-if="categories?.length"
        :modules="[Autoplay]"
        :slides-per-view="1"
        :space-between="20"
        :loop="categories.length > 1"
        :autoplay="{ delay: 2500, disableOnInteraction: false }"
        :breakpoints="{
          480: { slidesPerView: Math.min(categories.length, 2), spaceBetween: 30 },
          768: { slidesPerView: Math.min(categories.length, 3), spaceBetween: 50 },
          1024: { slidesPerView: Math.min(categories.length, 4), spaceBetween: 70 },
        }"
        class="my-swiper"
      >
        <SwiperSlide v-for="category in categories" :key="category.id">
          <CategoryCard :category="category" />
        </SwiperSlide>
      </Swiper>

      <p v-else class="loading">هیچ دسته‌بندی‌ای یافت نشد.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Autoplay } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/autoplay'
import router from '@/router'
import { useCategoryStore } from '@/stores/useCategoryStore'
import CategoryCard from '@/components/CategoryCard.vue'

const store = useCategoryStore()
const loading = ref(false)
const error = ref(null)
const categories = computed(() => store.allCategories)

const goToCategory = () => router.push(`/categories/`)

onMounted(async () => {
  try {
    loading.value = true
    await store.getAllCategories()
  } catch (err) {
    error.value = 'خطا در دریافت دسته‌بندی‌ها'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.categories-section {
  position: relative;
  margin: 20px auto;
  padding: 40px 20px;
  text-align: center;
  background: linear-gradient(to bottom, #000 50%, #fff 50%);
}

.section-title {
  font-size: 28px;
  margin-bottom: 25px;
  font-weight: bold;
  color: #fff;
  position: relative;
  z-index: 1;
  cursor: pointer;
  text-align: center;
}

.categories-swiper {
  max-width: 1250px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.loading {
  color: #ddd;
  font-size: 16px;
}

.error {
  color: red;
  font-size: 16px;
}

.my-swiper {
  padding: 20px 0;
}


@media (max-width: 1024px) {
  .categories-section {
    padding: 35px 15px;
  }
  .section-title {
    font-size: 24px;
    margin-bottom: 20px;
  }
  .my-swiper {
    padding: 15px 0;
  }
}


@media (max-width: 768px) {
  .categories-section {
    padding: 30px 10px;
  }
  .section-title {
    font-size: 22px;
    margin-bottom: 18px;
  }
  .my-swiper {
    padding: 10px 0;
  }
}


@media (max-width: 480px) {
  .categories-section {
    padding: 25px 8px;
  }
  .section-title {
    font-size: 20px;
    margin-bottom: 15px;
  }
  .my-swiper {
    padding: 8px 0;
  }
}
</style>
