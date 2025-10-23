import { defineStore } from 'pinia'
import { articleService } from '@/services/ArticleService'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

export const useArticleStore = defineStore('articles', {
  state: () => ({
    articles: [],
    article: null,
    loading: false,
  }),

  actions: {
    async fetchArticles() {
      this.loading = true
      const res = await articleService.getAll()
      this.articles = res.data.articles || []
      this.loading = false
    },

    async fetchArticle(id) {
      this.loading = true
      const res = await articleService.get(id)
    
      this.article = res.data.articles

  
      this.loading = false
      return this.article 
    },

    async createArticle(formData) {
      await articleService.create(formData)
      toast.success('مقاله با موفقیت اضافه شد')
    },

    async updateArticle(id, formData) {
      await articleService.update(id, formData)
      toast.success('مقاله با موفقیت به روزرسانی شد')
    },

    async deleteArticle(id) {
      await articleService.remove(id)
      toast.success('مقاله با موفقیت حذف شد')
      await this.fetchArticles()
    },
  },
})
