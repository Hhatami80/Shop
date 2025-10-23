<template>
  <div class="category-detail-page">
    <Banner />
    <StickyHeader :visible="true" />
    <div class="products-container">
      <h2 class="page-title">دسته‌بندی {{ categoryTitle }}</h2>
      <div v-if="category" class="category-banner">
        <img :src="category.image" :alt="category.title" />
      </div>
      <p v-if="!category" class="no-products">دسته‌ای یافت نشد.</p>

      <div v-if="topProducts.length" class="top-products-grid">
        <div
          v-for="product in topProducts"
          :key="product.id"
          class="top-product-card"
          @click="goToProduct(product.id)"
        >
          <div class="image-wrapper">
            <img :src="product.image" :alt="product.title" />
          </div>
          <h3>{{ product.title }}</h3>
          <p class="old-price">
             {{ Number(product.product?.price || product.price).toLocaleString() }} تومان
          </p>
          <p class="final-price">
            {{ Number(product.final_price).toLocaleString() }} تومان
          </p>
        </div>
      </div>

      <div v-if="otherProducts.length" class="products-grid">
        <div
          v-for="product in otherProducts"
          :key="product.id"
          class="product-card"
          @click="goToProduct(product.id)"
        >
          <div class="image-wrapper"> 
            <img :src="product.image" :alt="product.title" />
          </div>
          <h3>{{ product.title }}</h3>
          <p class="price">
            {{ Number(product.final_price || product.price).toLocaleString() }} تومان
          </p>
        </div>
      </div>
      
      <p v-else-if="category && !filteredProducts.length" class="no-products">
        هنوز محصولی برای این دسته وجود ندارد.
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCategoryStore } from '@/stores/useCategoryStore'
import Banner from '@/components/Banner.vue'
import StickyHeader from '@/components/StickyHeader.vue'

const route = useRoute()
const router = useRouter()
const categoryId = Number(route.params.id)
const categoryStore = useCategoryStore()

const category = computed(() => categoryStore.getCategoryById(categoryId))
const filteredProducts = computed(() => categoryStore.getProductsByCategory(categoryId))
const topProducts = computed(() => filteredProducts.value.slice(0, 2))
const otherProducts = computed(() => filteredProducts.value.slice(2))
const categoryTitle = computed(() => category.value?.title || 'نامشخص')

const goToProduct = (productId) => {
  router.push({ name: 'ProductDetail', params: { id: productId } })
}

onMounted(async () => {
  if (!categoryStore.allCategories.length) await categoryStore.getAllCategories()
  if (!categoryStore.allProducts.length) await categoryStore.getAllProducts()
})
</script>

<style scoped>
.category-detail-page {
  background: #f9f9f9;
  font-family: 'Yekan', sans-serif;
  direction: rtl;
  padding-bottom: 80px;
}

.products-container {
  padding: 50px 20px;
  text-align: center;
}

.page-title {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 50px;
  color: #2c2c2c;
  position: relative;
  display: inline-block;
}

.page-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  right: 0;
  left: 0;
  margin: auto;
  width: 80px;
  height: 4px;
  border-radius: 2px;
  background: linear-gradient(90deg, #f9c710, #e0b60c);
}

.category-banner img {
  max-width: 500px;
  border-radius: 20px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  margin-bottom: 50px;
}


.top-products-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 30px; 
  margin: 60px auto;
  max-width: 1400px; 
  justify-content: center;
  align-items: stretch;
}

.top-product-card {
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  background: #fff;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  transition: all 0.4s ease;
  cursor: pointer;
  animation: fadeUp 0.7s ease forwards;
  padding-bottom: 20px; 
}

.top-product-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.15);
}

.top-product-card .image-wrapper {
  width: 100%;
  height: 500px;
  overflow: hidden;
  background: #fafafa;
}

.top-product-card .image-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease, filter 0.3s ease;
}

.top-product-card:hover .image-wrapper img {
  transform: scale(1.07);
  filter: brightness(1.08);
}

.top-product-card h3 {
  font-size: 24px; 
  font-weight: 800;
  color: #222;
  margin: 25px 0 10px;
}

.top-product-card .old-price {
    font-size: 16px;
    color: #888;
    text-decoration: line-through;
    margin-bottom: 5px;
}

.top-product-card .final-price {
  font-size: 20px;
  color: #dc3545; 
  font-weight: bold;
  margin-bottom: 20px;
}



.products-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr); 
  gap: 70px; 
  max-width: 1400px;
  margin: 50px auto 0 auto;
  justify-content: center;
  justify-items: center;
}

.product-card {
  background: #fff;
  direction: rtl; 
  border-radius: 20px; 
  padding: 25px 20px; 
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


.product-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -150%;
  width: 50%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(249, 199, 16, 0.3), transparent); 
  transform: skewX(-20deg);
  transition: all 0.6s ease-in-out;
  z-index: 1; 
}

.product-card:hover::before {
  left: 150%;
}

.product-card:hover {
  transform: translateY(-10px); 
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2); 
  border-color: #f9c710; 
}

.product-card .image-wrapper {
  width: 100%;
  max-width: 150px; 
  height: 150px;
  margin: 0 auto 45px auto;
  display: flex; 
  justify-content: center; 
  align-items: center
}

.product-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
  padding: 10px; 
  background: #f9f9f9;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border: 3px solid #f9c710;
  transition: transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.product-card:hover img {
  transform: scale(1.05) rotate(2deg); 
  box-shadow: 0 4px 15px rgba(249, 199, 16, 0.6);
}

.product-card h3 {
  font-size: 18px; 
  font-weight: 700;
  color: #1a1a1a;
  margin-top: 5px;
  transition: color 0.3s;
}

.product-card:hover h3 {
  color: #f9c710; 
}

.product-card .price {
  color: #004a64;
  font-weight: bold;
  font-size: 16px;
  margin-top: 8px;
}

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}


@media (max-width: 1300px) {
  .products-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 1024px) {
  .products-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 992px) {
  .top-products-grid {
    grid-template-columns: 1fr; 
  }
  .top-product-card .image-wrapper {
    height: 400px;
  }
}

@media (max-width: 768px) {
  .products-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .products-grid {
    grid-template-columns: 1fr;
  }
}
</style>