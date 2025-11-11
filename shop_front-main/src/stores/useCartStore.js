import { defineStore } from 'pinia'
import { cartService } from '@/services/cartService'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'
import { useLoginStore } from '@/stores/useLoginStore'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [],
    loading: false,
    error: null,
  }),
  getters: {
    totalQuantity: (state) => state.items.reduce((sum, i) => sum + i.quantity, 0),
    totalPrice: (state) =>
      state.items.reduce(
        (sum, i) => sum + i.quantity * (i.product.discounted_price || i.product.price),
        0
      ),
  },
  actions: {
    async fetchCart() {
      const loginStore = useLoginStore()
      if (!loginStore.isAuthenticated) {
        this.items = [] 
        return
      }

      this.loading = true
      this.error = null
      try {
        const response = await cartService.getCart()
        this.items = response.data.items || []
      } catch (error) {
        this.error = error
        toast.error(error.response?.data?.message || 'خطا در دریافت سبد خرید')
      } finally {
        this.loading = false
      }
    },

    async addItem(productId, quantity = 1) {
      const loginStore = useLoginStore()
      if (!loginStore.isAuthenticated) {
        toast.error('برای افزودن به سبد خرید باید وارد شوید')
        return
      }

      this.loading = true
      this.error = null
      try {
        const response = await cartService.addToCart(productId, quantity)
        if (response.data.items) {
          this.items = response.data.items
        } else {
          const existingItem = this.items.find(i => i.product.id === productId)
          if (existingItem) {
            existingItem.quantity += quantity
            existingItem.total_price =
              existingItem.quantity * (existingItem.product.discounted_price || existingItem.product.price)
          } else {
            this.items.push({
              id: response.data.item_id || Math.random(),
              product: response.data.product,
              quantity,
              total_price: quantity * (response.data.product.discounted_price || response.data.product.price)
            })
          }
        }
        toast.success('محصول به سبد اضافه شد')
      } catch (error) {
        toast.error(error.response?.data?.message || 'خطا در افزودن به سبد')
      } finally {
        this.loading = false
      }
    },

    async updateItem(itemId, quantity) {
      if (quantity < 1) return
      const loginStore = useLoginStore()
      if (!loginStore.isAuthenticated) return

      const itemIndex = this.items.findIndex(i => i.id === itemId)
      if (itemIndex === -1) return
      this.items[itemIndex].quantity = quantity
      this.items[itemIndex].total_price =
        quantity * (this.items[itemIndex].product.discounted_price || this.items[itemIndex].product.price)

      try {
        await cartService.updateCartItem(itemId, quantity)
      } catch (error) {
        toast.error(error.response?.data?.message || 'خطا در به روزرسانی سبد خرید')
      }
    },

    async removeItem(itemId) {
      const loginStore = useLoginStore()
      if (!loginStore.isAuthenticated) {
        this.items = this.items.filter((i) => i.id !== itemId)
        return
      }

      this.loading = true
      this.error = null
      try {
        await cartService.removeFromCart(itemId)
        this.items = this.items.filter((i) => i.id !== itemId)
        toast.success('محصول با موفقیت حذف شد')
      } catch (error) {
        toast.error(error.response?.data?.message || 'خطا در حذف محصول')
      } finally {
        this.loading = false
      }
    },

    async clearCart() {
      const loginStore = useLoginStore()
      if (!loginStore.isAuthenticated) {
        this.items = []
        return
      }

      this.loading = true
      this.error = null
      try {
        await cartService.clearCart()
        this.items = []
        toast.success('سبد خرید خالی شد')
      } catch (error) {
        toast.error(error.response?.data?.message || 'خطا در خالی شدن سبد خرید')
      } finally {
        this.loading = false
      }
    },
  },
})
