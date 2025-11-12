import { defineStore } from 'pinia'
import orderService from '@/services/orderService'
import { useCartStore } from './useCartStore'
import { toast } from 'vue3-toastify'

export const useOrderStore = defineStore('orderStore', {
  state: () => ({
    loading: false,
    orders: [],
    totalOrders: 0,
    page: 1,
    perPage: 5,
    paymentMethod: 'online',
    gateway: 'zarinpal',
  }),

  actions: {
    async fetchOrders({ page = 1, perPage = 5, status = 'all', forUser = false } = {}) {
      this.loading = true
      try {
        const params = { page, perPage, status }
        const response = forUser
          ? await orderService.getAllOrders({ page, perPage, status, user: 'current' })
          : await orderService.getAllOrders({ page, perPage, status })

        this.orders = response?.data?.results || []
        this.totalOrders = response?.data?.count || 0
        this.page = page
        this.perPage = perPage
      } catch (err) {
        console.error('Fetch orders error:', err)
        toast.error('خطا در دریافت سفارش‌ها')
        this.orders = []
        this.totalOrders = 0
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
      if (!cartStore.items.length) {
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
        return response?.data?.success === true
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
        const error = err.response?.data.error
        if (error) toast.warning(error)
        else toast.error('خطا در تغییر وضعیت سفارش')
      }
    },

    async cancelUserOrder(orderId) {
      try {
        await orderService.updateOrder(orderId, { status: 'canceled' })
        await this.fetchOrders({ page: this.page, perPage: this.perPage, forUser: true })
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
