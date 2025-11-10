<template>
  <div class="cart-grid">
    <div v-if="cartStore.items.length === 0" class="empty-cart">
      <div class="empty-icon">
        <i class="fas fa-shopping-cart"></i>
      </div>
      <p>سبد خرید شما خالی است</p>
      <small>برای شروع خرید، محصولات مورد علاقه خود را اضافه کنید!</small>
    </div>

    <div v-else class="cart-items">
      <div v-for="item in cartStore.items" :key="item.id" class="cart-item">
        <img :src="item.product.image" alt="product" class="item-image" />

        <div class="item-info">
          <h4 class="item-title">{{ item.product.title }}</h4>
          <p class="item-desc">{{ item.product.description }}</p>

          <div class="item-footer">
            <div class="price-section">
              <p
                v-if="
                  item.product.discounted_price &&
                  item.product.discounted_price < item.product.price
                "
                class="item-discount"
              >
                <i class="fas fa-fire"></i>
                {{
                  (
                    (item.product.price - item.product.discounted_price) *
                    item.quantity
                  ).toLocaleString()
                }}
                تومان تخفیف
              </p>
              <p class="item-price">
                {{ Number(item.product.discounted_price || item.product.price).toLocaleString() }}
                تومان / واحد
              </p>
            </div>

            <div class="qty-section">
              <button v-if="item.quantity > 1" @click="decrease(item)" class="qty-btn increase-btn">
                <i class="fas fa-minus"></i>
              </button>
              <button v-else @click="removeItem(item.id)" class="qty-btn delete-btn">
                <i class="fas fa-trash"></i>
              </button>
              <span class="qty-text">{{ item.quantity }}</span>
              <button @click="increase(item)" class="qty-btn increase-btn">
                <i class="fas fa-plus"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="cart-summary" v-if="cartStore.items.length > 0">
      <p class="total">
        <span>تعداد کالاها:</span> <span>{{ cartStore.totalQuantity }}</span>
      </p>
      <p class="total">
        <span>جمع کل:</span>
        <span>{{ cartStore.totalPrice.toLocaleString() }} تومان</span>
      </p>
      <button class="checkout-btn" @click="goToCheckout">تایید و تکمیل سفارش</button>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useCartStore } from '@/stores/useCartStore'
import { useRouter } from 'vue-router'
const router = useRouter()

function goToCheckout() {
  router.push({ name: 'checkout' })
}

const cartStore = useCartStore()
onMounted(() => cartStore.fetchCart())

function increase(item) {
  cartStore.updateItem(item.id, item.quantity + 1)
}
function decrease(item) {
  if (item.quantity > 1) cartStore.updateItem(item.id, item.quantity - 1)
}
function removeItem(id) {
  cartStore.removeItem(id)
}
</script>

<style scoped>
.cart-grid {
  --primary-gold: #ffd700;
  --gold-hover: #e6c200;
  --text-dark: #34495e;
  --text-light: #7f8c8d;
  --bg-light: #f4f6f9;
  --card-bg: #ffffff;
  --danger-color: #dc3545;
  --danger-hover: #c82333;
  --shadow-subtle: rgba(0, 0, 0, 0.05);

  display: grid;
  grid-template-columns: 2.5fr 1fr;
  gap: 30px;
  direction: rtl;

  max-width: 1200px;
  margin: 40px auto;
  padding: 20px;
  background: var(--bg-light);
  border-radius: 16px;
}

.empty-cart {
  grid-column: 1 / -1;
  text-align: center;
  font-size: 1.2rem;
  color: var(--text-dark);
  padding: 60px 30px;
  border-radius: 16px;
  background: var(--card-bg);
  border: 2px dashed var(--primary-gold);
  font-weight: 600;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;

  animation: fadeScaleIn 0.5s ease forwards;
}

.empty-cart .empty-icon {
  font-size: 50px;
  color: var(--primary-gold);
  animation: bounce 1.2s infinite;
}


.empty-cart small {
  font-size: 0.9rem;
  color: var(--text-light);
}

@keyframes fadeScaleIn {
  0% {
    opacity: 0;
    transform: scale(0.7);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes bounce {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.cart-items {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.cart-item {
  display: flex;
  gap: 20px;
  padding: 25px;
  background: var(--card-bg);
  border-radius: 12px;
  box-shadow: 0 4px 15px var(--shadow-subtle);
  border: 1px solid var(--border-light);
  transition:
    transform 0.3s,
    box-shadow 0.3s;
}
.cart-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.item-image {
  width: 120px;
  height: 120px;
  border-radius: 10px;
  object-fit: contain;
  background: #fff;
  padding: 5px;
  border: 1px solid var(--border-light);
  flex-shrink: 0;
}

.item-info {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  flex: 1;
}

.item-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-dark);
  margin-bottom: 8px;
}

.item-desc {
  font-size: 0.9rem;
  color: var(--text-light);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 15px;
  background: var(--bg-light);
  padding: 15px 18px;
  border-radius: 10px;
}

.price-section {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.item-discount {
  color: var(--danger-color);
  font-weight: 700;
  font-size: 0.85rem;
}

.item-discount i {
  color: var(--danger-color);
  margin-left: 4px;
}

.item-price {
  font-weight: 800;
  font-size: 1.1rem;
  color: var(--text-dark);
  padding: 4px 10px;
  border-radius: 8px;
  min-width: 120px;
  text-align: center;
  background: #ffeeb2;
}

.qty-section {
  display: flex;
  align-items: center;
  gap: 8px;
  border: 1px solid var(--primary-gold);
  border-radius: 10px;
  overflow: hidden;
}

.qty-btn {
  background: var(--primary-gold);
  border: none;
  width: 38px;
  height: 38px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 16px;
  color: var(--text-dark);
  transition: all 0.2s;
}
.qty-btn:hover {
  background: var(--gold-hover);
}

.delete-btn {
  background: var(--danger-color);
  color: #fff;
}
.delete-btn:hover {
  background: var(--danger-hover);
}

.qty-text {
  min-width: 35px;
  text-align: center;
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--text-dark);
}

.cart-summary {
  border-radius: 12px;
  padding: 30px;
  background: var(--card-bg);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: sticky;
  top: 70px;
  align-self: start;
}

.cart-summary p.total {
  display: flex;
  justify-content: space-between;
  font-weight: 600;
  font-size: 1.1rem;
  margin: 0;
  padding-bottom: 10px;
  border-bottom: 1px dashed var(--border-light);
}

.cart-summary p.total:last-of-type {
  font-size: 1.3rem;
  font-weight: 800;
  color: var(--text-dark);
  border-bottom: none;
  padding-top: 10px;
}

.checkout-btn {
  background: var(--primary-gold);
  color: var(--text-dark);
  border: none;
  width: 100%;
  padding: 16px;
  font-size: 1.1rem;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 700;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
}
.checkout-btn:hover {
  background: var(--gold-hover);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 215, 0, 0.6);
}

@media (max-width: 992px) {
  .cart-grid {
    grid-template-columns: 1fr;
    margin: 20px;
  }
  .cart-summary {
    position: static;
    top: auto;
  }
  .cart-item {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  .item-footer {
    width: 100%;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
  }
  .item-image {
    width: 150px;
    height: 150px;
  }
}
</style>
