<template>
  <Loading v-model="isLoading" :logo="logoImage" />
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
      <WearableSlider title="پوشینه ها" :products="productStore.pooshine" />
    </section>

    <section class="section">
      <FeaturedProductsSlider title="محصولات ویژه" :discounted_product="productStore.featured" />
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
import { useFeatureSectionStore } from '@/stores/FeatureSectionStore'
import { useCategoryStore } from '@/stores/useCategoryStore'
import { useAboutUsStore } from '@/stores/useAboutUsStore'
import AboutUs from '@/components/AboutUs.vue'
import FeatureSection from '@/components/FeatureSection.vue'
import HomeCategories from '@/components/HomeCategories.vue'
import ProductSlider from '@/components/ProductSlider.vue'
import BestSellerSlider from '@/components/BestSellerSlider.vue'
import WearableSlider from '@/components/WearableSlider.vue'
import Loading from '@/components/Loading.vue'
import logoImage from '@/assets/image/logo.png'

const isLoading = ref(true)
const productStore = useProductStore()
const selectedProductId = ref(null)
const FeatureSectionStore = useFeatureSectionStore()
const CategoryStore = useCategoryStore()
const AboutUsStore = useAboutUsStore()

const newProducts = computed(() => productStore.new_products)

onMounted(async () => {
  try {
    await Promise.all([
      productStore.getAllProducts(),
      productStore.getBestSellers(),
      productStore.getPooshine(),
      FeatureSectionStore.getFeatureSection(),
      CategoryStore.getAllCategories(),
      AboutUsStore.fetchAbout(),
    ])

    if (productStore.products.length > 0) {
      const firstId = productStore.products[0].id
      await productStore.getProductById(firstId)
    }
  } finally {
    isLoading.value = false
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
