import { defineStore } from 'pinia'
import { userService } from '@/services/userService'
import axios from 'axios'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

export const useUserStore = defineStore('user', {
  state: () => ({
    profile: {
      username: '',
      email: '',
      phone: '',
      birthdate: '',
      image: null,
      imageUrl: '',
    },
    addresses: [],
    bankAccounts: {},
    provinces: [],
    cities: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchProfile() {
      this.loading = true
      this.error = null
      try {
        const res = await userService.getProfile()
        this.profile = { ...this.profile, ...res.data.data }
      } catch (error) {
        toast.error('خطا در دریافت پروفایل کاربر')
        this.error = error
      } finally {
        this.loading = false
      }
    },

    async updateProfile(newProfile) {
      this.loading = true
      try {
        let payload = newProfile
        if (!(newProfile instanceof FormData)) {
          payload = new FormData()
          Object.keys(newProfile).forEach((key) => {
            if (newProfile[key] !== null && newProfile[key] !== undefined) {
              payload.append(key, newProfile[key])
            }
          })
        }

        const res = await userService.updateProfile(payload)
        const updated = res.data.data || res.data
        this.profile = {
          ...this.profile,
          ...updated,
          imageUrl:
            this.profile.image instanceof File
              ? URL.createObjectURL(this.profile.image)
              : updated.imageUrl,
        }
        toast.success('پروفایل با موفقیت ذخیره شد!')
      } catch (error) {
        const message = error.response?.data?.message || error.message || 'خطا در ذخیره پروفایل'
        toast.error(message)
      } finally {
        this.loading = false
      }
    },

    updateProfileField(field, value) {
      if (field in this.profile) this.profile[field] = value
    },

    updateProfileImage(file) {
      this.profile.image = file
      this.profile.imageUrl = URL.createObjectURL(file)
    },

    async fetchAddresses() {
      try {
        const res = await userService.getAddresses()
        this.addresses = res.data || []
      } catch (error) {
        toast.error('خطا در دریافت آدرس‌ها')
      }
    },

    addAddress(address) {
      this.addresses.push(address)
      toast.success('آدرس افزوده شد ✅')
    },

    updateAddress(index, field, value) {
      if (this.addresses[index]) this.addresses[index][field] = value
    },

    deleteAddress(index) {
      this.addresses.splice(index, 1)
      toast.info('آدرس حذف شد')
    },

    async saveAddresses() {
      try {
        await userService.updateAddresses(this.addresses)
        toast.success('آدرس‌ها ذخیره شد')
      } catch (error) {
        toast.error('خطا در ذخیره آدرس‌ها')
      }
    },

    async fetchBankAccounts() {
      try {
        const res = await userService.getBankInfo()
        this.bankAccounts = res.data?.bankAccounts || {}
      } catch (error) {
        toast.error('خطا در دریافت اطلاعات بانکی')
      }
    },
    async addBankAccount(account) {
      try {
        console.log('store.addBankAccount called with:', account)
        const res = await userService.addBankAccount(account)
        console.log('server response for addBankAccount:', res.data)
        this.bankAccounts.push(res.data)
        toast.success('حساب بانکی با موفقیت ثبت شد ✅')
      } catch (error) {
        const message = error.response?.data?.message || 'خطا در ذخیره حساب بانکی'
        toast.error(message)
        throw error // تا کامپوننت هم بتونه خطا را catch کند
      }
    },
    async deleteBankAccount(index) {
      const account = this.bankAccounts[index]

      // اگر حساب هنوز id ندارد (جدید و روی سرور ثبت نشده)
      if (!account?.id) {
        this.bankAccounts.splice(index, 1) // حذف فقط در frontend
        return
      }

      // حذف واقعی از سرور
      try {
        await userService.deleteBankAccount(account)
        this.bankAccounts.splice(index, 1) // حذف از frontend بعد از موفقیت
        toast.success('حساب بانکی حذف شد ✅')
      } catch (error) {
        toast.error('خطا در حذف حساب بانکی')
      }
    },
    async saveBankAccounts() {
      try {
        await userService.updateBankInfo(this.bankAccounts)
        toast.success('اطلاعات بانکی ذخیره شد')
      } catch (error) {
        toast.error('خطا در ذخیره اطلاعات بانکی')
      }
    },

    async fetchProvinces() {
      try {
        const res = await axios.get('/api/provinces')
        this.provinces = res.data
      } catch (error) {
        toast.error('خطا در دریافت استان‌ها')
      }
    },

    async fetchCities(provinceId) {
      try {
        const res = await axios.get(`/api/cities?provinceId=${provinceId}`)
        this.cities = res.data
      } catch (error) {
        toast.error('خطا در دریافت شهرها')
      }
    },
  },
})
