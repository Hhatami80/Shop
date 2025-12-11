<template>
  <StickyHeader />
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
      <div class="product-gallery" v-if="product?.image">
        <div class="gallery-grid">
          <img :src="product.image" alt="عکس اصلی" class="main-image" />
          <img
            v-for="(img, index) in product.images || []"
            :key="index"
            :src="img.image"
            :alt="`گالری ${index + 1}`"
            class="extra-image"
          />
        </div>
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
          <button class="size-guide golden-button">راهنمای سایز</button>
        </div>

        <div class="price">
          <template v-if="isPurchasable"> {{ toPersianNumber(product.price) }} تومان </template>

          <template v-else>
            <span>{{ product.price }}</span>
          </template>
        </div>

        <div class="quantity" v-if="product.is_purchasable">
          <span>تعداد</span>
          <div class="controls">
            <button @click="decrease">−</button>
            <span>{{ quantity }}</span>
            <button @click="increase">+</button>
          </div>
        </div>

        <div class="buy-section">
          <button
          v-if="product.is_purchasable"
            class="add-to-cart golden-button"
            @click="addToCart(product.id)"
            :disabled="alreadyInCart"
          >
            <template v-if="!isPurchasable"> {{ product.price }} </template>
            <template v-else>
              {{ alreadyInCart ? 'افزوده شد' : 'افزودن به سبد خرید' }}
            </template>
          </button>
          <p class="stock" v-if="product.stock <= 2">
            تنها {{ toPersianNumber(product.stock) }} عدد در انبار موجود است
          </p>
          <button class="wishlist golden-button">
            <i class="far fa-heart"></i> افزودن به علاقه‌مندی‌ها
          </button>
        </div>

        <div class="tabs">
          <button :class="{ active: activeTab === 'details' }" @click="activeTab = 'details'">
            جزئیات
          </button>
          <button :class="{ active: activeTab === 'comments' }" @click="activeTab = 'comments'">
            نظرات
          </button>
        </div>

        <div v-if="product.properties?.length" class="product-properties-list">
          <h4>ویژگی‌های محصول</h4>
          <ul>
            <li v-for="(prop, index) in product.properties" :key="index">
              <span class="prop-key">{{ prop.key }}:</span>
              <span class="prop-value">{{ prop.value }}</span>
            </li>
          </ul>
        </div>

        <div v-if="activeTab === 'details'" class="details">
          <p>{{ product.description }}</p>
          <!-- <p>شناسه محصول: {{ product.id }}</p> -->
        </div>

        <div v-else class="comments">
          <div v-if="commentStore.loading">در حال بارگذاری نظرات...</div>
          <div v-else>
            <div v-if="commentStore.comments.length === 0">
              هنوز نظری برای این محصول ثبت نشده است.
            </div>
            <ul v-else class="comment-list">
              <li v-for="c in commentStore.comments" :key="c.id" class="comment-item">
                <p class="user">{{ c.user.fullname || c.user.username }}:</p>
                <p class="text">{{ c.text }}</p>
                <p class="date">{{ c.jalali_created_date }}</p>
              </li>
            </ul>
          </div>
          <button class="submit-comment golden-button" @click="openCommentModal">ثبت نظر</button>
        </div>
      </div>
    </div>

    <section class="related-products" v-if="relatedProducts.length">
      <h3>محصولات مشابه</h3>
      <div class="related-grid">
        <router-link
          v-for="item in relatedProducts"
          :key="item.id"
          :to="`/product/${item.id}`"
          class="product-card"
        >
          <img :src="item.image" :alt="item.title" />
          <p class="name">{{ item.title }}</p>
          <p class="price">{{ toPersianNumber(item.price) }} تومان</p>
        </router-link>
      </div>
    </section>

    <div v-if="isCommentModalOpen" class="modal-overlay" @click.self="closeCommentModal">
      <div class="modal">
        <h3>ثبت نظر</h3>
        <div class="modal-form">
          <div class="row">
            <input v-model="commentForm.firstName" type="text" placeholder="نام" />
            <input v-model="commentForm.lastName" type="text" placeholder="نام خانوادگی" />
          </div>
          <div class="row">
            <input v-model="commentForm.email" type="email" placeholder="ایمیل" />
            <input v-model="commentForm.phone" type="text" placeholder="تلفن همراه" />
          </div>
          <input class="title1" v-model="commentForm.title" type="text" placeholder="عنوان" />
          <textarea v-model="commentForm.comment" placeholder="نظر خود را وارد کنید..."></textarea>
        </div>
        <div class="modal-actions">
          <button class="golden-button" @click="submitComment">ثبت</button>
          <button @click="closeCommentModal">انصراف</button>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="loading">در حال بارگذاری محصول...</div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'
import { useProductStore } from '@/stores/useProductStore'
import { useCategoryStore } from '@/stores/useCategoryStore'
import { useCartStore } from '@/stores/useCartStore'
import StickyHeader from '@/components/StickyHeader.vue'
import { useProductCommentStore } from '@/stores/useProductCommentStore'

const route = useRoute()
const productStore = useProductStore()
const categoryStore = useCategoryStore()
const cartStore = useCartStore()
const commentStore = useProductCommentStore()

const selectedSize = ref(null)
const quantity = ref(1)
const activeTab = ref('details')
const isCommentModalOpen = ref(false)

const commentForm = ref({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  title: '',
  comment: '',
})

const productId = computed(() => Number(route.params.id))
const product = computed(() => productStore.selectedProduct)
const categoryTitle = computed(() => {
  const category = categoryStore.allCategories.find((c) => c.id === product.value?.category?.id)
  return category ? category.title : ''
})
const alreadyInCart = computed(() =>
  cartStore.items.some((item) => item.product.id === productId.value)
)
const relatedProducts = computed(() => {
  if (!product.value?.category?.id) return []
  return productStore.products
    .filter((p) => p.category?.id === product.value.category.id && p.id !== product.value.id)
    .slice(0, 4)
})
const isPurchasable = computed(() => product.value?.is_purchasable === true)

function increase() {
  quantity.value++
}
function decrease() {
  if (quantity.value > 1) quantity.value--
}
function toPersianNumber(number) {
  return number?.toLocaleString('fa-IR')
}

async function loadProduct() {
  await productStore.getProductById(productId.value)
}
async function addToCart(productId) {
  if (alreadyInCart.value) {
    toast.error('این محصول قبلاً به سبد خرید اضافه شده است')
    return
  }
  await cartStore.addItem(productId, quantity.value)
}

function openCommentModal() {
  isCommentModalOpen.value = true
}
function closeCommentModal() {
  isCommentModalOpen.value = false
}

async function submitComment() {
  if (
    !commentForm.value.firstName.trim() ||
    !commentForm.value.lastName.trim() ||
    !commentForm.value.email.trim() ||
    !commentForm.value.comment.trim()
  ) {
    toast.error('لطفاً فیلدهای ضروری را پر کنید')
    return
  }

  const commentData = { ...commentForm.value, text: commentForm.value.comment }
  await commentStore.submitComment(productId.value, commentData)
  await commentStore.fetchApprovedComments(productId.value)

  commentForm.value = { firstName: '', lastName: '', email: '', phone: '', title: '', comment: '' }
  closeCommentModal()
}

onMounted(async () => {
  productStore.selectedProduct = null
  await categoryStore.getAllCategories()
  await productStore.getAllProducts()
  await loadProduct()
  if (productId.value) await commentStore.fetchApprovedComments(productId.value)
})

watch(
  () => route.params.id,
  async () => {
    productStore.selectedProduct = null
    quantity.value = 1
    selectedSize.value = null
    await loadProduct()
    if (productId.value) await commentStore.fetchApprovedComments(productId.value)
  }
)

watch(activeTab, async (tab) => {
  if (tab === 'comments' && productId.value)
    await commentStore.fetchApprovedComments(productId.value)
})
</script>

<style scoped>
.product-page {
  background-color: white;
  padding: 20px 40px;
  direction: rtl;
  margin-top: 10px;
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
  flex-direction: row;
  gap: 0px;
  align-items: flex-start;
  justify-content: flex-start;
}

.product-info {
  flex: auto;
  text-align: right;
  margin-right: 50px;
  margin-left: 450px;
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
  background: #f9c710;
  color: #1a1a1a;
  border-color: #f9c710;
}

.size-guide.golden-button {
  background: #f9c710;
  color: #1a1a1a;
  border: none;
  border-radius: 6px;
  padding: 8px 20px;
  cursor: pointer;
}

.price {
  font-size: 20px;
  color: #333;
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
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: flex-start;
}

.add-to-cart.golden-button {
  background: #f9c710;
  color: #1a1a1a;
  border: none;
  border-radius: 6px;
  padding: 14px;
  width: 220px;
  cursor: pointer;
  font-size: 16px;
}

.wishlist.golden-button {
  background: #fff;
  color: #1a1a1a;
  border: 1px solid #f9c710;
  border-radius: 6px;
  padding: 12px;
  width: 220px;
  cursor: pointer;
  font-size: 15px;
  transition: all 0.3s ease;
}

.wishlist.golden-button:hover {
  background: #f9c710;
  color: #000;
}

.product-gallery {
  flex: 1 1 auto;
  margin-right: 60px;
}

.gallery-grid {
  display: grid;
  grid-template-columns: 250px 250px;
  grid-template-rows: 350px 350px;
  gap: 12px;
}

.gallery-grid img:nth-child(1) {
  grid-column: 1 / 2;
  grid-row: 1 / 2;
}

.gallery-grid img:nth-child(2) {
  grid-column: 2 / 3;
  grid-row: 1 / 2;
}

.gallery-grid img:nth-child(3) {
  grid-column: 1 / 2;
  grid-row: 2 / 3;
}

.gallery-grid img:nth-child(4) {
  grid-column: 2 / 3;
  grid-row: 2 / 3;
}

.gallery-grid img {
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
.related-grid {
  display: flex;
  gap: 35px;
  justify-content: center;
  flex-wrap: wrap;
}

.product-card {
  flex: 0 0 300px;
  max-width: 220px;
  border: 1px solid #ddd;
  height: auto;
  border-radius: 10px;
  padding: 20px;
  transition: all 0.3s ease;
  background: #fff;
  text-decoration: none;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
}

.product-card img {
  width: 100%;
  border-radius: 8px;
  height: 60%;
  object-fit: cover;
}

.product-card .name {
  font-size: 18px;
  margin-top: 10px;
  color: #333;
}

.product-card .price {
  color: #333;
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

.modal-actions .golden-button {
  background: #f9c710;
  color: #1a1a1a;
  border: none;
  border-radius: 6px;
  padding: 8px 20px;
  cursor: pointer;
  font-weight: 600;
}

.modal-actions button:last-child {
  background: #ccc;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  border: none;
}

.tabs {
  display: flex;
  gap: 10px;
  margin-top: 25px;
}

.tabs button {
  background: #f9c710;
  color: #1a1a1a;
  border: none;
  border-radius: 6px;
  padding: 8px 20px;
  font-weight: 600;
  cursor: pointer;
}

.tabs button.active {
  background: #e6b800;
}

.details,
.comments {
  margin-top: 20px;
  line-height: 1.9;
  text-align: right;
}

.submit-comment.golden-button {
  background: #f9c710;
  color: #1a1a1a;
  border: none;
  border-radius: 6px;
  padding: 8px 20px;
  cursor: pointer;
  font-weight: 600;
}

.title1 {
  margin-bottom: 10px;
  width: 246px;
}
.product-properties-list {
  margin-top: 20px;
}

.product-properties-list h4 {
  font-weight: bold;
  font-size: 18px;
  margin-bottom: 10px;
  color: #333;
}

.product-properties-list ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.product-properties-list li {
  padding: 6px 0;
  font-size: 15px;
  display: flex;
  gap: 6px;
}

.product-properties-list .prop-key {
  font-weight: 600;
  color: #1a1a1a;
}

.product-properties-list .prop-value {
  color: #555;
}
.comment-list {
  list-style: none;
  padding: 0;
  margin: 0;
  margin-top: 15px;
}

.comment-item {
  border-bottom: 1px solid #eee;
  padding: 12px 0;
}

.comment-item:last-child {
  border-bottom: none;
}

.comment-item .user {
  font-weight: bold;
  color: #1a1a1a;
  margin-bottom: 4px;
}

.comment-item .text {
  font-size: 15px;
  color: #333;
  margin-bottom: 4px;
  line-height: 1.6;
}

.comment-item .date {
  font-size: 13px;
  color: #888;
}

@media (max-width: 900px) {
  .content {
    flex-direction: column-reverse;
  }
  .product-gallery .gallery-images {
    grid-template-columns: 1fr;
  }
  .sizes,
  .tabs {
    justify-content: flex-start;
  }
}
</style>
