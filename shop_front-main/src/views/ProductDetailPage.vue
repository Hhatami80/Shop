<template>
  <div v-if="product" class="product-page">
    <nav class="breadcrumb">
      <router-link to="/">صفحه اصلی</router-link>
      <span>/</span>
      <router-link :to="`/categories/${product.category?.id}`">
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
          <button class="add-to-cart" @click="addToCart(product.id)">
            افزودن به سبد خرید
          </button>
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
          <button class="submit-comment" @click="openCommentModal">ثبت نظر</button>
        </div>
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

    <div v-if="isCommentModalOpen" class="modal-overlay" @click.self="closeCommentModal">
      <div class="modal">
        <h3>ثبت نظر</h3>
        <div class="modal-form">
          <div class="row">
            <input v-model="commentForm.firstName" type="text" placeholder="نام" />
            <input
              v-model="commentForm.lastName"
              type="text"
              placeholder="نام خانوادگی"
            />
          </div>

          <div class="row">
            <input v-model="commentForm.email" type="email" placeholder="ایمیل" />
            <input v-model="commentForm.phone" type="text" placeholder="تلفن همراه" />
          </div>

          <input
            class="title1"
            v-model="commentForm.title"
            type="text"
            placeholder="عنوان"
          />

          <textarea
            v-model="commentForm.comment"
            placeholder="نظر خود را وارد کنید..."
          ></textarea>
        </div>
        <div class="modal-actions">
          <button @click="submitComment">ثبت</button>
          <button @click="closeCommentModal">انصراف</button>
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
import { useCartStore } from "@/stores/useCartStore";

const route = useRoute();
const productStore = useProductStore();
const categoryStore = useCategoryStore();
const cartStore = useCartStore();

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

async function addToCart(productId) {
  await cartStore.addItem(productId, quantity.value);
}
const isCommentModalOpen = ref(false);
const commentForm = ref({
  firstName: "",
  lastName: "",
  email: "",
  phone: "",
  title: "",
  comment: "",
});

function openCommentModal() {
  isCommentModalOpen.value = true;
}
function closeCommentModal() {
  isCommentModalOpen.value = false;
}

function submitComment() {
  if (
    !commentForm.value.firstName.trim() ||
    !commentForm.value.lastName.trim() ||
    !commentForm.value.email.trim() ||
    !commentForm.value.comment.trim()
  ) {
    alert("لطفاً فیلدهای ضروری را پر کنید.");
    return;
  }

  console.log("نظر ثبت شد:", commentForm.value);
  alert("نظر شما با موفقیت ثبت شد!");

  commentForm.value = {
    firstName: "",
    lastName: "",
    email: "",
    phone: "",
    title: "",
    comment: "",
  };
  closeCommentModal();
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
  gap: 10px;
  margin-top: 25px;
}
.title1 {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
  outline: none;
  font-size: 12px;
  width: 500px;
  margin-bottom: 10px;
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
}
.product-gallery img {
  width: 100%;
  height: 100%;
  object-fit: cover;
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
}
.product-card {
  border: 1px solid #ddd;
  height: 500px;
  border-radius: 10px;
  padding: 10px;
  transition: all 0.3s ease;
  background: #fff;
}
.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
}
.product-card img {
  width: 100%;
  border-radius: 8px;
  height: 60%;
  object-fit: fill;
}
.product-card .name {
  font-size: 18px;
  margin-top: 10px;
  color: #333;
}
.product-card .price {
  color: #4d6d58;
  font-weight: bold;
  margin-top: 5px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}
.modal {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  width: 500px;
  max-width: 90%;
}
.modal h3 {
  margin-bottom: 15px;
  text-align: center;
}
.modal-form .row {
  display: flex;
  gap: 10px;
  margin-bottom: 12px;
}
.modal-form input,
.modal-form textarea {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
  outline: none;
}
.modal-form textarea {
  width: 100%;
  height: 100px;
  resize: none;
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 10px;
}
.modal-actions button:first-child {
  background: #4d6d58;
  color: white;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  border: none;
}
.modal-actions button:last-child {
  background: #ccc;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  border: none;
}

@media (max-width: 900px) {
  .content {
    flex-direction: column-reverse;
  }
  .product-gallery {
    grid-template-columns: 1fr;
  }
  .sizes,
  .tabs {
    justify-content: flex-start;
  }
}
</style>
