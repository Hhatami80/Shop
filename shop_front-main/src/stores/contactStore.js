import { defineStore } from "pinia";
import { contactService } from "@/services/contactService";

export const useContactStore = defineStore("contactInfo", {
  state: () => ({
    info: null,
    loading: false,
    error: null
  }),

  actions: {
    async fetchInfo() {
      this.loading = true;
      this.error = null;

      try {
        const res = await contactService.getInfo();
        this.info = res.data;
      } catch (err) {
        this.error = "خطا در دریافت اطلاعات تماس";
      } finally {
        this.loading = false;
      }
    }
  }
});
