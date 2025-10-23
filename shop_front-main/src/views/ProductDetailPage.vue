<template>
  <div class="product-detail-page">
    <StickyHeader :visible="true" />

    <div class="product-container">
      <div class="images-section" v-if="productStore.selectedProduct.id">
        <div class="main-image">
          <img :src="selectedImage" :alt="productStore.selectedProduct.title" />
        </div>
        <div class="thumbnail-images">
          <img
            v-for="(img, index) in productImages"
            :key="index"
            :src="img"
            :alt="productStore.selectedProduct.title"
            :class="{ active: selectedImage === img }"
            @click="selectedImage = img"
          />
        </div>
      </div>

      <div class="details-section" v-if="productStore.selectedProduct.id">
        <h1 class="product-title">{{ productStore.selectedProduct.title }}</h1>

        <div class="product-description">{{ productStore.selectedProduct.description }}</div>
        <div class="prices-horizontal">
          <span class="final-price">
            {{ Number(productStore.selectedProduct.discounted_price).toLocaleString() }} تومان
          </span>
          <span v-if="productStore.selectedProduct.price" class="original-price">
            {{ Number(productStore.selectedProduct.price).toLocaleString() }} تومان
          </span>
        </div>

        <div class="actions">
          <button class="add-to-cart-btn" @click="addToCart">افزودن به سبد خرید</button>
        </div>

        <div class="extra-info">
          <p><strong>دسته‌بندی:</strong> {{ categoryTitle }}</p>
          <p>
            <strong>موجودی:</strong>
            {{ productStore.selectedProduct.is_done ? 'موجود' : 'ناموجود' }}
          </p>
        </div>
      </div>
    </div>

    <div v-if="productStore.selectedProduct.id" class="tabs-section">
      <div class="tabs">
        <button :class="{ active: activeTab === 'description' }" @click="activeTab = 'description'">
          توضیحات
        </button>
        <button :class="{ active: activeTab === 'comments' }" @click="activeTab = 'comments'">
          نظرات ({{ productStore.comments.length }})
        </button>
      </div>

      <div class="tab-content">
        <div v-if="activeTab === 'description'">
          <p>{{ productStore.description }}</p>
        </div>
        <div v-if="activeTab === 'comments'">
          <div class="comment-form">
            <textarea
              v-model="productStore.commentForm.text"
              placeholder="نظر خود را وارد کنید..."
            ></textarea>
            <button @click="submitComment">ارسال نظر</button>
          </div>
          <ul class="comments-list">
            <li v-for="comment in productStore.comments" :key="comment.id">
              <p>
                <strong>{{ comment.user_name }}</strong
                >:
              </p>
              <p>{{ comment.text }}</p>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div v-if="relatedProducts.length" class="related-products-section">
      <h2>محصولات مرتبط</h2>
      <swiper
        :modules="[Pagination, Autoplay]"
        :slides-per-view="4"
        :space-between="20"
        :loop="true"
        :pagination="{ clickable: true }"
        :autoplay="{ delay: 3000 }"
      >
        <swiper-slide v-for="item in relatedProducts" :key="item.id">
          <div class="product-card" @click="goToProduct(item.id)">
            <div class="image-wrapper">
              <img :src="item.image" :alt="item.title" />
            </div>
            <h3>{{ item.title }}</h3>
            <p class="price">{{ Number(item.discounted_price).toLocaleString() }} تومان</p>
            <p class="price">
              <del>{{ Number(item.price).toLocaleString() }} تومان</del>
            </p>
          </div>
        </swiper-slide>
      </swiper>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProductStore } from '@/stores/useProductStore'
import { useCategoryStore } from '@/stores/useCategoryStore'
import StickyHeader from '@/components/StickyHeader.vue'
import { useCartStore } from '@/stores/useCartStore'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Autoplay, Pagination } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/pagination'
import 'swiper/css/autoplay'

import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

const cartStore = useCartStore()
const route = useRoute()
const router = useRouter()
const productStore = useProductStore()
const categoryStore = useCategoryStore()

const selectedImage = ref('')
const activeTab = ref('description')

const productImages = computed(() => {
  if (!productStore.selectedProduct.id) return []
  const imgs = productStore.selectedProduct.images?.length
    ? productStore.selectedProduct.images
    : [productStore.selectedProduct.image]
  return imgs || []
})

const categoryTitle = computed(() => {
  return categoryStore.getCategoryById(productStore.selectedProduct.category?.id)?.title || 'نامشخص'
})

const addToCart = async () => {
  const product = productStore.selectedProduct

  if (!product?.id) {
    toast.error('محصولی برای افزودن به سبد وجود ندارد!')
    return
  }

  try {
    await cartStore.addItem(product.id, 1)
  } catch (error) {
    toast.error('خطا در افزودن محصول به سبد خرید!')
  }
}

const relatedProducts = computed(() => {
  return productStore.products
    .filter(
      (p) =>
        p.category?.id === productStore.selectedProduct.category?.id &&
        p.id !== productStore.selectedProduct.id
    )
    .slice(0, 8)
})

const goToProduct = (id) => router.push({ name: 'ProductDetail', params: { id } })

const submitComment = async () => {
  await productStore.submitComment(Number(route.params.id))
  if (productStore.submitSuccess) toast.success('نظر شما با موفقیت ثبت شد!')
  if (productStore.submitError) toast.error(productStore.submitError)
}

const loadProduct = async (id) => {
  await productStore.getProductById(id)
  await productStore.fetchTabsData(id)
  if (productStore.selectedProduct) {
    const imgs = productStore.selectedProduct.images?.length
      ? productStore.selectedProduct.images
      : [productStore.selectedProduct.image]
    selectedImage.value = imgs[0] || ''
  }
}

onMounted(async () => {
  if (!productStore.products.length) await productStore.getAllProducts()
  if (!categoryStore.allCategories.length) await categoryStore.getAllCategories()
  await loadProduct(Number(route.params.id))
})
watch(
  () => route.params.id,
  async (newId) => {
    await loadProduct(Number(newId))
  }
)
</script>

<style scoped>
.product-detail-page {
  font-family: 'Vazirmatn', 'Yekan', sans-serif;
  background: #fcfcfc;
  direction: rtl;
  padding-bottom: 80px;
}

.product-container {
  display: flex;
  gap: 40px;
  max-width: 1200px;
  margin: 60px auto 0 auto;
  flex-wrap: wrap;
}

.images-section {
  flex: 1;
  min-width: 300px;
}

.main-image {
  width: 100%;
  aspect-ratio: 1; 
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  background-color: #f9f9f9; 
}

.main-image img {
  width: 100%;
  height: 100%;
  object-fit: fill;
  transition: transform 0.4s ease;
}

.thumbnail-images {
  display: flex;
  gap: 10px;
  margin-top: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.thumbnail-images img {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  object-fit: cover;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.thumbnail-images img.active {
  border-color: #f9c710;
  transform: scale(1.05);
}

.details-section {
  flex: 1;
  min-width: 300px;
}

.product-title {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #1a1a1a;
}

.product-description {
  margin-bottom: 20px;
  color: #333;
  line-height: 1.6;
}

.prices-horizontal {
  display: flex;
  gap: 15px;
  margin: 20px 0;
  align-items: center;
}

.prices-horizontal .final-price {
  font-size: 22px;
  font-weight: 900;
  color: #f9c710;
}

.prices-horizontal .original-price {
  font-size: 18px;
  color: #888;
  text-decoration: line-through;
}

.actions {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.add-to-cart-btn {
  padding: 12px 25px;
  border-radius: 12px;
  font-weight: bold;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #f9c710;
  color: #222;
}

.add-to-cart-btn:hover {
  background: #e0b60c;
}

.extra-info p {
  margin: 5px 0;
  color: #555;
}

.tabs-section {
  max-width: 1200px;
  margin: 60px auto 0;
}

.tabs {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.tabs button {
  padding: 10px 20px;
  background: #eee;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
}

.tabs button.active {
  background: #f9c710;
  color: #222;
}

.tab-content p,
.tab-content ul {
  background: #fff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}

.comment-form textarea {
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 10px;
  resize: none;
  border: 1px solid #ddd;
}

.comment-form button {
  padding: 10px 20px;
  background: #f9c710;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
}

.related-products-section {
  max-width: 1200px;
  margin: 60px auto 0;
}

.product-card {
  background: #fff;
  border-radius: 20px;
  padding: 20px;
  text-align: center;
  border: 2px solid #f9c710;
  cursor: pointer;
  transition: all 0.3s ease;
}

.product-card:hover {
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.product-card .image-wrapper {
  width: 100%;
  height: 200px;
  overflow: hidden;
  border-radius: 12px;
  margin-bottom: 15px;
}

.product-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-card h3 {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 10px;
  color: #222;
}

.product-card .price {
  font-size: 16px;
  color: #004a64;
  font-weight: bold;
}
</style>
