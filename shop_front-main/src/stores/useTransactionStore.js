// src/stores/useTransactionStore.js
import { defineStore } from "pinia";
import { transactionService } from "@/services/transactionService";
import { toast } from "vue3-toastify";

export const useTransactionStore = defineStore("transactions", {
  state: () => ({
    transactions: [],
    loading: false,
    error: null,
  }),

  getters: {
    totalTransactions: (state) => state.transactions.length,
    successfulTransactions: (state) =>
      state.transactions.filter((t) => t.status === "success"),
    failedTransactions: (state) =>
      state.transactions.filter((t) => t.status === "failed"),
  },

  actions: {
    async fetchAll(params = {}) {
      this.loading = true;
      this.error = null;
      try {
        const res = await transactionService.getAll(params);
        this.transactions = res.data.results || res.data || [];
      } catch (error) {
        console.error("Transaction Fetch Error:", error);
        this.error = error;
        toast.error("خطا در دریافت تراکنش‌ها");
      } finally {
        this.loading = false;
      }
    },

    async fetchById(id) {
      try {
        const res = await transactionService.getById(id);
        return res.data;
      } catch (error) {
        console.error(error);
        toast.error("خطا در دریافت جزئیات تراکنش");
      }
    },

    async deleteTransaction(id) {
      try {
        await transactionService.delete(id);
        this.transactions = this.transactions.filter((t) => t.id !== id);
        toast.success("تراکنش با موفقیت حذف شد");
      } catch (error) {
        console.error(error);
        toast.error("خطا در حذف تراکنش");
      }
    },
  },
});
