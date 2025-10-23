import api from './AxiosService'

export const productService = {
  get() {
    return api.get('/products')
  },
  getSpecialProducts(){
    return api.get('products/special-products')
  },
  getBestSellers(){
    return api.get('/products/bestsellers')
  },

  getById(productId) {
    return api.get(`/products/${productId}`)
  },

  getDescription(productId) {
    return api.get(`/products/${productId}/description`)
  },

  getSpecs(productId) {
    return api.get(`/products/${productId}/specs`)
  },

  getComments(productId) {
    return api.get(`/products/${productId}/comments`)
  },

  postComment(productId, payload) {
    return api.post(`/products/${productId}/comments`, payload)
  },

  create(productFormData) {
    return api.post('/product-add', productFormData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },

  update(productId, productFormData) {
    return api.put(`/product-edit/${productId}`, productFormData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },

  remove(productId) {
    return api.delete(`/product-delete/${productId}`)
  },
}
