import api from './AxiosService'

export const categoryService = {
  get() {
    return api.get('/category')
  },

  post(category) {
    return api.post('/category-add', category, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },

  put(id, category) {
    return api.put(`/category-edit/${id}`, category, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },

  delete(id) {
    return api.delete(`/category-delete/${id}`)
  },
}
