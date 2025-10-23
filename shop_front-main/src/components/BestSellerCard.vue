<template>
  <div class="bestseller-card" @click="$emit('click', product)">
    <img :src="product.image" :alt="product.title" class="product-image" />

    <div class="product-info">
      <h3 class="product-title">{{ product.title }}</h3>
      <p v-if="product.description" class="product-desc">
        {{ product.description }}
      </p>

      <div class="price-section">
        <span class="price">{{ formatPrice(product.price)  }} تومان</span>
        <span v-if="product.Price" class="old-price">
          {{ product.price ? product.price.toLocaleString() : '0' }}
        </span>
      </div>

      <button
        class="add-to-cart"
        :disabled="!product.inStock"
        @click.stop="$emit('openModal', product)"
      >
        {{ product.inStock ? 'بررسی و خرید  ' : 'ناموجود' }}
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  product: {
    type: Object,
    required: true,
  },
})

const formatPrice = (price) => (price ? price.toLocaleString('fa-IR').replace(/٬/g, ",") : '۰')
</script>

<style scoped>
.bestseller-card {
  display: flex;
  height: 460px;
  min-height: 460px;
  font-family: 'Yekan';
  flex-direction: column;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s ease;
}
.bestseller-card:hover {
  transform: translateY(-3px);
}
.product-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}
.product-info {
  padding: 12px;
  text-align: right;
}
.product-title {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 10px;
  line-height: 1.5em;
  font-size: 16px;
  font-weight: bold;
  color: #222;
}
.product-desc {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  position: relative;
  margin-bottom: 10px;
  line-height: 1.5em;
  max-height: 4.5em;
  word-break: break-word;
  min-height: 72px;
}
.price-section {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}
.price {
  font-size: 16px;
  font-weight: bold;
  color: #f9c710;
}
.old-price {
  font-size: 14px;
  color: #888;
  text-decoration: line-through;
}
.add-to-cart {
  font-weight: bold;
  background: #f9c710;
  font-family: 'Yekan';
  color: #222;
  border: none;
  border-radius: 10px;
  padding: 8px 12px;
  width: 100%;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s ease;
}
.add-to-cart:disabled {
  background: #ccc;
  cursor: not-allowed;
}
.add-to-cart:hover:not(:disabled) {
  background: #e5b809;
}
</style>
