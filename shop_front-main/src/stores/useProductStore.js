import { defineStore } from 'pinia'
import { productService } from '@/services/ProductService'
import Vue3Toastify from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

export const useProductStore = defineStore('product', {
  state: () => ({
    products: [],
    new_products: [],
    bestsellers: [],
    bestsellersImage: [],
    selectedProduct: {},
    description: '',
    specs: {},
    comments: [],
    commentForm: { text: '' },
    filters: { minPrice: 0, maxPrice: 0, selectedBrands: [] },
    loading: false,
    error: null,
    submitSuccess: false,
    submitError: null,
  }),

  getters: {
    filteredProducts(state) {
      return state.products.filter((product) => {
        const price = Number(product.price) || 0
        const brand = product.brand || ''
        const isPriceValid =
          (!state.filters.minPrice || price >= state.filters.minPrice) &&
          (!state.filters.maxPrice || price <= state.filters.maxPrice)
        const isBrandValid =
          state.filters.selectedBrands.length === 0 || state.filters.selectedBrands.includes(brand)
        return isPriceValid && isBrandValid
      })
    },
  },

  actions: {
    async getAllProducts() {
      this.loading = true
      this.error = null
      try {
        const response = await productService.get()
        this.new_products = response.data.new_products.map((p) => ({
          ...p,
          price: Number(p.price) || 0,
          discounted_price: Number(p.discounted_price) || 0,
          image: p.image || '',
          description: p.description || '',
        }))

        this.products = response.data.products.map((p) => ({
          ...p,
          brand: p.brand || 'ناشناخته',
          price: Number(p.price) || 0,
          discounted_price: Number(p.discounted_price) || 0,
          discount: Number(p.discount) || 0,
          description: p.description || '',
          image: p.image || '',
          short_description: p.short_description || '',
          properties: p.properties || [],
          category: p.category || {},
          average_rating: Number(p.average_rating) || 0,
          is_done: !!p.is_done,
          is_favorited: !!p.is_favorited,
          slug: p.slug || '',
          created_date: p.created_date || '',
          jalali_created_date: p.jalali_created_date || '',
        }))
      } catch (error) {
        this.error = 'خطا در دریافت محصولات'
      } finally {
        this.loading = false
      }
    },

    async getBestSellers() {
      this.loading = true
      this.error = null
      try {
        const response = await productService.getBestSellers()
        this.bestsellers = response.data.products.map((p) => ({
          id: p.id,
          title: p.title,
          description: p.description || '',
          price: Number(p.price) || 0,
          image: p.image.startsWith('http') ? p.image : `${import.meta.env.VITE_API_URL}${p.image}`,
          inStock: true,
        }))
      } catch (error) {
        this.error = 'خطا در دریافت محصولات'
      } finally {
        this.loading = false
      }
    },

    async getProductById(productId) {
      this.loading = true
      this.error = null
      try {
        const response = await productService.getById(productId)
        const p = response.data.product
        this.selectedProduct = {
          ...p,
          brand: p.brand || 'ناشناخته',
          price: Number(p.price) || 0,
          discounted_price: Number(p.discounted_price) || 0,
          discount: Number(p.discount) || 0,
          description: p.description || '',
          image: p.image || '',
          short_description: p.short_description || '',
          properties: p.properties || [],
          category: p.category || {},
          average_rating: Number(p.average_rating) || 0,
          is_done: !!p.is_done,
          is_favorited: !!p.is_favorited,
          slug: p.slug || '',
          created_date: p.created_date || '',
          jalali_created_date: p.jalali_created_date || '',
        }
      } catch (error) {
        this.error = 'محصول یافت نشد'
      } finally {
        this.loading = false
      }
    },

    async fetchTabsData(productId) {
      this.loading = true
      this.error = null
      try {
        const [descRes, specsRes, commentsRes] = await Promise.all([
          productService.getDescription(productId),
          productService.getSpecs(productId),
          productService.getComments(productId),
        ])
        this.description = descRes.data.description || ''
        this.specs = specsRes.data.specs || {}
        this.comments = commentsRes.data.comments || []
      } catch (error) {
        this.error = 'خطا در دریافت اطلاعات تب‌ها'
      } finally {
        this.loading = false
      }
    },

    async submitComment(productId) {
      this.submitSuccess = false
      this.submitError = null
      try {
        await productService.postComment(productId, { text: this.commentForm.text })
        this.submitSuccess = true
        this.commentForm.text = ''
        const res = await productService.getComments(productId)
        this.comments = res.data.comments || []
      } catch (err) {
        this.submitError = 'خطا در ارسال نظر. لطفاً دوباره تلاش کنید.'
      }
    },

    setPriceFilter(min, max) {
      this.filters.minPrice = min
      this.filters.maxPrice = max
    },

    toggleBrandFilter(brand) {
      const index = this.filters.selectedBrands.indexOf(brand)
      if (index > -1) this.filters.selectedBrands.splice(index, 1)
      else this.filters.selectedBrands.push(brand)
    },

    clearFilters() {
      this.filters = { minPrice: 0, maxPrice: 0, selectedBrands: [] }
    },

    async addProduct(newProduct) {
      this.loading = true
      this.error = null
      try {
        const response = await productService.create(newProduct)
        const p = response.data
        this.getAllProducts()
        // this.products.push({
        //   ...p
        //   // brand: p.brand || 'ناشناخته',
        //   // price: Number(p.price) || 0,
        //   // discounted_price: Number(p.discounted_price) || 0,
        //   // discount: Number(p.discount) || 0,
        //   // description: p.description || '',
        //   // image: p.image || '',
        //   // short_description: p.short_description || '',
        //   // properties: p.properties || [],
        //   // category: p.category || {},
        //   // average_rating: Number(p.average_rating) || 0,
        //   // is_done: !!p.is_done,
        //   // is_favorited: !!p.is_favorited,
        //   // slug: p.slug || '',
        //   // created_date: p.created_date || '',
        //   // jalali_created_date: p.jalali_created_date || '',
        // })
      } catch (error) {
        this.error = 'خطا در افزودن محصول'
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateProduct(productId, updatedProduct) {
      this.loading = true
      this.error = null
      try {
        const response = await productService.update(productId, updatedProduct)
        const index = this.products.findIndex((p) => p.id === productId)
        if (index !== -1) {
          const p = response.data
          this.products[index] = {
            ...p,
            brand: p.brand || 'ناشناخته',
            price: Number(p.price) || 0,
            discounted_price: Number(p.discounted_price) || 0,
            discount: Number(p.discount) || 0,
            description: p.description || '',
            image: p.image || '',
            short_description: p.short_description || '',
            properties: p.properties || [],
            category: p.category || {},
            average_rating: Number(p.average_rating) || 0,
            is_done: !!p.is_done,
            is_favorited: !!p.is_favorited,
            slug: p.slug || '',
            created_date: p.created_date || '',
            jalali_created_date: p.jalali_created_date || '',
          }
        }
      } catch (error) {
        this.error = 'خطا در ویرایش محصول'
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteProduct(productId) {
      this.loading = true
      this.error = null
      try {
        await productService.remove(productId)
        this.products = this.products.filter((p) => p.id !== productId)
      } catch (error) {
        this.error = 'خطا در حذف محصول'
        throw error
      } finally {
        this.loading = false
      }
    },
  },
})
