import { defineStore } from 'pinia'
import { walletService } from '@/services/walletService'
import { toast } from 'vue3-toastify'

export const useWalletStore = defineStore('wallet', {
  state: () => ({
    balance: 0,
    transactions: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchBalance() {
      this.loading = true
      try {
        const res = await walletService.getBalance()
        this.balance = res.data.balance
      } catch (error) {
        toast.error('خطا در دریافت موجودی')
        this.error = error
      } finally {
        this.loading = false
      }
    },

    async fetchTransactions() {
      this.loading = true
      try {
        const res = await walletService.getTransactions()
        this.transactions = res.data.transactions
      } catch (error) {
        toast.error('خطا در دریافت تراکنش‌ها')
        this.error = error
      } finally {
        this.loading = false
      }
    },

    async addCredit({ amount, method }) {
      try {
        await walletService.addCredit({ amount, method })
        toast.success('کیف پول شارژ شد ✅')
        await this.fetchBalance()
        await this.fetchTransactions()
      } catch (error) {
        toast.error('خطا در شارژ کیف پول')
      }
    },

    async withdraw({ amount, method }) {
      try {
        await walletService.withdraw({ amount, method })
        toast.success('برداشت با موفقیت انجام شد')
        await this.fetchBalance()
        await this.fetchTransactions()
      } catch (error) {
        toast.error('خطا در برداشت')
      }
    },
  },
})
