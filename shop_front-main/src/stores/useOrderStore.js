import { defineStore } from 'pinia'
import orderService from '@/services/orderService'
import { useCartStore } from './useCartStore'
import { toast } from 'vue3-toastify'

export const useOrderStore = defineStore('orderStore', {
  state: () => ({
    loading: false,
    orders: [],
    paymentMethod: 'online',
  }),

  actions: {
    async fetchOrders() {
      this.loading = true
      try {
        const response = await orderService.getAllOrders()
        this.orders = response.data
      } catch (err) {
        console.error(err)
        toast.error('خطا در دریافت سفارش‌ها')
      } finally {
        this.loading = false
      }
    },

    async submitOrder() {
      const cartStore = useCartStore()
      if (!cartStore.items.length) {
        toast.error('سبد خرید خالی است!')
        return
      }

      this.loading = true
      try {
        const payload = {
          items: cartStore.items.map((i) => ({
            product_id: i.product.id,
            quantity: i.quantity,
            unit_price: i.product.discounted_price || i.product.price,
          })),
          total_price: cartStore.totalPrice,
          payment_method: this.paymentMethod,
          address_id: 1,
        }

        const response = await orderService.createOrder(payload)
        toast.success('سفارش با موفقیت ثبت شد')
        cartStore.clearCart()
        return response.id
      } catch (err) {
        console.error(err)
        toast.error('خطا در ثبت سفارش')
      } finally {
        this.loading = false
      }
    },

    async updateOrderStatus(orderId, status) {
      try {
        await orderService.updateOrder(orderId, { status })
        toast.success('وضعیت سفارش به‌روزرسانی شد')
      } catch (err) {
        console.error(err)
        toast.error('خطا در تغییر وضعیت سفارش')
      }
    },

    async deleteOrder(orderId) {
      try {
        await orderService.deleteOrder(orderId)
        this.orders = this.orders.filter((o) => o.id !== orderId)
        toast.success('سفارش حذف شد')
      } catch (err) {
        console.error(err)
        toast.error('خطا در حذف سفارش')
      }
    },
  },
})
