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
}

export default walletService
