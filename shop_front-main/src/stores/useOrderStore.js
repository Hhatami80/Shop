import { defineStore } from 'pinia'
import orderService from '@/services/orderService'
import { useCartStore } from './useCartStore'
import { toast } from 'vue3-toastify'

export const useOrderStore = defineStore('orderStore', {
  state: () => ({
    loading: false,
    orders: [],
    paymentMethod: 'online',
    gateway: 'zarinpal',
  }),

  actions: {
    async fetchOrders() {
      this.loading = true
      try {
        const response = await orderService.getAllOrders()

        if (Array.isArray(response?.data?.data)) {
          this.orders = response.data.data
        } else if (Array.isArray(response?.data)) {
          this.orders = response.data
        } else {
          this.orders = []
        }
      } catch (err) {
        console.error('Fetch orders error:', err)
        toast.error('خطا در دریافت سفارش‌ها')
      } finally {
        this.loading = false
      }
    },

    async fetchOrderById(orderId) {
      this.loading = true
      try {
        const response = await orderService.getOrderById(orderId)
        return response?.data || null
      } catch (err) {
        console.error('Fetch order by ID error:', err)
        toast.error('خطا در دریافت جزئیات سفارش')
        return null
      } finally {
        this.loading = false
      }
    },

    async submitOrder(payload) {
      const cartStore = useCartStore()

      if (cartStore.items.length === 0) {
        toast.error('سبد خرید خالی است!')
        return null
      }

      this.loading = true
      try {
        if (this.paymentMethod === 'online') {
          const response = await orderService.requestZarinpalPayment(payload)
          const result = response?.data?.data || response?.data || {}
          const paymentUrl = result?.paymentUrl
          const orderId = result?.orderId

          console.log('🔹 Zarinpal Payment Response:', result)

          if (paymentUrl) {
            toast.success('در حال انتقال به درگاه پرداخت...')
            return { paymentUrl, orderId }
          } else {
            toast.error('خطا در دریافت لینک پرداخت')
            return null
          }
        } else {
          const response = await orderService.createOrder(payload)
          await cartStore.clearCart()
          toast.success('سفارش با موفقیت ثبت شد ')
          return { orderId: response?.data?.id }
        }
      } catch (err) {
        console.error('Submit order error:', err)
        const detail = err?.response?.data?.detail || err?.message
        toast.error(detail || 'خطا در ثبت سفارش')
        return null
      } finally {
        this.loading = false
      }
    },

    async verifyPayment(authority, order_id, status) {
      this.loading = true
      try {
        const response = await orderService.verifyZarinpalPayment({ authority, order_id, status })
        const data = response?.data
        if (data?.success == true) {
          return true
        } else {
          toast.error('پرداخت ناموفق بود ')
          return false
        }
      } catch (err) {
        console.error('Verify payment error:', err)
        toast.error('خطا در بررسی پرداخت')
        return false
      } finally {
        this.loading = false
      }
    },

    async updateOrderStatus(orderId, status) {
      try {
        await orderService.requestChangeStatus(orderId, status)
        toast.success('وضعیت سفارش به‌روزرسانی شد ')
      } catch (err) {
        console.error('Update order status error:', err)
        toast.error('خطا در تغییر وضعیت سفارش')
      }
    },

    async cancelUserOrder(orderId) {
      try {
        const response = await orderService.updateOrder(orderId, { status: 'canceled' })
        if (response.status === 204) {
          this.orders = await this.fetchOrders()
        }
        toast.success('سفارش با موفقیت لغو شد')
      } catch (err) {
        console.error('Cancel order error:', err)
        toast.error('لغو سفارش موفقیت‌آمیز نبود')
      }
    },

    async deleteOrder(orderId) {
      try {
        await orderService.deleteOrder(orderId)
        this.orders = this.orders.filter((o) => o.id !== orderId)
        toast.success('سفارش حذف شد ')
      } catch (err) {
        console.error('Delete order error:', err)
        toast.error('خطا در حذف سفارش')
      }
    },
  },
})
