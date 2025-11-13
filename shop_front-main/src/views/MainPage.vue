<template>
  <div class="page-container">
    <section class="section">
      <search-box />
    </section>

    <section class="section">
      <home-categories />
    </section>

    <section id="about" class="section">
      <about-us />
    </section>

    <section class="section">
      <feature-section />
    </section>
    <section class="section">
      <BestSellerSlider :products="productStore.bestsellers" />
    </section>

    <section class="section">
      <FeaturedProductsSlider title="محصولات ویژه" :discounted_product="productStore.bestsellers" />
    </section>

    <section class="section">
      <ProductSlider :new_products="newProducts" title="محصولات جدید" />


    </section>
  </div>
</template>




<script setup>
import { onMounted, ref, computed } from 'vue'
import FeaturedProductsSlider from '@/components/FeaturedProductsSlider.vue'
import { useProductStore } from '@/stores/useProductStore'
import AboutUs from '@/components/AboutUs.vue'
import FeatureSection from '@/components/FeatureSection.vue'
import HomeCategories from '@/components/HomeCategories.vue'
import ProductSlider from '@/components/ProductSlider.vue'
import BestSellerSlider from '@/components/BestSellerSlider.vue'

const productStore = useProductStore()
const selectedProductId = ref(null)



const newProducts = computed(() => productStore.new_products)


onMounted(async () => {
  await productStore.getAllProducts()
  await productStore.getBestSellers()

  if (productStore.products.length > 0) {
    selectedProductId.value = productStore.products[0].id
    await productStore.getProductById(selectedProductId.value)
  }
})
</script>
<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.section {
  width: 100%;
}
.section:last-child {
  margin-bottom: 60px;
}
</style>



