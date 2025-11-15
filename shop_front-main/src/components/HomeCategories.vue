<template>
  <div class="categories-section">
    <h2 class="section-title" @click="goToCategory">دسته‌بندی‌ها</h2>

    <div v-if="loading" class="loading">در حال بارگذاری...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else class="categories-content">
      <div
        v-if="categories.length > 0 && categories.length < 4"
        class="static-categories"
      >
        <CategoryCard
          v-for="category in categories"
          :key="category.id"
          :category="category"
          class="static-category-card"
        />
      </div>

      <Swiper
        v-else-if="categories?.length"
        :modules="[Autoplay]"
        :slides-per-view="1"
        :space-between="20"
        :loop="categories.length > 1"
        :autoplay="{ delay: 2500, disableOnInteraction: false }"
        :breakpoints="{
          480: { slidesPerView: 2, spaceBetween: 30 },
          768: { slidesPerView: 3, spaceBetween: 50 },
          1024: { slidesPerView: 4, spaceBetween: 70 },
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

.categories-content {
  max-width: 1250px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}


.static-categories {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 60px;
  margin-right: 50px;
  flex-wrap: wrap;
}

.static-category-card {
  width: 250px;
  max-width: 90%;
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
}

@media (max-width: 768px) {
  .static-categories {
    gap: 20px;
  }
  .static-category-card {
    width: 200px;
  }
}

@media (max-width: 480px) {
  .static-categories {
    flex-direction: column;
    gap: 15px;
  }
  .static-category-card {
    width: 80%;
  }
}
</style>
