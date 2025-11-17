<template>
  <div class="product-card" @click="$emit('click')">
    <div class="product-image">
      <img :src="product?.image || defaultImage" :alt="product.title" />
    </div>
    <div class="product-content">
      <h3 class="product-title">{{ product?.title }}</h3>
      <p class="product-description">{{ product?.description }}</p>

      <div class="product-price">
        <span class="original" v-if="showOriginalPrice">{{ formattedOriginalPrice }}</span>
        <span class="discounted">{{ formattedDiscountedPrice }}</span>
      </div>

      <button class="add-button" @click.stop="$emit('open-modal', product)">بررسی و خرید</button>
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

const formattedOriginalPrice = computed(
  () => originalPrice.value.toLocaleString('fa-IR') + ' تومان'
)
const formattedDiscountedPrice = computed(
  () =>
    (discountedPrice.value > 0 ? discountedPrice.value : originalPrice.value).toLocaleString('fa-IR') +
    ' تومان'
)
const showOriginalPrice = computed(
  () => discountedPrice.value > 0 && discountedPrice.value < originalPrice.value
)
</script>

<style scoped>
*,
*::before,
*::after {
  box-sizing: border-box;
  font-family: 'IRANSansX', sans-serif;
}

.product-card {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 372px;
  min-width: 220px;
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0,0,0,0.08);
  transition: transform 0.2s ease;
  cursor: pointer;
}

.product-card:hover {
  transform: translateY(-3px);
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
}

.product-content {
  padding: 12px;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.product-title {
  font-size: 1rem;
  font-weight: bold;
  color: #222;
  line-height: 1.4em;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.product-description {
  font-size: 0.875rem;
  color: #555;
  line-height: 1.4em;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 60px;
}

.product-price {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  gap: 6px;
}

.discounted {
  font-size: 1rem;
  font-weight: bold;
  color: #f9c710;
}

.original {
  font-size: 0.875rem;
  text-decoration: line-through;
  color: #888;
}

.add-button {
  margin-top: auto;
  padding: 10px;
  font-weight: bold;
  border-radius: 10px;
  border: none;
  width: 100%;
  background: #f9c710;
  color: #222;
  cursor: pointer;
  transition: background 0.2s;
}

.add-button:hover {
  background: #e5b809;
}

.add-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>
