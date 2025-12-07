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
        <!-- <p>{{ a.jalali_created_date }}</p> -->
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
@import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazir-font@v30.1.0/dist/font-face.css');

.articles-public-container {
  direction: rtl;
  max-width: 1200px;
  margin: 30px auto;
  padding: 2rem;
  background-color: #fff;   
}

h2 {
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
  text-align: center;
}


.articles-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr); 
  gap: 1.5rem;
}


.article-card {
  width: 100%;
  max-width: 330px;
  background: #fff;
  border-radius: 12px;

  
  border: 2px solid #f9c710;

  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
}


.article-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 20px rgba(249, 199, 16, 0.25);
  border-color: #ffdd33; 
}


.article-card img {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.article-content {
  padding: 1rem;
}

.article-card h3 {
  margin: 0.8rem 1rem 0.4rem;
  font-size: 1.2rem;
  padding-right: 12px;
}

.article-card p {
  margin: 0 1rem 1rem;
  color: #555;
  font-size: 0.95rem;
  padding-right: 12px;

  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.5rem;
  max-height: calc(1.5rem * 3);
}


.article-date {
  display: block;
  font-size: 0.85rem;
  color: #888;
  text-align: left;
}

.loading {
  text-align: center;
  padding: 20px 0;
  font-size: 1.1rem;
}
@media (max-width: 992px) {
  .articles-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .articles-grid {
    grid-template-columns: repeat(1, 1fr);
  }
}

</style>

