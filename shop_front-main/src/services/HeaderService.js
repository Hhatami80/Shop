import api from './AxiosService'

export const headerService = {
  async getHeader() {
    return api.get('/header')
  },

  async updateHeader(payload) {
    return api.put('/header/', payload)
  },

  async getlogo(){
    return api.get('/upload-logo1')
  },

  async uploadLogo(site_logo) {
    const formData = new FormData()
    formData.append('site_logo', site_logo)
    return api.put('/upload-logo/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },

}
