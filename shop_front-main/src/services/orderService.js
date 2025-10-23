import api from './AxiosService'

export const orderService = {
  getAllOrders() {
    return api.get('/orders/')
  },

  createOrder(payload) {
    return api.post('/orders/', payload)
  },

  updateOrder(id, data) {
    return api.patch(`/orders/${id}/`, data)
  },

  deleteOrder(id) {
    return api.delete(`/orders/${id}/`)
  },
}

export default orderService
