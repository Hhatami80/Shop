<template>
  <div class="bestseller-card" @click="$emit('click', product)">
    <img :src="product.image" :alt="product.title" class="product-image" />

    <div class="product-info">
      <h3 class="product-title">{{ product.title }}</h3>
      <p  class="product-desc">
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
  flex-direction: column;
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  height: 460px;
  min-height: 460px;
}
.bestseller-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}
.product-image {
  width: 100%;
  height: 230px;
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
  font-size: 1.1rem;
  font-weight: 700;
  color: #222;
  margin: 0 0 6px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
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
  font-weight: bold;
  color: #f9c710;
  margin-bottom: 8px;
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
  padding: 8px 15px;
  border: none;
  border-radius: 12px;
  background: #f9c710;
  color: #222;
  font-weight: 600;
  cursor: pointer;
  transition: 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  box-shadow: 0 4px 15px rgba(249, 199, 16, 0.4);
}
.add-to-cart:hover {
  background: #e5b809;
  box-shadow: 0 6px 20px rgba(229, 184, 9, 0.5);
}
@media (max-width: 768px) {
  .product-card {
    height: 340px;
  }
  .product-image {
    height: 140px;
  }
}
</style>
