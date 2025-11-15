<template>
  <div class="product-card" @click="$emit('click')">
    <img v-if="product.image" :src="product?.image" :alt="product.title" class="product-image" />

    <div class="product-details">
      <h3 class="product-title" >{{ product?.title }}</h3>
      <p class="product-description" >
        {{ product?.description }}
      </p>

      <div class="product-price">
        <span class="final-price">{{ product?.price.toLocaleString('fa-IR').replace(/٬/g, ",")}} تومان</span>
      </div>

      <button class="btn-add-to-cart" @click.stop="$emit('open-modal', product)">
        <i class="fas fa-cart-plus"></i> بررسی و خرید
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  product: { type: Object, required: true },
})
</script>

<style scoped>
.product-card {
  display: flex;
  flex-direction: column;
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  height: 460px;
  min-height: 460px;
  width: 372px;

}
.product-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}
.product-image {
  width: 100%;
  height: 230px;
  object-fit: cover;
  border-bottom: 2px solid #f9c710;
}
.product-details {
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
  font-weight: bold;
  color: #f9c710;
  margin-bottom: 8px;
}
.final-price {
  font-weight: bold;
  font-size: 1rem;
}
.btn-add-to-cart {
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
.btn-add-to-cart:hover {
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
