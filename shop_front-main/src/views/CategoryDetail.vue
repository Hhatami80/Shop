<template>
  <div class="category-product-page">
    <StickyHeader :visible="true" />
    <Banner />

    <section class="featured-products" v-if="featuredProducts.length">
      <router-link
        v-for="(product, index) in featuredProducts"
        :key="index"
        :to="`/product/${product.id}`"
        class="featured-card"
      >
        <div class="featured-image-wrapper">
          <img :src="product.image" alt="محصول ویژه" class="featured-image" />
          <span v-if="product.discount" class="featured-discount">
            {{ product.discount }}%
          </span>
        </div>
        <div class="featured-info">
          <h3 class="featured-name">{{ product.title }}</h3>
          <p class="featured-price">{{ toPersianNumber(product.price) }} ریال</p>
        </div>
      </router-link>
    </section>

    <section class="filter-bar">
      <div class="filter-right" @click="toggleFilterMenu">
        <i class="fas fa-sliders-h"></i>
        <span>مرتب‌سازی</span>
        <div v-if="isFilterOpen" class="filter-dropdown" @click.stop>
          <button @click="sortBy('priceAsc')">ارزان‌ترین</button>
          <button @click="sortBy('priceDesc')">گران‌ترین</button>
          <button @click="sortBy('discount')">بیشترین تخفیف</button>
        </div>
      </div>
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
          <span v-if="product.discount" class="discount-badge">
            {{ product.discount }}%
          </span>
        </div>
        <h4 class="product-name">{{ product.title }}</h4>
        <p class="product-price">{{ toPersianNumber(product.price) }} ریال</p>
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
import { ref, computed, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import StickyHeader from "@/components/StickyHeader.vue";
import Banner from "@/components/Banner.vue";
import { useCategoryStore } from "@/stores/useCategoryStore";

const categoryStore = useCategoryStore();
const route = useRoute();

const isFilterOpen = ref(false);
const selectedSort = ref("");
const currentPage = ref(1);
const itemsPerPage = 8;

const categoryId = Number(route.params.id);

const allProducts = computed(() => categoryStore.getProductsByCategory(categoryId));

const featuredProducts = computed(() => allProducts.value.slice(0, 2));

const gridProducts = ref([]);

watch(
  allProducts,
  () => {
    gridProducts.value = allProducts.value.slice(2);
    currentPage.value = 1;
  },
  { immediate: true }
);

function toggleFilterMenu() {
  isFilterOpen.value = !isFilterOpen.value;
}
function sortBy(type) {
  selectedSort.value = type;
  if (type === "priceAsc") gridProducts.value.sort((a, b) => a.price - b.price);
  if (type === "priceDesc") gridProducts.value.sort((a, b) => b.price - a.price);
  if (type === "discount") gridProducts.value.sort((a, b) => b.discount - a.discount);
  isFilterOpen.value = false;
}

const totalPages = computed(() => Math.ceil(gridProducts.value.length / itemsPerPage));
const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return gridProducts.value.slice(start, start + itemsPerPage);
});
function changePage(page) {
  currentPage.value = page;
}

function toPersianNumber(number) {
  return number.toLocaleString("fa-IR");
}

onMounted(async () => {
  await categoryStore.getAllCategories();
  await categoryStore.getAllProducts();
});

watch(
  () => route.params.id,
  () => {
    currentPage.value = 1;
  }
);
</script>

<style scoped>
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css");

.category-product-page {
  font-family: "Vazirmatn", sans-serif;
  direction: rtl;
  background: #f9f9f9;
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
  color: #4d6d58;
  gap: 6px;
  position: relative;
}
.filter-right i {
  font-size: 18px;
  color: #4d6d58;
}
.filter-dropdown {
  position: absolute;
  top: 35px;
  right: 0;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  padding: 6px 0;
  display: flex;
  flex-direction: column;
  min-width: 150px;
  z-index: 10;
}
.product-card,
.featured-card {
  text-decoration: none;
  color: inherit;
  display: block;
}

.filter-dropdown button {
  background: none;
  border: none;
  text-align: right;
  padding: 8px 14px;
  font-size: 14px;
  color: #4d6d58;
  cursor: pointer;
  transition: background 0.2s;
}
.filter-dropdown button:hover {
  background: #f2f2f2;
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
  color: #2e5540;
  font-weight: bold;
  font-size: 20px;
}
.featured-info {
  padding: 10px;
  height: 30%;
}
.featured-name {
  font-size: 18px;
  color: #4d6d58;
}
.featured-price {
  font-size: 16px;
  color: #4d6d58;
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

.product-card {
  background: #fff;
  overflow: hidden;
  text-align: right;
  padding-bottom: 10px;
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
  color: #2e5540;
  font-weight: bold;
  font-size: 16px;
}
.product-name {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 2px;
  color: #4d6d58;
}
.product-price {
  color: #4d6d58;
  font-weight: bold;
}

.pagination {
  display: flex;
  justify-content: center;
  margin: 30px 0;
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
  background: #4d6d58;
  color: #fff;
  border-color: #4d6d58;
}
</style>
