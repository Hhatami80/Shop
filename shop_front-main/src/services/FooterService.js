import api from './AxiosService'

export const footerService = {

  getFooter() {
    return api.get('/footer')
  },


  updateFooter(payload) {
    return api.put('admin/footer/', payload, {
      headers: {
        Accept: 'application/json',
      },
    })
  },
}
