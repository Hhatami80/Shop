<template>
  <div class="article-list-container">
    <div class="article-list-header">
      <h2>مقالات</h2>
      <button class="btn" @click="$router.push({ name: 'ArticleCreate' })">ایجاد مقاله</button>
    </div>

    <ul class="article-list">
      <li class="article-card" v-for="a in store.articles" :key="a.id">
        <div class="article-card-body">
          <img v-if="a.image" :src="a.image" alt="article image" class="article-image" />
          <h3>{{ a.title }}</h3>
          <p>{{ a.short_description }}</p>
        </div>
        <div class="article-card-actions">
          <button
            class="btn btn-edit"
            @click="$router.push({ name: 'ArticleEdit', params: { id: a.id } })"
          >
            ویرایش
          </button>
          <button class="btn btn-delete" @click="store.deleteArticle(a.id)">حذف</button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useArticleStore } from '@/stores/ArticleStore'

const store = useArticleStore()
onMounted(() => store.fetchArticles())
</script>

<style scoped>
.article-list-container {
  --primary-gold: #ffd700;
  --gold-hover: #E6C200;
  --text-dark: #34495e; 
  --text-light: #7f8c8d; 
  --bg-light: #f8f9fa; 
  --card-bg: #ffffff;
  --border-light: #e9ecef;
  --danger-color: #dc3545;
  --danger-hover: #c82333;

  max-width: 1200px;
  margin: 30px auto;
  padding: 2rem;
  font-family: 'Vazirmatn', sans-serif;
  background: var(--bg-light);
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  direction: rtl;
}

h2 {
  color: var(--text-dark);
}

.article-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  border-bottom: 2px solid var(--border-light);
  padding-bottom: 15px;
}

.article-list-header h2 {
  font-size: 2rem;
  font-weight: 800;
}

.article-list-header .btn {
  background-color: var(--primary-gold);
  color: white;
  font-weight: 700;
  padding: 10px 22px;
  border-radius: 8px; 
  transition: all 0.3s ease;
  border: none;
  box-shadow: 0 3px 8px rgba(255, 215, 0, 0.3);
  flex-grow: 0;
}

.article-list-header .btn:hover {
  background-color: var(--gold-hover);
  transform: translateY(-1px); 
  box-shadow: 0 5px 12px rgba(255, 215, 0, 0.5);
}


.article-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  list-style: none;
  padding: 0;
  margin: 0;
}
.article-card {
  background: var(--card-bg);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  padding: 15px;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s, box-shadow 0.3s;
}
.article-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}


.article-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 8px;
  display: block;
  flex-shrink: 0;
  margin-bottom: 15px;
}


.article-card-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
}


.article-card-body h3 {
  margin: 0;
  font-size: 1.3rem;
  color: var(--text-dark);
  font-weight: 700;
  line-height: 1.4;
}


.article-card-body p {
  margin: 0;
  color: var(--text-light);
  font-size: 0.95rem;
  line-height: 1.6;
  
  display: -webkit-box;
  -webkit-line-clamp: 3; 
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  word-wrap: break-word;
}


.article-card-actions {
  margin-top: auto;
  padding-top: 15px;
  border-top: 1px solid var(--border-light);
  display: flex;
  gap: 10px;
}


.btn {
  padding: 10px 15px;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  color: #fff;
  flex: 1;
  text-align: center;
}

.btn-edit {
  background-color: var(--gold-hover); 
  color: white;
}

.btn-edit:hover {
  background-color: var(--primary-gold);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(255, 215, 0, 0.4);
}

.btn-delete {
  background-color: var(--danger-color);
}

.btn-delete:hover {
  background-color: var(--danger-hover);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(220, 53, 69, 0.4);
}
</style>