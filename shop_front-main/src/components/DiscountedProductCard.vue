<template>
  <div class="product-card">
    <div class="product-image">
      <img :src="product?.image || defaultImage" :alt="product.title" />
    </div>
    <div class="product-content">
      <h3 class="product-title">{{ product?.title }}</h3>
      <p class="product-description">{{ product?.description }}</p>

      <div class="product-price">
        <span class="original" v-if="showOriginalPrice">
          {{ formattedOriginalPrice }}
        </span>
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
    (discountedPrice.value > 0 ? discountedPrice.value : originalPrice.value).toLocaleString(
      'fa-IR'
    ) + ' تومان'
)

const showOriginalPrice = computed(
  () => discountedPrice.value > 0 && discountedPrice.value < originalPrice.value
)
</script>

<style scoped>
* {
  font-family: 'Yekan';
}

.product-card {
  display: flex;
  height: 460px;
  min-height: 460px;
  flex-direction: column;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s ease;
}
.product-card:hover {
  transform: translateY(-3px);
}

.product-image img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.product-content {
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

.product-description {
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

.product-price {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: space-between;
  gap: 6px;
  margin-bottom: 14px;
  margin-top: 10px;
}

.discounted {
  font-size: 18px;
  font-weight: bold;
  color: #f9c710;
}

.original {
  font-size: 14px;
  text-decoration: line-through;
  color: #888;
  opacity: 0.8;
}

.add-button {
  font-weight: bold;
  background: #f9c710;
  color: #222;
  border: none;
  border-radius: 10px;
  padding: 10px 14px;
  width: 100%;
  font-size: 15px;
  cursor: pointer;
  transition: background 0.2s ease;
  margin-top: auto;
}

.add-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.add-button:hover:not(:disabled) {
  background: #e5b809;
}
</style>

