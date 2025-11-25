<template>
  <div class="article-view" v-if="article">
    <h1>{{ article.title }}</h1>
    <img v-if="article.image" :src="article.image" alt="article image" class="article-image" />

    <p class="article-meta">
      {{ article.jalali_created_date || 'تاریخ نامشخص' }}
    </p>

    <p class="article-short" v-html="rendered_short_description">
    </p>
    <div class="article-content" v-html="rendered_full_description"></div>
  </div>

  <div v-else-if="loading">در حال بارگذاری...</div>
  <div v-else class="error">مقاله یافت نشد</div>
</template>
<script setup>
import { onMounted, computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useArticleStore } from '@/stores/ArticleStore'
import md from "@/utils/markdown";


const store = useArticleStore()
const route = useRoute()

const short_description = ref("");
const full_description = ref("");

const rendered_short_description = ref("");
const rendered_full_description = ref("");

// store-based computed properties
const loading = computed(() => store.loading);
const article = computed(() => store.article);

// fetch article on mount
onMounted(() => {
  store.fetchArticle(route.params.id);
});

// React when article loads from store
watch(
  () => store.article,
  (a) => {
    if (!a) return;

    short_description.value = a.short_description || "";
    full_description.value = a.full_description || "";

    // Render markdown
    rendered_short_description.value = md.render(short_description.value);
    rendered_full_description.value = md.render(full_description.value);
  },
  { immediate: true }
);

</script>

<style scoped>
.article-view {
  direction: rtl;
  background: #ffffff;
  max-width: 900px;
  margin: 2rem auto;
  
  line-height: 1.9;
  padding: 2.5rem;
  border-radius: 20px;
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.08);
  color: #1f2937;
  transition: all 0.3s ease;
}

.article-view:hover {
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.article-view h1 {
  font-size: 2.4rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
  text-align: center;
  color: #0f172a;
  line-height: 1.3;
  position: relative;
}

.article-view h1::after {
  content: '';
  display: block;
  width: 80px;
  height: 4px;
  background: linear-gradient(90deg, #f59e0b, #f97316);
  margin: 0.8rem auto 0;
  border-radius: 2px;
}

.article-image {
  width: 100%;
  max-height: 480px;
  object-fit: cover;
  margin: 2rem 0;
  border-radius: 18px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.article-image:hover {
  transform: scale(1.02);
}

.article-meta {
  font-size: 0.9rem;
  color: #6b7280;
  margin-bottom: 1.5rem;
  text-align: center;
  font-style: italic;
}

.article-short {
  font-weight: 600;
  font-size: 1.2rem;
  margin: 1.5rem 0;
  color: #374151;
  background: #fef3c7;
  padding: 1rem 1.2rem;
  border-right: 6px solid #f59e0b;
  border-radius: 12px;
}

.article-content {
  color: #374151;
  font-size: 1.08rem;
  white-space: pre-line;
  line-height: 1.95;
}

.article-content p {
  margin-bottom: 1.2rem;
}

.article-content h2 {
  font-size: 1.6rem;
  margin: 2rem 0 1rem;
  font-weight: 700;
  color: #0f172a;
  border-right: 4px solid #f59e0b;
  padding-right: 0.8rem;
}

.article-content h3 {
  font-size: 1.3rem;
  margin: 1.5rem 0 1rem;
  font-weight: 600;
  color: #1e293b;
}

.article-content ul {
  padding-right: 1.5rem;
  margin-bottom: 1.2rem;
  list-style: disc;
}

.article-content li {
  margin-bottom: 0.5rem;
}

.article-content a {
  color: #2563eb;
  font-weight: 500;
  text-decoration: none;
  border-bottom: 1px dashed #2563eb;
  transition: color 0.2s ease, border-color 0.2s ease;
}
.article-content a:hover {
  color: #1d4ed8;
  border-color: #1d4ed8;
}

@media (max-width: 768px) {
  .article-view {
    padding: 1.5rem;
    margin: 1rem;
  }
  .article-view h1 {
    font-size: 1.8rem;
  }
  .article-content {
    font-size: 1rem;
  }
  .article-image {
    max-height: 300px;
  }
}
</style>