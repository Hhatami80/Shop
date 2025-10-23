import api from './AxiosService'



export const articleService = {
  getAll() {
    return api.get('/articles/')
  },

  get(id) {
    return api.get(`/articles-edit/${id}/`)
  },

  create(formData) {
    return api.post('/articles', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },

  update(id, formData) {
    return api.put(`/articles-edit/${id}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },

  remove(id) {
    return api.delete(`/articles-delete/${id}`)
  }
}