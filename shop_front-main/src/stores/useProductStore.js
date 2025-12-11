import { defineStore } from 'pinia'
import { productService } from '@/services/ProductService'
import {toast} from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'
import { adminService } from '@/services/adminService'
import { useAdminStore } from './useAdminStore'

export const useProductStore = defineStore('product', {
  state: () => ({
    products: [],
    new_products: [],
    bestsellers: [],
    pooshine: [],
    bestsellersImage: [],
    selectedProduct: {},
    description: '',
    specs: {},
    featured: [],
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
          price: Number(p.price) || p.price,
          discounted_price: Number(p.discounted_price) || 0,
          image: p.image || '',
          description: p.description || '',
        }))

        this.products = response.data.products.map((p) => ({
          ...p,
          is_featured: p.is_featured ?? false,
          is_purchasable: p.is_purchasable,
          brand: p.brand || 'ناشناخته',
          price: Number(p.price) || p.price,
          discounted_price: Number(p.discounted_price) || 0,
          discount: Number(p.discount) || 0,
          description: p.description || '',
          image: p.image || '',
          short_description: p.short_description || '',
          properties: p.properties || [],
          category: p.category || {},
          is_active: p.is_active !== undefined ? p.is_active : true,
          average_rating: Number(p.average_rating) || 0,
          is_done: !!p.is_done,
          is_favorited: !!p.is_favorited,
          slug: p.slug || '',
          created_date: p.created_date || '',
          jalali_created_date: p.jalali_created_date || '',
        }))
        this.featured = response.data.featured || []
      } catch (error) {
        this.error = 'خطا در دریافت محصولات'
      } finally {
        this.loading = false
      }
    },
    async toggleProductStatus(productId, newStatus) {
      this.loading = true
      this.error = null

      try {
        const payload = { is_active: newStatus }
        const res = await productService.update(productId, payload)

        const updatedProduct = res?.data?.products?.[0]

        const index = this.products.findIndex((p) => p.id === productId)
        if (index !== -1) {
          if (updatedProduct) {
            this.products[index] = {
              ...this.products[index],
              ...updatedProduct,
            }
          } else {
            this.products[index].is_active = !!newStatus
          }
        }

        toast.success(`محصول ${newStatus ? 'فعال' : 'غیرفعال'} شد.`)
      } catch (error) {
        console.error('خطا در تغییر وضعیت محصول:', error)
        this.error = 'خطا در تغییر وضعیت محصول'
        toast.error(this.error)
      } finally {
        this.loading = false
      }
    },
    async getPooshine() {
      this.loading = true
      this.errors = null

      try {
        const response = await productService.get()
        this.pooshine = response.data.pooshineh || []
      } catch (error) {
        console.log(error)
        this.error = error.data.message
      } finally {
        this.loading = false
      }
    },
    async getBestSellers() {
      this.loading = true
      this.error = null
      try {
        const response = await productService.getBestSellers()
        this.bestsellers = response.data.bestsellers.map((p) => ({
          id: p.id,
          title: p.title,
          description: p.description || '',
          price: Number(p.price) || p.price,
          image: p.image.startsWith('http') ? p.image : `${import.meta.env.VITE_API_URL}${p.image}`,
          inStock: true,
          is_purchasable: p.is_purchasable
          
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
          is_featured: p.is_featured ?? false,
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
        this.comments = response.data.comment
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
       
        if (newProduct instanceof FormData) {
          
          if (!newProduct.has('is_featured')) {
            newProduct.append('is_featured', 0)
          }
        }

        await productService.create(newProduct)
        await this.getAllProducts()
      } catch (error) {
        console.log(error)
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
        if (updatedProduct instanceof FormData) {
          if (!updatedProduct.has('is_featured')) {
            updatedProduct.append('is_featured', 0)
          }
        }

        const response = await productService.update(productId, updatedProduct)

        if (response.status === 200 || response.status === 201) {
          useAdminStore().getAllProducts()
          toast.success('محصول با موفقیت ویرایش شد')
        }
      } catch (error) {
        console.log(error);
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
