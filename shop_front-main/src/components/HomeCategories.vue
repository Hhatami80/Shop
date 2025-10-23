<template>
  <div class="categories-section">
    <h2 class="section-title" @click="goToCategory">دسته‌بندی‌ها</h2>

    <div v-if="loading" class="loading">در حال بارگذاری...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="categories-swiper">
      <Swiper
        v-if="categories?.length"
        :modules="[Autoplay]"
        :slides-per-view="4"
        :space-between="100"
        loop
        :autoplay="{ delay: 2000, disableOnInteraction: false }"
        class="my-swiper"
      >
        <SwiperSlide
          v-for="category in categories"
          :key="category.id"
        >
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

const goToCategory = () => {
  router.push(`/categories/`)
}

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
  font-family: 'Yekan', sans-serif;
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

.loading {
  color: #ddd;
  font-size: 16px;
}

.error {
  color: red;
  font-size: 16px;
}
</style>
