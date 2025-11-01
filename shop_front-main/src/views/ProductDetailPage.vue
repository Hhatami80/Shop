<template>
  <div v-if="product" class="product-page">
    <nav class="breadcrumb">
      <router-link to="/">صفحه اصلی</router-link>
      <span>/</span>
      <router-link :to="`/categories/${product.categoryId}`">
        {{ categoryTitle }}
      </router-link>
      <span>/</span>
      <span>{{ product.title }}</span>
    </nav>

    <div class="content">
      <div class="product-gallery">
        <img
          v-for="(img, i) in product.images"
          :key="i"
          :src="img"
          :alt="product.title"
        />
      </div>

      <div class="product-info">
        <h2 class="title">{{ product.title }}</h2>
        <p class="code">کد محصول: {{ product.id }}</p>

        <div class="color-section" v-if="product.color">
          <span>رنگ:</span>
          <span class="color-name">{{ product.color.name }}</span>
          <div class="color-box" :style="{ backgroundColor: product.color.hex }"></div>
        </div>

        <div class="size-section" v-if="product.sizes?.length">
          <p>سایز</p>
          <div class="sizes">
            <button
              v-for="size in product.sizes"
              :key="size"
              :class="{ active: size === selectedSize }"
              @click="selectedSize = size"
            >
              {{ size }}
            </button>
          </div>
          <button class="size-guide">راهنمای سایز</button>
        </div>

        <div class="price">{{ toPersianNumber(product.price) }} ریال</div>

        <div class="quantity">
          <span>تعداد</span>
          <div class="controls">
            <button @click="decrease">−</button>
            <span>{{ quantity }}</span>
            <button @click="increase">+</button>
          </div>
        </div>

        <div class="buy-section">
          <button class="add-to-cart">افزودن به سبد خرید</button>
          <p class="stock" v-if="product.stock <= 2">
            تنها {{ toPersianNumber(product.stock) }} عدد در انبار موجود است
          </p>
          <button class="wishlist">
            <i class="far fa-heart"></i> افزودن به علاقه‌مندی‌ها
          </button>
        </div>

        <div class="tabs">
          <button
            :class="{ active: activeTab === 'details' }"
            @click="activeTab = 'details'"
          >
            جزئیات
          </button>
          <button
            :class="{ active: activeTab === 'comments' }"
            @click="activeTab = 'comments'"
          >
            نظرات
          </button>
        </div>

        <div v-if="activeTab === 'details'" class="details">
          <p>{{ product.description }}</p>
          <p>شناسه محصول: {{ product.id }}</p>
        </div>

        <div v-else class="comments">
          <p>هنوز نظری برای این محصول ثبت نشده است.</p>
        </div>

        <button class="submit-comment">ثبت نظر</button>
      </div>
    </div>

    <div class="related-products" v-if="relatedProducts.length">
      <h3>محصولات مشابه</h3>
      <div class="related-grid">
        <div v-for="(item, index) in relatedProducts" :key="index" class="product-card">
          <img :src="item.image" :alt="item.title" />
          <p class="name">{{ item.title }}</p>
          <p class="price">{{ toPersianNumber(item.price) }} ریال</p>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="loading">در حال بارگذاری محصول...</div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import { useProductStore } from "@/stores/useProductStore";
import { useCategoryStore } from "@/stores/useCategoryStore";

const route = useRoute();
const productStore = useProductStore();
const categoryStore = useCategoryStore();

const selectedSize = ref(null);
const quantity = ref(1);
const activeTab = ref("details");

const productId = computed(() => Number(route.params.id));

const product = computed(() => productStore.selectedProduct);

const categoryTitle = computed(() => {
  const category = categoryStore.allCategories.find(
    (c) => c.id === product.value?.category?.id
  );
  return category ? category.title : "";
});

const relatedProducts = computed(() => {
  if (!product.value?.category?.id) return [];
  return productStore.products
    .filter(
      (p) => p.category?.id === product.value.category.id && p.id !== product.value.id
    )
    .slice(0, 4);
});

function increase() {
  quantity.value++;
}
function decrease() {
  if (quantity.value > 1) quantity.value--;
}

function toPersianNumber(number) {
  return number?.toLocaleString("fa-IR");
}

async function loadProduct() {
  await productStore.getProductById(productId.value);
}

onMounted(async () => {
  await categoryStore.getAllCategories();
  await productStore.getAllProducts();
  await loadProduct();
});

watch(
  () => route.params.id,
  async () => {
    quantity.value = 1;
    selectedSize.value = null;
    await loadProduct();
  }
);
</script>

<style scoped>
.product-page {
  background-color: white;
  padding: 30px 60px;
  direction: rtl;
  font-family: "Yekan", sans-serif;
  color: #2f3e34;
}

.breadcrumb {
  font-size: 14px;
  margin-bottom: 20px;
  color: #666;
  text-align: right;
}

.breadcrumb a {
  text-decoration: none;
  color: #666;
}

.breadcrumb span {
  margin: 0 6px;
}

.content {
  display: flex;
  justify-content: space-between;
  gap: 40px;
  align-items: flex-start;
}

.product-info {
  flex: 1;
  text-align: right;
}

.title {
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 8px;
}

.code {
  color: #777;
  margin-bottom: 16px;
}

.color-section {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 6px;
  margin-bottom: 15px;
}

.color-box {
  width: 25px;
  height: 25px;
  border: 1px solid #ccc;
}

.size-section {
  margin-bottom: 20px;
}

.sizes {
  display: flex;
  justify-content: flex-start;
  gap: 10px;
  margin-top: 10px;
}

.sizes button {
  padding: 6px 12px;
  border: 1px solid #999;
  background: #fff;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.sizes button.active {
  background: #a7b5ac;
  color: white;
  border-color: #a7b5ac;
}

.size-guide {
  display: block;
  margin: 15px 0 0 0;
  border: 1px solid #999;
  padding: 10px 30px;
  background: #fff;
  border-radius: 6px;
  cursor: pointer;
}

.price {
  font-size: 20px;
  color: #2f3e34;
  font-weight: bold;
  margin: 20px 0;
}

.quantity {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
}

.controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.controls button {
  width: 28px;
  height: 28px;
  border: 1px solid #999;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
}

.buy-section {
  margin-top: 25px;
  text-align: right;
}

.add-to-cart,
.wishlist,
.submit-comment {
  margin-left: 0;
  margin-right: auto;
}

.add-to-cart {
  width: 60%;
  padding: 10px;
  background: white;
  border: 1px solid #444;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

.add-to-cart:hover {
  background: #f9f9f9;
}

.stock {
  color: red;
  font-size: 14px;
  margin-top: 6px;
}

.wishlist {
  background: none;
  border: none;
  color: #2f3e34;
  font-size: 15px;
  cursor: pointer;
  margin-top: 10px;
}

.tabs {
  display: flex;
  justify-content: flex-start;
  gap: 10px;
  margin-top: 25px;
}

.tabs button {
  border: 1px solid #777;
  background: white;
  padding: 8px 30px;
  cursor: pointer;
  border-radius: 4px;
}

.tabs button.active {
  background: #4d6d58;
  color: white;
  border-color: #4d6d58;
}

.details,
.comments {
  margin-top: 20px;
  line-height: 1.9;
  text-align: right;
}

.submit-comment {
  display: block;
  margin: 25px 0 0 0;
  padding: 10px 40px;
  border: 1px solid #444;
  background: white;
  cursor: pointer;
  border-radius: 4px;
}

.product-gallery {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  justify-items: start;
}

.product-gallery img {
  width: 90%;
  height: 100%;
  object-fit: fill;
  border-radius: 6px;
  border: 1px solid #eee;
}

.related-products {
  margin-top: 60px;
  text-align: right;
}

.related-products h3 {
  font-size: 20px;
  margin-bottom: 25px;
  color: #2f3e34;
}

.related-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 25px;
  justify-items: start;
}

.product-card {
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 10px;
  transition: all 0.3s ease;
  background: #fff;
  width: 90%;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
}

.product-card img {
  width: 100%;
  border-radius: 8px;
}

.product-card .name {
  font-size: 14px;
  margin-top: 10px;
  color: #333;
}

.product-card .price {
  color: #4d6d58;
  font-weight: bold;
  margin-top: 5px;
}

@media (max-width: 900px) {
  .content {
    flex-direction: column-reverse;
    align-items: flex-start;
  }

  .product-gallery {
    width: 100%;
    justify-items: start;
  }

  .size-section .sizes,
  .tabs {
    justify-content: flex-start;
  }

  .buy-section {
    text-align: right;
  }
}
</style>
