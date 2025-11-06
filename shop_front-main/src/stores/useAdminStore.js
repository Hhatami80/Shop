import { adminService } from '@/services/adminService'
import { defineStore } from 'pinia'

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
  },
})
