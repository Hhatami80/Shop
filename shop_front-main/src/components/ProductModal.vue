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
            <div v-if="productComments.length">
              <div v-for="(comment, index) in productComments" :key="index" class="review">
                <!-- <p class="review-author">{{ comment.author_name }}</p> -->
                <!-- <div class="review-rating">
                  <span v-for="i in 5" :key="i" :class="{ filled: i <= comment.rating }">★</span>
                </div> -->
                <p class="review-text">{{ comment.text }}</p>
                <hr />
              </div>
            </div>
            <div v-else>
              <p>هیچ نظری ثبت نشده است.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useCartStore } from '@/stores/useCartStore'
import { useProductCommentStore } from '@/stores/useProductCommentStore'

const props = defineProps({
  show: Boolean,
  product: Object,
})
const emit = defineEmits(['close'])

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
    count.value = 1
    if (newVal?.id) {
      await commentStore.fetchApprovedComments(newVal.id)
    }
  },
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
    await commentStore.submitComment(props.product.id, newComment.value, userRating.value)
    newComment.value = ''
    userRating.value = 0
    alert('نظر شما با موفقیت ارسال شد و بعد از تایید ادمین نمایش داده می‌شود.')
  } catch (err) {
    console.error(err)
  }
}
</script>

<style scoped>
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
}

.modal-content {
  background: white;
  border-radius: 16px;
  max-width: 900px;
  width: 90%;
  overflow-y: auto;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  position: relative;
  animation: scaleIn 0.3s ease forwards;
}

@keyframes scaleIn {
  0% {
    transform: scale(0.9);
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
  top: 15px;
  left: 15px;
  background: #f9f9f9;
  border: none;
  font-size: 26px;
  cursor: pointer;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  color: #333;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: 0.3s;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
}
.close-btn:hover {
  background: gold;
  color: #000;
  transform: scale(1.1);
}

.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}
.tabs button {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  background: #eee;
  cursor: pointer;
  transition: 0.3s;
  font-weight: 600;
}
.tabs button.active {
  background: #facc15;
  color: #fff;
}

.description {
  text-align: justify;
}

.tab-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.product-card {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  background: #fff;
  padding: 25px;
  border-radius: 16px;
  direction: rtl;
}

.product-image img {
  width: 100%;
  height: 280px;
  border-radius: 12px;
  border: 1px solid #ddd;
  object-fit: cover;
}

.product-details h2 {
  font-size: 22px;
  margin: 0;
}

.meta {
  display: flex;
  gap: 20px;
  margin-top: 6px;
}

.meta hr {
  flex-grow: 1;
  border: 0;
  border-top: 1px solid #ddd;
  margin-top: 5px;
}

.price {
  font-size: 20px;
  color: #000;
  font-weight: bold;
  margin: 20px 0;
}

.rating-display span {
  color: #facc15;
  font-size: 18px;
  margin-right: 2px;
}

.actions {
  display: flex;
  align-items: center;
  gap: 15px;
  margin: 15px 0;
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
  height: 40px;
  cursor: pointer;
  font-size: 18px;
  font-weight: bold;
}
.quantity-control span {
  width: 50px;
  text-align: center;
  font-weight: bold;
  font-size: 16px;
  background: rgb(231, 228, 228);
}

.add-to-cart {
  background: #facc15;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: 0.3s;
  width: 180px;
  color: #000;
}
.add-to-cart:hover {
  background: #eab308;
}

.share {
  margin-top: 20px;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}
.share button {
  width: 40px;
  height: 40px;
  border: none;
  cursor: pointer;
  font-size: 18px;
  transition: 0.3s;
  border-radius: 6px;
  color: #facc15;
  background: #000;
  display: flex;
  align-items: center;
  justify-content: center;
}
.share button:hover {
  background: #facc15;
  color: #222;
}

.add-review {
  border: 1px solid #ddd;
  padding: 15px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.review-stars span {
  font-size: 24px;
  color: #ccc;
  cursor: pointer;
  margin-right: 5px;
  transition: 0.3s;
}
.review-stars span.filled {
  color: gold;
}
.add-review textarea {
  width: 100%;
  height: 80px;
  padding: 8px;
  border-radius: 8px;
  border: 1px solid #ccc;
  resize: none;
}
.add-review button {
  align-self: flex-start;
  padding: 8px 16px;
  border: none;
  background: #facc15;
  color: #fff;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.3s;
}
.add-review button:hover {
  background: #eab308;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.review-text {
  color: #444;
}

.old-price {
  text-decoration: line-through;
  color: #888;
  margin-left: 8px;
}
.new-price {
  color: #e11d48;
}

@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    padding: 15px;
  }

  .product-card {
    grid-template-columns: 1fr;
    gap: 20px;
    padding: 15px;
  }

  .product-image img {
    height: 220px;
  }

  .product-details h2 {
    font-size: 18px;
  }

  .price {
    font-size: 18px;
  }

  .add-to-cart {
    width: 100%;
  }

  .tabs {
    justify-content: center;
  }

  .close-btn {
    top: 10px;
    left: 10px;
    width: 35px;
    height: 35px;
    font-size: 22px;
  }
}

@media (max-width: 480px) {
  .modal-content {
    padding: 10px;
  }

  .product-details h2 {
    font-size: 16px;
  }

  .price {
    font-size: 16px;
  }

  .quantity-control button {
    width: 35px;
    height: 35px;
  }

  .quantity-control span {
    width: 40px;
  }

  .share button {
    width: 36px;
    height: 36px;
    font-size: 16px;
  }
}

</style>
