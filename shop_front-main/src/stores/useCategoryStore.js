import { defineStore } from 'pinia';
import { categoryService } from '@/services/categoryService';
import { productService } from '@/services/ProductService';
import { toast } from 'vue3-toastify';

export const useCategoryStore = defineStore('category', {
  state: () => ({
    allCategories: [],
    allProducts: [],    
  }),

  getters: {
    getProductsByCategory: (state) => {
      return (categoryId) =>
        state.allProducts.filter((p) => p.category?.id === categoryId);
    },
    getCategoryById: (state) => {
      return (categoryId) =>
        state.allCategories.find((cat) => cat.id === categoryId) || null;
    },
  },

  actions: {
    async getAllCategories() {
      try {
        const response = await categoryService.get();
        this.allCategories = response.data.categories || response.data || [];
      } catch (error) {
        console.error('خطا در دریافت دسته‌ها:', error.response?.data || error);
        toast.error('خطا در دریافت دسته‌بندی‌ها');
      }
    },

    async addCategory(formData) {
      try {
        await categoryService.post(formData);
        await this.getAllCategories();
        toast.success('دسته‌بندی با موفقیت افزوده شد.');
        return true;
      } catch (error) {
        console.error('خطا در افزودن دسته:', error);
        toast.error('خطا در افزودن دسته‌بندی.');
        return false;
      }
    },

    async updateCategory(id, formData) {
      try {
        await categoryService.put(id, formData);
        await this.getAllCategories();
        toast.success('دسته‌بندی با موفقیت ویرایش شد.');
      } catch (error) {
        console.error('خطا در ویرایش دسته:', error);
        toast.error('خطا در ویرایش دسته‌بندی.');
      }
    },

    async deleteCategory(id) {
      try {
        await categoryService.delete(id);
        await this.getAllCategories();
        toast.success('دسته‌بندی با موفقیت حذف شد.');
      } catch (error) {
        console.error('خطا در حذف دسته:', error);
        toast.error('خطا در حذف دسته‌بندی.');
      }
    },
    async getAllProducts() {
      try {
        const response = await productService.get();
        this.allProducts = response.data.products || [];
      } catch (error) {
        console.error('خطا در دریافت محصولات:', error.response?.data || error);
        toast.error('خطا در دریافت محصولات');
      }
    },
  },
});
