<template>
  <div class="category-product-page">
    <StickyHeader :visible="true" />
    <Banner :banners="currentCategoryBannerImages" />

    <div class="breadcrumb">
      <router-link to="/">صفحه اصلی</router-link>
      <span v-if="categoryName"> / {{ categoryName }}</span>
    </div>
    <section class="filter-bar">
      <div
        class="filter-right"
        :class="{ active: isFilterOpen }"
        @click="toggleFilterMenu"
      >
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
          <span v-if="product.discount" class="featured-discount">
            {{ product.discount }}%
          </span>
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
          <span v-if="product.discount" class="discount-badge">
            {{ product.discount }}%
          </span>
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
import { ref, computed, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import StickyHeader from "@/components/StickyHeader.vue";
import Banner from "@/components/CategoryBanner.vue";
import { useCategoryStore } from "@/stores/useCategoryStore";

const categoryStore = useCategoryStore();
const route = useRoute();

const isFilterOpen = ref(false);
const selectedSort = ref("");
const currentPage = ref(1);
const itemsPerPage = 8;

const categoryName = ref("");

const currentCategoryId = computed(() => Number(route.params.id));

const allProducts = computed(() =>
  categoryStore.getProductsByCategory(currentCategoryId.value)
);
const featuredProducts = computed(() => allProducts.value.slice(0, 2));
const gridProducts = ref([]);
const currentCategoryBannerImages = computed(() => {
  const cat = categoryStore.getCategoryById(currentCategoryId.value);
  return cat?.banner_images || [];
});
watch(
  allProducts,
  () => {
    gridProducts.value = allProducts.value.slice(2);
    currentPage.value = 1;
  },
  { immediate: true }
);

watch(
  [() => categoryStore.allCategories, currentCategoryId],
  () => {
    const cat = categoryStore.getCategoryById(currentCategoryId.value);
    categoryName.value = cat ? cat.title || cat.name : "";
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
  if (number === null || number === undefined) return "";
  return Number(number).toLocaleString("fa-IR");
}

onMounted(async () => {
  await categoryStore.getAllCategories();
  await categoryStore.getProductsByCategoryApi(currentCategoryId.value);

  
});

watch(
  () => route.params.id,
  async () => {
    currentPage.value = 1;
    await categoryStore.getProductsByCategoryApi(currentCategoryId.value);
  }
);

</script>

<style scoped>
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css");

.category-product-page {
  
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

.filter-right i {
  font-size: 18px;
  color: inherit;
  transition: transform 0.3s ease;
}

.filter-right.active i {
  transform: rotate(90deg);
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
  animation: dropdownFade 0.3s ease forwards;
}

@keyframes dropdownFade {
  from {
    opacity: 0;
    transform: translateY(-5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.filter-dropdown button {
  background: none;
  border: none;
  padding: 10px 16px;
  text-align: right;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #333;
}

.filter-dropdown button:hover {
  background-color: #fff8e1;
  color: #000;
}

.product-card,
.featured-card {
  text-decoration: none;
  color: inherit;
  display: block;
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
  color: #ffd700;
  font-weight: bold;
  font-size: 16px;
}

.product-name {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 2px;
  color: #000;
}

.product-price {
  color: #000;
  font-weight: bold;
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

@media (max-width: 1200px) {
  .breadcrumb {
    margin: 15px 30px;
  }

  .filter-bar {
    margin: 20px 30px 10px;
  }

  .featured-card {
    width: 420px;
    height: 750px;
  }

  .featured-image-wrapper {
    height: 75%;
  }

  .product-image-wrapper {
    height: 320px;
  }
}


@media (max-width: 900px) {
  .breadcrumb {
    margin: 10px 20px;
    font-size: 13px;
  }

  .filter-bar {
    margin: 10px 20px;
    flex-wrap: wrap;
    gap: 10px;
  }

  .filter-right {
    padding: 8px 14px;
    font-size: 14px;
  }

  .featured-products {
    gap: 20px;
    margin-top: 10px;
  }

  .featured-card {
    width: 100%;
    height: auto;
    border-radius: 12px;
  }

  .featured-image-wrapper {
    height: 400px;
  }

  .featured-info {
    height: auto;
  }

  .product-image-wrapper {
    height: 300px;
  }
}


@media (max-width: 600px) {

  .category-product-page {
    padding-bottom: 40px;
  }

  .breadcrumb {
    margin: 10px 16px;
    font-size: 12px;
  }

  .filter-bar {
    margin: 10px 16px;
    flex-wrap: wrap;
    gap: 12px;
  }

  .filter-right {
    width: 100%;
    justify-content: center;
    padding: 10px;
  }

  .filter-dropdown {
    right: 0;
    width: 100%;
  }

  .featured-products {
    margin: 15px 10px;
  }

  .featured-card {
    width: 100%;
    height: auto;
  }

  .featured-image-wrapper {
    height: 300px;
  }

  .featured-name {
    font-size: 18px;
  }

  .featured-price {
    font-size: 15px;
  }

  .product-grid {
    gap: 16px;
    margin: 0 12px 30px;
  }

  .product-image-wrapper {
    height: 250px;
  }

  .product-name {
    font-size: 17px;
  }

  .product-price {
    font-size: 15px;
  }

  .pagination button {
    padding: 5px 10px;
  }
}


@media (max-width: 400px) {
  .featured-image-wrapper {
    height: 240px;
  }
  .product-image-wrapper {
    height: 200px;
  }
  .filter-right {
    font-size: 13px;
    padding: 8px;
  }
}

</style>
