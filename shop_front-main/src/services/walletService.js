import api from './AxiosService'

export const walletService = {
  getBalance() {
    return api.get('/wallet/balance/')
  },

  getTransactions() {
    return api.get('/wallet/transactions/')
  },

  addCredit(payload) {
    return api.post('/wallet/deposit/', payload)
  },

  withdraw(payload) {
    return api.post('/wallet/withdraw/', payload)
  },
  createPayment(payload) {
  return api.post('/wallet/payment/', payload)
},
walletVerify(payload) {
  return api.post('/wallet/verify/', payload)
}
} 

export default walletService
