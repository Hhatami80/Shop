import { defineStore } from 'pinia'
import { categoryService } from '@/services/categoryService'
import { productService } from '@/services/ProductService'
import { toast } from 'vue3-toastify'

export const useCategoryStore = defineStore('category', {
  state: () => ({
    allCategories: [],
    allProducts: [],
    categoryProducts: {},
  }),

  getters: {
    getCategoryById: (state) => {
      return (categoryId) => state.allCategories.find((cat) => cat.id === categoryId) || null
    },
    getProductsByCategory: (state) => {
      return (categoryId) => state.categoryProducts[categoryId] || []
    },
  },

  actions: {
    async getAllCategories() {
      this.loading = true
      try {
        const response = await categoryService.get()
        this.allCategories = response.data.categories || response.data || []
      } catch (error) {
        console.error('خطا در دریافت دسته‌ها:', error.response?.data || error)
        toast.error('خطا در دریافت دسته‌بندی‌ها')
      } finally {
        this.loading = false
      }
    },
    async getProductsByCategoryApi(categoryId) {
      try {
        const res = await productService.getByCategory(categoryId)
        this.categoryProducts[categoryId] = res.data
      } catch (error) {
        console.error('خطا در دریافت محصولات دسته:', error.response?.data || error)
        toast.error('خطا در دریافت محصولات دسته')
      }
    },

    async addCategory(formData) {
      try {
        await categoryService.post(formData)
        await this.getAllCategories()
        toast.success('دسته‌بندی با موفقیت افزوده شد.')
        return true
      } catch (error) {
        console.error('خطا در افزودن دسته:', error)
        toast.error('خطا در افزودن دسته‌بندی.')
        return false
      }
    },

    async updateCategory(id, formData) {
      try {
        await categoryService.put(id, formData)
        await this.getAllCategories()
        toast.success('دسته‌بندی با موفقیت ویرایش شد.')
      } catch (error) {
        console.error('خطا در ویرایش دسته:', error)
        toast.error('خطا در ویرایش دسته‌بندی.')
      }
    },

    async deleteCategory(id) {
      try {
        await categoryService.delete(id)
        await this.getAllCategories()
        toast.success('دسته‌بندی با موفقیت حذف شد.')
      } catch (error) {
        console.error('خطا در حذف دسته:', error)
        toast.error('خطا در حذف دسته‌بندی.')
      }
    },
    // async getAllProducts() {
    //   try {
    //     const res = await productService.get()

    //     const merged = [
    //       ...(res.data.products || []),
    //       ...(res.data.pooshineh || []),
    //       ...(res.data.new_products || []),
    //       ...(res.data.discounted_products || []),
    //       ...(res.data.featured || []),
    //     ]
    //     this.allProducts = Array.from(new Map(merged.map((p) => [p.id, p])).values())
    //   } catch (error) {
    //     console.error('خطا در دریافت محصولات:', error.response?.data || error)
    //     toast.error('خطا در دریافت محصولات')
    //   }
    // },
  },
})
