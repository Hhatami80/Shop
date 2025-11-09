<template>
  <div class="articles-public-container">
    <h2>مقالات</h2>
    <div v-if="loading">در حال بارگذاری...</div>

    <div v-else class="articles-grid">
      <div
        class="article-card"
        v-for="a in store.articles"
        :key="a.id"
        @click="$router.push({ name: 'ArticleView', params: { id: a.id } })"
      >
        <img v-if="a.image" :src="a.image" alt="article image" />
        <h3>{{ a.title }}</h3>
        <p>{{ a.short_description }}</p>
        <p>{{ a.jalali_created_date }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useArticleStore } from '@/stores/ArticleStore'

const store = useArticleStore()
const loading = computed(() => store.loading)

onMounted(() => store.fetchArticles())
</script>

<style scoped>

.articles-public-container {
  direction: rtl;
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
  
  background-color: #fff;
  border-radius: 12px;    
  box-shadow: 0 2px 10px rgba(0,0,0,0.05); 
}


.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.article-card {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.article-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.1);
}

.article-card img {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.article-card h3 {
  margin: 0.8rem 1rem 0.4rem;
  font-size: 1.2rem;
}

.article-card p {
  margin: 0 1rem 1rem;
  color: #555;
  font-size: 0.95rem;

  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.5rem;
  max-height: calc(1.5rem * 3);

}
</style>
