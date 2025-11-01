import api from './AxiosService'

export const userService = {

  getUsers() {
    return api.get('/users')
  },
  deleteUser(id) {
    return api.delete(`/users/${id}`)
  },


  getProfile() {
    return api.get('/user/profile/')
  },
  updateProfile(data) {
    return api.put('/user/profile/', data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },


  getAddresses() {
    return api.get('/user/addresses/')
  },
  addAddress(address) {
    return api.post('/user/addresses/', address)
  },
  updateAddresses(addresses) {
    return api.put('/user/addresses/', { addresses })
  },
  deleteAddress(id) {
    return api.delete(`/user/addresses/${id}`)
  },


  getBankInfo() {
    return api.get('/user/bank-accounts/')
  },
  addBankAccount(account) {
    return api.post('/user/bank-accounts/', account)
  },
  updateBankInfo(data) {
    return api.put('/user/bank-accounts/', data)
  },
  deleteBankAccount(id) {
    return api.delete(`/user/bank-accounts-delete/${id}`)
  },


  getProvinces() {
    return api.get('/locations/provinces/')
  },
  getCities(provinceId) {
    return api.get(`/locations/cities?province=${encodeURIComponent(provinceId)}`)
  },
}
