import { adminService } from '@/services/adminService'
import { defineStore } from 'pinia'
import { productService } from '@/services/ProductService'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

export const useAdminStore = defineStore('admin', {
  state: () => ({
    products: [],
    loading: false,
    error: null,
  }),

  actions: {
    async getAllProducts() {
      this.loading = true
      this.error = null
      const response = await adminService.getAdminPageProducts()
      this.products = response.data.products
      this.loading = false
    },
    async deleteProduct(productId) {
          this.loading = true
          this.error = null
          try {
            const response = await adminService.removeProduct(productId)
            this.getAllProducts()
            return response.data
          } catch (error) {
            this.error = 'خطا در حذف محصول'
            throw error
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
        this.getAllProducts()  
        toast.success(`محصول ${newStatus ? 'فعال' : 'غیرفعال'} شد.`) 

      } catch (error) {
        console.error('خطا در تغییر وضعیت محصول:', error)
        this.error = 'خطا در تغییر وضعیت محصول'
        toast.error(this.error)
      } finally {
        this.loading = false
      }
    },
  },
})
