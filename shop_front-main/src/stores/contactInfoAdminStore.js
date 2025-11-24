import { defineStore } from "pinia";
import { contactService } from "@/services/contactService";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";


export const useAdminContactInfoStore = defineStore("adminContactInfo", {
  state: () => ({
    info: null,
    loading: false,
    saving: false,
    error: null
  }),

  actions: {
    async fetchInfo() {
  this.loading = true;
  try {
    const res = await contactService.getInfo();
    this.info = res.data;
  } catch {
    this.info = {
      title: "",
      subtitle: "",
      address: "",
      phone: "",
      email: "",
      work_hours: "",
      instagram: "",
      telegram: "",
      whatsapp: ""
    };
  } finally {
    this.loading = false;
  }
}
,

    async updateInfo() {
      this.saving = true;
      try {
        await contactService.updateInfo(this.info);
        toast.success("اطلاعات با موفقیت ذخیره شد");
      } catch (err) {
        toast.error("خطایی رخ داد");
      } finally {
        this.saving = false;
      }
    }
  }
});
