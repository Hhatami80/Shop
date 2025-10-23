<template>
  <div class="category-page">
    <StickyHeader :visible="true" />
    <Banner />
    <div class="categories-container">
      <h2 class="page-title">دسته‌بندی‌ها</h2>
      <div class="categories-grid">
        <div
          class="category-item"
          v-for="cat in categoryStore.allCategories"
          :key="cat.id"
          @click="$router.push(`/categories/${cat.id}`)"
        >
          <div class="category-content">
            <img :src="cat.image" :alt="cat.title" class="category-image" />
            <h3>{{ cat.title }}</h3>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCategoryStore } from '@/stores/useCategoryStore'
import Banner from '@/components/Banner.vue'
import { onMounted } from 'vue'
import StickyHeader from '@/components/StickyHeader.vue'

const categoryStore = useCategoryStore()
onMounted(() => categoryStore.getAllCategories())
</script>

<style scoped>
.category-page {
  direction: rtl;
  background: #fcfcfc;
  min-height: 100vh;
  font-family: 'Vazirmatn', 'Yekan', sans-serif;
}

.categories-container {
  padding: 60px 40px; 
  text-align: center;
}

.page-title {
  font-size: 34px;
  color: #1a1a1a;
  margin-bottom: 50px;
  font-weight: 900;
  position: relative;
  display: inline-block;
}

.page-title::after {
  content: '';
  position: absolute;
  bottom: -15px;
  right: 0;
  left: 0;
  margin: auto;
  width: 100px;
  height: 5px;
  border-radius: 2.5px;
  background: linear-gradient(90deg, #f9c710, #e0b60c);
  box-shadow: 0 2px 8px rgba(249, 199, 16, 0.4);
}

.categories-grid {
  display: grid;
  direction: ltr;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 65px;
  max-width: 1200px;
  margin: 0 auto;
  justify-items: center; 
}

.category-item {
  background: #fff;
  direction: rtl; 
  border-radius: 20px;
  padding: 30px 20px;
  text-align: center;
  color: #111;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  transition: all 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
  cursor: pointer;
  width: 100%;
  position: relative;
  overflow: hidden;
  border: 1px solid #eee;
}

.category-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -150%;
  width: 50%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(249, 199, 16, 0.3), transparent);
  transform: skewX(-20deg);
  transition: all 0.6s ease-in-out;
}

.category-item:hover::before {
  left: 150%;
}

.category-item:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
  border-color: #f9c710;
}

.category-content {
  position: relative;
  z-index: 2; 
}

.category-image {
  width: 120px;
  height: 120px;
  object-fit: cover;
  background: #f9f9f9;
  padding: 15px;
  border-radius: 50%;
  margin-bottom: 20px;
  transition: transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border: 3px solid #f9c710;
}

.category-item:hover .category-image {
  transform: scale(1.05) rotate(2deg);
  box-shadow: 0 4px 15px rgba(249, 199, 16, 0.6);
}

.category-item h3 {
  font-size: 22px;
  font-weight: 800;
  margin-top: 5px;
  color: #1a1a1a;
  transition: color 0.3s;
}

.category-item:hover h3 {
  color: #f9c710;
}

@media (max-width: 600px) {
  .categories-container {
    padding: 40px 15px;
  }
  .page-title {
    font-size: 28px;
    margin-bottom: 40px;
  }
  .categories-grid {
    gap: 30px; 
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    justify-items: center;
  }
}
</style>
