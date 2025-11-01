import { defineStore } from "pinia";
import { walletService } from "@/services/walletService";
import { toast } from "vue3-toastify";

export const useWalletStore = defineStore("wallet", {
  state: () => ({
    balance: 0,
    transactions: [],
    pendingAmount: 0,
    loading: false,
    error: null,
  }),

  getters: {
    hasTransactions: (state) => state.transactions.length > 0,
    creditTransactions: (state) => state.transactions.filter((t) => t.type === "credit"),
    debitTransactions: (state) => state.transactions.filter((t) => t.type === "debit"),
  },

  actions: {
    async fetchBalance() {
      this.loading = true;
      this.error = null;
      try {
        const res = await walletService.getBalance();
        this.balance = res.data.balance || 0;
      } catch (error) {
        console.error(error);
        toast.error("خطا در دریافت موجودی");
        this.error = error;
      } finally {
        this.loading = false;
      }
    },

    async fetchTransactions() {
      this.loading = true;
      this.error = null;
      try {
        const res = await walletService.getTransactions();
        this.transactions = res.data.transactions || [];
      } catch (error) {
        console.error(error);
        toast.error("خطا در دریافت تراکنش‌ها");
        this.error = error;
      } finally {
        this.loading = false;
      }
    },

    async addCredit({ amount, method }) {
      this.loading = true;
      try {
        await walletService.addCredit({ amount, method });
        toast.success("کیف پول با موفقیت شارژ شد ");
        await Promise.all([this.fetchBalance(), this.fetchTransactions()]);
      } catch (error) {
        console.error(error);
        toast.error("خطا در شارژ کیف پول");
      } finally {
        this.loading = false;
      }
    },

    async withdraw({ amount, method }) {
      this.loading = true;
      try {
        await walletService.withdraw({ amount, method });
        toast.success("برداشت با موفقیت انجام شد ");
        await Promise.all([this.fetchBalance(), this.fetchTransactions()]);
      } catch (error) {
        console.error(error);
        toast.error("خطا در برداشت وجه");
      } finally {
        this.loading = false;
      }
    },

    async createPayment({ amount, gateway }) {
      try {
        const res = await walletService.createPayment({ amount, gateway });
        return res.data; 
      } catch (error) {
        console.error(error);
        toast.error("خطا در ایجاد پرداخت");
        throw error;
      }
    },
    async verifyWallet({ payment_id, authority, zarinpal_status }) {
      try {
        const res = await walletService.walletVerify({ payment_id, authority, zarinpal_status })
        return res.data
      } catch {
        console.error(error);
        toast.error("خطا در احراز پرداخت")
      }
    }
  },
});
