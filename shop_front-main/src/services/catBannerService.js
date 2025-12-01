import api from '@/services/AxiosService'

export default {
  getBanners(categoryId) {
    return api.get(`/category/${categoryId}/banners`)
  },

  updateBanner(categoryId, bannerId, formData) {
    return api.patch(`/category-edit/${categoryId}/banners/${bannerId}`, formData)
  },

  deleteBanner(categoryId, bannerId) {
    return api.delete(`/category-delete/${categoryId}/banners/${bannerId}`)
  },

  addBanner(categoryId, formData) {
    return api.post(`/category-edit/${categoryId}/banners`, formData)
  },
}
