
import { defineStore } from "pinia";
import { userService } from "@/services/userService";
import { toast } from "vue3-toastify";
import jalaali from "jalaali-js";


function toJalali(gDate) {
  if (!gDate) return "";
  const [gy, gm, gd] = gDate.split("-").map(Number);
  const { jy, jm, jd } = jalaali.toJalaali(gy, gm, gd);
  return `${jy}/${String(jm).padStart(2, "0")}/${String(jd).padStart(2, "0")}`;
}


function toGregorian(jDate) {
  if (!jDate) return "";
  const [jy, jm, jd] = jDate.split("/").map(Number);
  const { gy, gm, gd } = jalaali.toGregorian(jy, jm, jd);
  return `${gy}-${String(gm).padStart(2, "0")}-${String(gd).padStart(2, "0")}`;
}

export const useUserStore = defineStore("user", {
  state: () => ({
    profile: {
      username: "",
      email: "",
      phone: "",
      birthdate: "",
      image: null,
      previewImage: null,
    },
    addresses: [],
    bankAccounts: [],
    provinces: [],
    cities: [],
    users: [],
    loading: false,
    error: null,
  }),

  actions: {

    async fetchUsers() {
      this.loading = true;
      try {
        const res = await userService.getUsers();
        this.users = Array.isArray(res.data.data) ? res.data.data : [];
      } catch (err) {
        console.error("Fetch users error:", err);
        toast.error("خطا در دریافت کاربران سایت");
      } finally {
        this.loading = false;
      }
    },

    async deleteUser(userId) {
      try {
        await userService.deleteUser(userId);
        this.users = this.users.filter((u) => u.id !== userId);
        toast.success("کاربر حذف شد ");
      } catch (err) {
        console.error("Delete user error:", err);
        toast.error("خطا در حذف کاربر");
      }
    },

    async fetchProfile() {
      this.loading = true;
      try {
        const res = await userService.getProfile();
        const data = res.data.data || {};

        let birthdate = "";
        if (data.birthdate) {
          birthdate = data.birthdate.includes("-") ? toJalali(data.birthdate) : data.birthdate;
        }

        this.profile = {
          username: data.username || "",
          email: data.email || "",
          phone: data.phone || "",
          birthdate,
          image: data.image || null,
          previewImage: null,
          first_name: data.first_name || "",
          last_name: data.last_name || "",
        };
      } catch (error) {
        console.error("Fetch profile error:", error);
        toast.error("خطا در دریافت پروفایل");
      } finally {
        this.loading = false;
      }
    },

    async updateProfile(data) {
      try {
        let formData;
        if (data instanceof FormData) {
          formData = data;
        } else {
          formData = new FormData();
          for (const [key, value] of Object.entries(data)) {
            if (key === "birthdate" && value) {
             
              formData.append(key, toGregorian(value));
            } else {
              formData.append(key, value);
            }
          }
        }

        const res = await userService.updateProfile(formData);
        const updated = res.data.data || {};

        this.profile.username = updated.username || this.profile.username;
        this.profile.email = updated.email || this.profile.email;
        this.profile.phone = updated.phone || this.profile.phone;
        this.profile.birthdate = updated.birthdate ? toJalali(updated.birthdate) : this.profile.birthdate;
        this.profile.image = updated.image || this.profile.image;
        this.profile.previewImage = null;

        toast.success("پروفایل با موفقیت ذخیره شد ");
      } catch (error) {
        console.error("Update profile error:", error);
        toast.error("خطا در ذخیره پروفایل");
      }
    },

    updateProfileImage(file) {
      if (!file) return;
      this.profile.image = file;
      this.profile.previewImage = URL.createObjectURL(file);
    },


    async fetchAddresses() {
      try {
        const res = await userService.getAddresses();
        this.addresses = Array.isArray(res.data) ? res.data : [];
      } catch {
        toast.error("خطا در دریافت آدرس‌ها");
      }
    },

    async addAddress(address) {
      try {
        const res = await userService.addAddress(address);
        if (res.data) this.addresses.push(res.data);
        
      } catch {
        toast.error("خطا در ثبت آدرس");
      }
    },

    async deleteAddress(index) {
      const addr = this.addresses[index];
      if (!addr?.id) {
        this.addresses.splice(index, 1);
        return;
      }
      try {
        await userService.deleteAddress(addr.id);
        this.addresses.splice(index, 1);
        toast.success("آدرس حذف شد ");
      } catch {
        toast.error("خطا در حذف آدرس");
      }
    },

    async saveAddresses() {
      try {
        await userService.updateAddresses(this.addresses);
        toast.success("آدرس‌ها ذخیره شد ");
      } catch {
        toast.error("خطا در ذخیره آدرس‌ها");
      }
    },
    async updateAddress(id, address) {
  try {
    await userService.updateAddress(id, address);
    toast.success("آدرس با موفقیت به‌روزرسانی شد");
    await this.fetchAddresses();
  } catch (err) {
    console.error("Update address error:", err);
    toast.error("خطا در ویرایش آدرس");
  }
},


    async fetchBankAccounts() {
      try {
        const res = await userService.getBankInfo();
        const data = res.data?.bankAccounts;
        this.bankAccounts = Array.isArray(data) ? data : data ? [data] : [];
      } catch (error) {
        toast.error("خطا در دریافت اطلاعات بانکی");
        this.bankAccounts = [];
      }
    },

    async addBankAccount(account) {
      try {
        const res = await userService.addBankAccount(account);
        const newAccount = res.data;
        if (!Array.isArray(this.bankAccounts)) this.bankAccounts = [];
        this.bankAccounts.push({
          ...newAccount,
          bankName: account.bankName,
          bankLogo: account.bankLogo,
        });
        toast.success("حساب بانکی با موفقیت ثبت شد ");
        return this.bankAccounts[this.bankAccounts.length - 1];
      } catch (error) {
        toast.error("خطا در ثبت حساب بانکی");
        throw error;
      }
    },

    async deleteBankAccount(indexOrId) {
      const index =
        typeof indexOrId === "number"
          ? indexOrId
          : this.bankAccounts.findIndex((a) => a.id === indexOrId);
      if (index === -1) return;

      const account = this.bankAccounts[index];
      if (!account?.id) {
        this.bankAccounts.splice(index, 1);
        toast.info("حساب حذف شد");
        return;
      }

      try {
        await userService.deleteBankAccount(account.id);
        this.bankAccounts.splice(index, 1);
        toast.success("حساب بانکی حذف شد ");
      } catch {
        toast.error("خطا در حذف حساب بانکی");
      }
    },

    async fetchProvinces() {
      try {
        const res = await userService.getProvinces();
        this.provinces = res.data || [];
      } catch {
        toast.error("خطا در دریافت استان‌ها");
      }
    },

    async fetchCities(provinceId) {
      try {
        const res = await userService.getCities(provinceId);
        this.cities = res.data || [];
      } catch {
        toast.error("خطا در دریافت شهرها");
      }
    },
  },
});
