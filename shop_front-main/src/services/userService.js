import api from './AxiosService'

export const userService = {
  async getUsers() {
    return api.get('/users')
  },

  async deleteUser(id) {
    return api.delete(`/users/${id}`)
  },

  async getProfile() {
    return api.get('/user/profile/')
  },

  async updateProfile(data) {
    return api.put('/user/profile/', data, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },
  async getAddresses() {
    return api.get('/user/addresses/')
  },

  async updateAddresses(data) {
    return api.put('/user/addresses/', { addresses: data })
  },

  async getBankInfo() {
    return api.get('/user/bank-accounts/') 
  },

  async addBankAccount(account) {
    return api.post('/user/bank-accounts/', account)
  },
  updateBankInfo(data) {
    return api.put('/user/bank-accounts/', data)
  },


  async deleteBankAccount(account) {
    
    return api.delete(`/user/bank-accounts/${account.id || account.cardNumber}`)
  },
  async getProvinces() {
  return api.get('/locations/provinces/') 
},

async getCities(province) {
  return api.get(`/locations/cities?province=${encodeURIComponent(province)}`) 
},
}
