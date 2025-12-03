<template>
  <div class="product-card" @click="$emit('click')">
    <div class="product-image">
      <img :src="product?.image || defaultImage" :alt="product.title" />
    </div>

    <div class="product-details">
      <h3 class="product-title">{{ product?.title }}</h3>
      <p class="product-description">{{ product?.description }}</p>

      <div class="product-price">
        <span class="original-price" v-if="hasDiscount">{{ formattedOriginalPrice }}</span>
        <span class="final-price">{{ formattedDiscountedPrice }}</span>
      </div>

      <button class="btn-add-to-cart" @click.stop="$emit('open-modal', product)">
        <i class="fas fa-cart-plus"></i> بررسی و خرید
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  product: { type: Object, required: true },
})

const defaultImage = '/default-product.jpg'

const originalPrice = computed(() => Number(props.product?.price) || 0)
const discountedPrice = computed(() => Number(props.product?.discounted_price) || 0)

const hasDiscount = computed(() => discountedPrice.value > 0 && discountedPrice.value < originalPrice.value)

const formattedOriginalPrice = computed(() => 
  originalPrice.value.toLocaleString('fa-IR').replace(/٬/g, ',') + ' تومان'
)

const formattedDiscountedPrice = computed(() => {
  const price = hasDiscount.value ? discountedPrice.value : originalPrice.value
  return price.toLocaleString('fa-IR').replace(/٬/g, ',') + ' تومان'
})
</script>

<style scoped>
*,
*::before,
*::after {
  box-sizing: border-box;
}

.product-card {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 372px;
  min-width: 220px;
  height: 400px;
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
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
  border-bottom: 2px solid #f9c710; /* This was missing! */
}

.product-details {
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

.product-description {
  font-size: 0.875rem;
  line-height: 1.4em;
  color: #555;
  margin-bottom: 10px;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-price {
  margin-bottom: 10px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.original-price {
  font-size: 0.875rem;
  color: #888;
  text-decoration: line-through;
}

.final-price {
  font-size: 1rem;
  font-weight: bold;
  color: #f9c710;
}

.btn-add-to-cart {
  margin-top: auto;
  width: 100%;
  padding: 10px;
  font-weight: bold;
  border-radius: 10px;
  border: none;
  background: #f9c710;
  color: #222;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 6px;
  box-shadow: 0 4px 15px rgba(249, 199, 16, 0.4);
  transition: background 0.2s ease, box-shadow 0.2s ease;
}

.btn-add-to-cart:hover {
  background: #e5b809;
  box-shadow: 0 6px 20px rgba(229, 184, 9, 0.5);
}
</style>