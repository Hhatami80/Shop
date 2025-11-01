import api from './AxiosService'

export const orderService = {

  getAllOrders() {
    return api.get('/orders/')
  },


  createOrder(payload) {
    return api.post('/checkout/', payload)
  },


  requestZarinpalPayment(payload) {

    return api.post('/payments/zarinpal/request/', payload)
  },

 verifyZarinpalPayment({ authority, order_id, status }) {

  return api.post('/payments/zarinpal/verify/', { "authority": authority, "order_id":order_id, "status":status })
}
,


  updateOrder(id, data) {
    return api.patch(`/orders/${id}/`, data)
  },


  deleteOrder(id) {
    return api.delete(`/orders/${id}/`)
  },
}

export default orderService
