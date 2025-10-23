<template>
  <div class="category-card" @click="goToCategory">
    <div class="image-wrapper">
      <img
        v-if="category.image"
        :src="category.image"
        :alt="category.name"
        class="category-image"
      />
    </div>
    <h3 class="category-title">{{ category.title }}</h3>
  </div>
</template>

<script setup>
import router from '@/router';

const props = defineProps({
  category: {
    type: Object,
    required: true,
  },
})
const goToCategory = () =>{
  router.push(`/categories/${props.category.id}`)
}
</script>

<style scoped>
.category-card {
  background: linear-gradient(145deg, #f9c710, #e0b60c);
  border-radius: 16px;
  padding: 20px 15px;
  text-align: center;
  color: #111;
  font-family: 'Yekan', sans-serif;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;

  
  width: 200px;
  height: 240px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.category-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25);
}

.image-wrapper {
  flex: 1; 
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 120px; 
}

.category-image {
  max-width: 100px;
  max-height: 100px;
  object-fit: contain;
  background: #fff;
  padding: 10px;
  border-radius: 12px;
}

.category-title {
  font-size: 18px;
  font-weight: 700;
  margin-top: 12px;
}
</style>
