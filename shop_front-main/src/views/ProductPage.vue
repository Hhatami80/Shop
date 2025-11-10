<template>
  <div class="products-page">
    <StickyHeader :visible="true" />
    <Banner />

    <div class="breadcrumb">
      <router-link to="/">صفحه اصلی</router-link>
      <span> / همه محصولات</span>
    </div>

    <section class="filter-bar">
      <div class="filter-right" :class="{ active: isFilterOpen }" @click="toggleFilterMenu">
        <i class="fas fa-sliders-h"></i>
        <span>مرتب‌سازی</span>
        <div v-if="isFilterOpen" class="filter-dropdown" @click.stop>
          <button @click="sortBy('priceAsc')">ارزان‌ترین</button>
          <button @click="sortBy('priceDesc')">گران‌ترین</button>
          <button @click="sortBy('discount')">بیشترین تخفیف</button>
        </div>
      </div>
    </section>

    <section class="featured-products" v-if="featuredProducts.length">
      <router-link
        v-for="(product, index) in featuredProducts"
        :key="index"
        :to="`/product/${product.id}`"
        class="featured-card"
      >
        <div class="featured-image-wrapper">
          <img :src="product.image" alt="محصول ویژه" class="featured-image" />
          <span v-if="product.discount" class="featured-discount"> {{ product.discount }}% </span>
        </div>
        <div class="featured-info">
          <h3 class="featured-name">{{ product.title }}</h3>
          <p class="featured-price">{{ toPersianNumber(product.price) }} تومان</p>
        </div>
      </router-link>
    </section>

    <section class="product-grid">
      <router-link
        v-for="(product, index) in paginatedProducts"
        :key="index"
        :to="`/product/${product.id}`"
        class="product-card"
      >
        <div class="product-image-wrapper">
          <img :src="product.image" alt="تصویر محصول" class="product-image" />
          <span v-if="product.discount" class="discount-badge"> {{ product.discount }}% </span>
        </div>
        <h4 class="product-name">{{ product.title }}</h4>
        <p class="product-price">{{ toPersianNumber(product.price) }} تومان</p>
      </router-link>
    </section>

    <section class="pagination" v-if="totalPages > 1">
      <button
        v-for="page in totalPages"
        :key="page"
        :class="{ active: currentPage === page }"
        @click="changePage(page)"
      >
        {{ toPersianNumber(page) }}
      </button>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import StickyHeader from '@/components/StickyHeader.vue'
import Banner from '@/components/Banner.vue'
import { useCategoryStore } from '@/stores/useCategoryStore'

const categoryStore = useCategoryStore()

const isFilterOpen = ref(false)
const selectedSort = ref('')
const currentPage = ref(1)
const itemsPerPage = 8

const allProducts = computed(() => categoryStore.allProducts || [])
const featuredProducts = computed(() => allProducts.value.slice(0, 2))
const gridProducts = ref([])

onMounted(async () => {
  await categoryStore.getAllProducts()
  gridProducts.value = allProducts.value.slice(2)
})

function toggleFilterMenu() {
  isFilterOpen.value = !isFilterOpen.value
}

function sortBy(type) {
  selectedSort.value = type
  if (type === 'priceAsc') gridProducts.value.sort((a, b) => a.price - b.price)
  if (type === 'priceDesc') gridProducts.value.sort((a, b) => b.price - a.price)
  if (type === 'discount') gridProducts.value.sort((a, b) => b.discount - a.discount)
  isFilterOpen.value = false
}

const totalPages = computed(() => Math.ceil(gridProducts.value.length / itemsPerPage))

const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return gridProducts.value.slice(start, start + itemsPerPage)
})

function changePage(page) {
  currentPage.value = page
}

function toPersianNumber(number) {
  if (number === null || number === undefined) return ''
  return Number(number).toLocaleString('fa-IR')
}
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

.products-page {
  direction: rtl;
  background: #f9f9f9;
}

.breadcrumb {
  margin: 15px 60px;
  font-size: 14px;
  color: #333;
}

.breadcrumb a {
  color: #333;
  text-decoration: none;
}
.breadcrumb a:hover {
  text-decoration: underline;
}

.filter-bar {
  display: flex;
  justify-content: flex-start;
  margin: 25px 60px 5px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ddd;
  position: relative;
}

.filter-right {
  display: flex;
  align-items: center;
  font-weight: 600;
  font-size: 15px;
  cursor: pointer;
  color: #333;
  gap: 6px;
  position: relative;
  background-color: #fff;
  border: 1px solid #ddd;
  padding: 10px 16px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.filter-right:hover {
  background-color: #f5f5f5;
  border-color: #ccc;
}

.filter-right.active {
  background-color: #ffe082;
  border-color: #ffca28;
  color: #000;
  box-shadow: 0 2px 8px rgba(255, 202, 40, 0.4);
}

.filter-dropdown {
  position: absolute;
  top: 48px;
  right: 0;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  padding: 6px 0;
  display: flex;
  flex-direction: column;
  min-width: 160px;
  z-index: 10;
}

.filter-dropdown button {
  background: none;
  border: none;
  padding: 10px 16px;
  text-align: right;
  font-size: 14px;
  cursor: pointer;
  color: #333;
  transition: all 0.2s ease;
}
.filter-dropdown button:hover {
  background-color: #fff8e1;
  color: #000;
}

.featured-products {
  display: flex;
  justify-content: center;
  gap: 30px;
  flex-wrap: wrap;
  margin-top: 20px;
  margin-bottom: 20px;
}

.featured-card {
  position: relative;
  width: 560px;
  height: 950px;
  overflow: hidden;
  background: #fff;
  text-align: right;
  text-decoration: none !important;
}

.featured-image-wrapper {
  position: relative;
  width: 100%;
  height: 85%;
}

.featured-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.featured-discount {
  position: absolute;
  top: 10px;
  right: 10px;
  color: #ffd700;
  font-weight: bold;
  font-size: 20px;
}

.featured-info {
  padding: 10px;
  height: 30%;
}

.featured-name {
  font-size: 20px;
  color: #000;
  font-weight: 600;
}

.featured-price {
  font-size: 16px;
  color: #000;
  font-weight: bold;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 25px;
  margin: 0px 20px 40px;
}

@media (max-width: 1200px) {
  .product-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 900px) {
  .product-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .product-grid {
    grid-template-columns: 1fr;
  }
}

.product-image-wrapper {
  position: relative;
  width: 100%;
  height: 380px;
  overflow: hidden;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.discount-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  color: #ffd700;
  font-weight: bold;
  font-size: 16px;
}

.product-card {
  text-decoration: none !important;
  background: #fff;
  overflow: hidden;
  text-align: right;
  padding: 10px;
  border: none;
  box-shadow: none;
}

.product-name {
  font-size: 18px;
  font-weight: 600;
  color: #000;
  margin: 10px 0 4px 0;
  padding: 0;
  border: none;
  line-height: 1.4;
}

.product-price {
  color: #000;
  font-weight: bold;
  font-size: 16px;
  margin: 0;
  padding: 0;
  border: none;
  line-height: 1.3;
}

.pagination {
  display: flex;
  justify-content: center;
  margin: 30px 0;
  padding-bottom: 20px;
  gap: 8px;
}

.pagination button {
  padding: 6px 12px;
  border: 1px solid #ccc;
  background: #fff;
  border-radius: 6px;
  cursor: pointer;
}

.pagination button.active {
  background: gold;
  color: #fff;
  border-color: gold;
}
</style>
