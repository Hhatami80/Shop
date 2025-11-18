import api from './AxiosService'

export const adminCommentService = {
  getAll({status="all", per_page=30, page=1, q} = {}) {
    const params = { status, per_page, page }
    if (q) params.q = q
    return api.get('/admin/comments', {params}) 
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
