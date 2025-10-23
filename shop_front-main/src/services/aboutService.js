import api from './AxiosService'

export const aboutService = {
  async fetchAboutData() {
    return await api.get('/aboutus')
  },

  async updateAboutData(data) {
    return await api.put('/aboutus/', data)
  },

  
}
