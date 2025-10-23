import api from './AxiosService'

export const adminCommentService = {
  getAll(params = {}) {
    return api.get('/admin/comments', { params }) 
  },

  approve(id) {
    return api.post(`/admin/comments/${id}/approve`)
  },

  approveBulk(ids) {
    return api.post(`/admin/comments/bulk-approve`, { ids }) 
  },

  remove(id) {
    return api.delete(`/admin/comments/${id}`)
  },
}
