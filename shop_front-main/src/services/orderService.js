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


  async updateOrder(id, data) {
    return api.patch(`/orders/${id}`, {'status': data.status})
  },
  requestChangeStatus(orderId, status) {
  return api.patch(`/admin/orders/${orderId}/change_status/`, { status });
},



  deleteOrder(id) {
    return api.delete(`/admin/orders/${id}/`)
  },
  getOrderById(id) {
  return api.get(`/orders/${id}`)
},

}

export default orderService
