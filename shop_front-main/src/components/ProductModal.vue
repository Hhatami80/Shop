<template>
  <transition name="fade">
    <div v-if="show" class="modal-overlay" @click.self="close">
      <div class="modal-content">
        <button class="close-btn" @click="close">✕</button>

        <div class="tabs">
          <button :class="{ active: activeTab === 'details' }" @click="activeTab = 'details'">
            مشخصات
          </button>
          <button :class="{ active: activeTab === 'reviews' }" @click="activeTab = 'reviews'">
            نظرات
          </button>
        </div>

        <div v-if="activeTab === 'details'" class="tab-content">
          <div class="product-card" v-if="product">
            <div class="product-details">
              <h2>{{ product.title }}</h2>
              <div class="meta">
                <p class="sku">شناسه محصول: {{ product.id || 'ندارد' }}</p>
                <hr />
              </div>
              <div class="price">
                <template v-if="product.discounted_price">
                  <span class="old-price">{{ product.price.toLocaleString('fa-IR') }} تومان</span>
                  <span class="new-price"
                    >{{ product.discounted_price.toLocaleString('fa-IR') }} تومان</span
                  >
                </template>
                <template v-else>
                  {{ product.price ? product.price.toLocaleString('fa-IR') : '0' }} تومان
                </template>
              </div>

              <div class="rating-display">
                <span v-for="i in 5" :key="i" :class="{ filled: i <= product.average_rating }"
                  >★</span
                >
              </div>
              <p class="description">{{ product.description || 'توضیحات موجود نیست' }}</p>
              <div class="actions">
                <div class="quantity-control">
                  <button @click="decrease">-</button>
                  <span>{{ count }}</span>
                  <button @click="increase">+</button>
                </div>
                <button class="add-to-cart" @click="addToCart" :disabled="alreadyInCart">
                  {{ alreadyInCart ? 'افزوده شد' : 'افزودن به سبد' }}
                </button>
              </div>

              <div class="share">
                <button><i class="fab fa-google-plus-g"></i></button>
                <button><i class="fab fa-facebook-f"></i></button>
                <button><i class="fab fa-twitter"></i></button>
              </div>
            </div>
            <div class="product-image">
              <img :src="product.image" alt="product" />
            </div>
          </div>
        </div>

        <div v-if="activeTab === 'reviews'" class="tab-content">
          <div class="add-review">
            <h3>ثبت نظر جدید</h3>
            <div class="review-stars">
              <span
                v-for="i in 5"
                :key="i"
                :class="{ filled: i <= hoverRating || i <= userRating }"
                @mouseover="hoverRating = i"
                @mouseleave="hoverRating = 0"
                @click="userRating = i"
                >★</span
              >
            </div>
            <textarea v-model="newComment" placeholder="نظر خود را وارد کنید..."></textarea>
            <button @click="submitComment">ارسال نظر</button>
          </div>

          <div class="reviews-list">
            <transition-group name="fade-comment">
              <div v-for="comment in productStore.comments" :key="comment.id" class="review">
                <div class="review-header">
                  <p class="review-author">
                    <strong>{{ comment.user.username }}</strong>
                  </p>
                  <p class="review-date">{{ comment.jalali_created_date }}</p>
                </div>

                <div class="review-rating">
                  <span
                    v-for="star in 5"
                    :key="star"
                    class="star"
                    :class="{ filled: star <= comment.rating }"
                    >★</span
                  >
                </div>

                <p class="review-text">{{ comment.text }}</p>
              </div>
            </transition-group>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'
import { useCartStore } from '@/stores/useCartStore'
import { useProductCommentStore } from '@/stores/useProductCommentStore'
import { useProductStore } from '@/stores/useProductStore'
const props = defineProps({
  show: Boolean,
  product: Object,
})

onMounted(async () => {
  await productStore.getProductById(props.product?.id)
})
const emit = defineEmits(['close'])

const productStore = useProductStore()
const cartStore = useCartStore()
const commentStore = useProductCommentStore()

const count = ref(1)
const activeTab = ref('details')
const userRating = ref(0)
const hoverRating = ref(0)
const newComment = ref('')



const alreadyInCart = computed(() => {
  if (!props.product?.id) return false
  return cartStore.items.some((item) => item.product.id === props.product.id)
})

watch(
  () => props.product,
  async (newVal) => {
    if (newVal?.id) {
      console.log('Fetching comments for product', newVal.id)
      await commentStore.fetchApprovedComments(newVal.id)
    }
  },
  { immediate: true },
)

const productComments = computed(() => {
  if (!props.product?.id) return []
  return commentStore.comments
})

function close() {
  emit('close')
}

function increase() {
  count.value++
}

function decrease() {
  if (count.value > 1) count.value--
}

async function addToCart() {
  if (!props.product?.id) return

  if (alreadyInCart.value) {
    alert('این محصول قبلاً به سبد خرید اضافه شده است.')
    return
  }

  await cartStore.addItem(props.product.id, count.value)
}

async function submitComment() {
  if (!newComment.value || userRating.value === 0 || !props.product?.id) return
  try {
    await commentStore.submitComment(props.product.id, newComment.value, '')
    newComment.value = ''
    userRating.value = 0
    toast.success('نظر شما با موفقیت ارسال شد و بعد از تایید ادمین نمایش داده می‌شود.')
  } catch (err) {
    console.error(err)
  }
}
</script>

<style scoped>
* {
  box-sizing: border-box !important;
  min-width: 0 !important;
}
html {
  font-size: 14px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 16px;
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  padding: clamp(12px, 2vw, 20px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  position: relative;
  animation: scaleIn 0.3s ease forwards;
}

@keyframes scaleIn {
  0% {
    transform: scale(0.96);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.close-btn {
  position: absolute;
  top: 12px;
  left: 12px;
  background: #f9f9f9;
  border: none;
  font-size: 22px;
  cursor: pointer;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  color: #333;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: 0.18s;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.12);
}
.close-btn:hover {
  background: gold;
  color: #000;
  transform: scale(1.05);
}

.tabs {
  display: flex;
  gap: 0.6rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  justify-content: flex-start;
}
.tabs button {
  padding: 0.55rem 0.9rem;
  border: none;
  border-radius: 8px;
  background: #eee;
  cursor: pointer;
  transition: 0.18s;
  font-weight: 600;
  font-size: 0.95rem;
}
.tabs button.active {
  background: #facc15;
  color: #fff;
}

.tab-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.product-card {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: clamp(12px, 2vw, 30px);
  background: #fff;
  padding: clamp(12px, 2vw, 25px);
  border-radius: 16px;
  direction: rtl;
  align-items: start;
  width: 100%;
}

.product-image img {
  width: 100%;
  height: auto;
  max-height: 320px;
  border-radius: 12px;
  border: 1px solid #ddd;
  object-fit: cover;
}

.product-details h2 {
  font-size: clamp(1rem, 2.1vw, 1.3rem);
  margin: 0 0 0.4rem 0;
}

.meta {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-top: 0.4rem;
}
.meta hr {
  flex-grow: 1;
  border: 0;
  border-top: 1px solid #ddd;
  margin-top: 4px;
}

.price {
  font-size: 1.05rem;
  color: #000;
  font-weight: 700;
  margin: 0.9rem 0;
}

.rating-display span {
  color: #facc15;
  font-size: 1.05rem;
  margin-right: 6px;
}

.actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin: 0.9rem 0;
  flex-wrap: wrap;
}

.quantity-control {
  display: flex;
  align-items: center;
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
  background: rgb(231, 228, 228);
}
.quantity-control button {
  background: rgb(231, 228, 228);
  color: #000;
  border: none;
  width: 40px;
  height: 36px;
  cursor: pointer;
  font-size: 18px;
  font-weight: bold;
  padding: 0;
}
.quantity-control span {
  min-width: 42px;
  text-align: center;
  font-weight: bold;
  font-size: 1rem;
  background: rgb(231, 228, 228);
}

.add-to-cart {
  background: #facc15;
  border: none;
  padding: 0.6rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: 0.18s;
  width: 100%;
  max-width: 220px;
  color: #000;
}
.add-to-cart:hover {
  background: #eab308;
}

.share {
  margin-top: 0.8rem;
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
}
.share button {
  width: 40px;
  height: 36px;
  border: none;
  cursor: pointer;
  font-size: 16px;
  transition: 0.18s;
  border-radius: 6px;
  color: #facc15;
  background: #000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.add-review {
  border: 1px solid #eee;
  padding: clamp(10px, 1.6vw, 18px);
  border-radius: 12px;
  background: #fafafa;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.review-stars span {
  font-size: 1.45rem;
  color: #ddd;
  cursor: pointer;
  transition: 0.18s;
}
.review-stars span.filled {
  color: #facc15;
}

.add-review textarea {
  width: 100%;
  height: 90px;
  padding: 10px;
  border-radius: 10px;
  border: 1px solid #ccc;
  resize: none;
  font-size: 0.95rem;
}

.add-review button {
  align-self: flex-start;
  padding: 0.45rem 1rem;
  border: none;
  background: #facc15;
  color: #000;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: 0.18s;
}
.add-review button:hover {
  background: #eab308;
}

.reviews-list {
  max-height: 45vh;
  overflow-y: auto;
  padding-right: 6px;
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

.reviews-list::-webkit-scrollbar {
  width: 7px;
}
.reviews-list::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 6px;
}

.review {
  background: #fff;
  border: 1px solid #eee;
  padding: clamp(10px, 1.6vw, 16px);
  border-radius: 12px;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.04);
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  width: 100%;
  max-width: 100%;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.6rem;
  font-size: 0.92rem;
}

.review-author {
  color: #222;
  font-weight: 700;
  margin: 0;
  font-size: 0.95rem;
}

.review-date {
  color: #888;
  font-size: 0.78rem;
  margin: 0;
}

.review-rating .star {
  font-size: 1.05rem;
  color: #ddd;
  margin-right: 6px;
}
.review-rating .star.filled {
  color: #facc15;
}

.review-text {
  color: #444;
  font-size: 0.95rem;
  line-height: 1.65;
  text-align: justify;
  word-break: break-word;
  overflow-wrap: break-word;
}

.review-actions {
  display: flex;
  gap: 0.6rem;
  margin-top: 0.25rem;
  flex-wrap: wrap;
}
.review-actions button {
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 0.95rem;
  color: #666;
  padding: 6px 8px;
  border-radius: 6px;
}
.review-actions button:hover {
  color: #000;
  background: rgba(0, 0, 0, 0.03);
}

.reply-box {
  margin-top: 0.6rem;
  border-right: 3px solid gold;
  padding-right: 0.6rem;
}
.reply-box textarea {
  width: 100%;
  height: 70px;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 8px;
  font-size: 0.92rem;
}
.reply-box button {
  margin-top: 8px;
  background: #facc15;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
}
.replies {
  border-right: 3px solid #eee;
  margin-top: 0.6rem;
  padding-right: 0.8rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.reply {
  background: #f9f9f9;
  padding: 10px;
  border-radius: 10px;
}

.reply-author {
  font-weight: 700;
  font-size: 0.92rem;
}
.reply-text {
  font-size: 0.9rem;
  color: #555;
  line-height: 1.5;
  word-break: break-word;
}

.fade-comment-enter-active,
.fade-comment-leave-active {
  transition: all 0.22s ease;
}
.fade-comment-enter-from {
  opacity: 0;
  transform: translateY(8px);
}
.fade-comment-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

@media (max-width: 1100px) {
  .product-card {
    grid-template-columns: 1fr !important;
  }
  .product-image img {
    max-height: 260px;
  }
}

@media (max-width: 720px) {
  .reviews-list {
    max-height: 38vh;
  }
  .modal-content {
    padding: clamp(10px, 3vw, 14px);
  }
}

.old-price {
  text-decoration: line-through;
  color: #888;
  margin-left: 8px;
}
.new-price {
  color: #e11d48;
}
</style>
