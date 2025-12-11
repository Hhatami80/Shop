<template>
  <div class="bestseller-card" @click="$emit('click', product)">
    <div class="product-image">
      <img :src="product.image || defaultImage" :alt="product.title" />
    </div>

    <div class="product-info">
      <h3 class="product-title">{{ product.title }}</h3>
      <p class="product-desc">{{ product.description }}</p>

      <div class="price-section">
        <span class="price">
          <template v-if="product.is_purchasable">
            {{ formatPrice(product.price) }} تومان
          </template>

          <template v-else-if="!product.is_purchasable">
            {{ product.price }}
          </template>
        </span>
      </div>

      <button
        class="add-to-cart"
        :disabled="!product.inStock"
        @click.stop="$emit('openModal', product)"
      >
        {{ product.inStock ? 'بررسی و خرید' : 'ناموجود' }}
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  product: { type: Object, required: true },
})

const defaultImage = '/default-product.jpg'
const formatPrice = (price) => (price ? price.toLocaleString('fa-IR').replace(/٬/g, ",") : '۰')
</script>

<style scoped>
*,
*::before,
*::after {
  box-sizing: border-box;
  font-family: 'IRANSansX', sans-serif;
}

.bestseller-card {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 372px;
  min-width: 220px;
  height: 400px;
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
}

.bestseller-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 15px 35px rgba(0,0,0,0.15);
}

.product-image {
  width: 100%;
  aspect-ratio: 16/9;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-bottom: 2px solid #f9c710;
}

.product-info {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  padding: 12px 15px;
}

.product-title {
  font-size: 1rem;
  font-weight: bold;
  color: #222;
  margin-bottom: 6px;
  line-height: 1.4em;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.product-desc {
  font-size: 0.875rem;
  line-height: 1.4em;
  color: #555;
  margin-bottom: 10px;
  min-height: 60px;
  min-height: unset;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.price-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 6px;
  margin-bottom: 12px;
}

.price {
  font-size: 1rem;
  font-weight: bold;
  color: #f9c710;
}

.old-price {
  font-size: 0.875rem;
  text-decoration: line-through;
  color: #888;
}

.add-to-cart {
  margin-top: auto;
  width: 100%;
  padding: 10px;
  font-weight: bold;
  border-radius: 10px;
  border: none;
  background: #f9c710;
  color: #222;
  cursor: pointer;
  transition: background 0.2s ease;
}

.add-to-cart:hover:not(:disabled) {
  background: #e5b809;
}

.add-to-cart:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>
