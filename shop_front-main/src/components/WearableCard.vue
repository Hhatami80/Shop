<template>
  <div class="final-product-card">
    <div class="image-wrapper">
      <img :src="product.image || defaultImage" :alt="product.title" class="product-image" />
      <!-- <div v-if="!product.inStock" class="out-of-stock">ناموجود</div> -->
    </div>

    <div class="content">
      <h3 class="title">{{ product.title }}</h3>

      <p class="desc">
        {{ product.description }}
      </p>

      <div class="price-section">
        <div class="price">
          {{ formatPrice(product.price) }}
          <span class="toman">تومان</span>
        </div>

        <div v-if="product.discountPrice" class="old-price">
          {{ formatPrice(product.discountPrice) }}
        </div>
      </div>

      <button
        class="buy-btn"
        :disabled="product.is_active === false"
        @click.stop="$emit('openModal', product)"
      >
        {{ product.is_active === false ? 'ناموجود' : 'بررسی و خرید' }}
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  product: { type: Object, required: true },
})

const defaultImage = '/default-product.jpg'

const formatPrice = (price) => {
  return price ? price.toLocaleString('fa-IR') : '۰'
}
</script>

<style scoped>
.final-product-card {
  width: 420px;
  height: 640px;
  background: #fff;
  border-radius: 28px;
  overflow: hidden;
  box-shadow: 0 15px 45px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  transition: all 0.35s ease;
  cursor: pointer;
}

.final-product-card:hover {
  transform: translateY(-12px);
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.18);
}

.image-wrapper {
  height: 46%;
  background: #fafafa;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 30px;
  position: relative;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  transition: transform 0.5s ease;
}

.final-product-card:hover .product-image {
  transform: scale(1.04);
}

.out-of-stock {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  color: white;
  font-size: 1.8rem;
  font-weight: 900;
  display: flex;
  align-items: center;
  justify-content: center;
}

.content {
  height: 54%;
  padding: 22px 28px 26px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  gap: 14px;
}

.title {
  font-size: 1rem;
  font-weight: bold;
  color: #1a1a1a;
  margin: 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.desc {
  font-size: 0.875rem;
  color: #555;
  line-height: 1.7;
  margin: 0;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.price-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.price {
  font-size: 1.1rem;
  font-weight: 900;
  color: #f9c710;
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.price .toman {
  font-size: 1rem;
  color: #777;
}

.old-price {
  font-size: 1rem;
  color: #aaa;
  text-decoration: line-through;
}

.buy-btn {
  margin-top: 14px;
  width: 100%;
  padding: 12px;
  font-weight: bold;
  border-radius: 12px;
  border: none;
  background: #f9c710;
  color: #222;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(249, 199, 16, 0.4);
  transition: background 0.2s ease;
}

.buy-btn:hover:not(:disabled) {
  background: #e5b809;
}

.buy-btn:disabled {
  background: #ddd;
  color: #777;
  cursor: not-allowed;
}
</style>
