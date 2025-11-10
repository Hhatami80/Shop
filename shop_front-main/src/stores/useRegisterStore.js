import { defineStore } from 'pinia'
import { registerService } from '@/services/RegisterService'
import { otpService } from '@/services/OtpService'
import { toast } from 'vue3-toastify'

export const useRegisterStore = defineStore('register', {
  state: () => ({
    registerUser: {
      username: '',
      phone: '',
      password: '',
      confirm_password: '',
    },
    otpCode: '',
    step: 'form',
  }),

  actions: {
    resetRegisterData() {
      this.registerUser = {
        username: '',
        phone: '',
        password: '',
        confirm_password: '',
      }
      this.otpCode = ''
      this.step = 'form'
    },

    async requestOtp() {
      const { username, phone, password, confirm_password } = this.registerUser

      if (!username || !phone || !password || !confirm_password) {
        toast.warning('همه فیلدها الزامی هستند')
        return false
      }

      if (password !== confirm_password) {
        toast.warning('رمز عبور و تکرار آن مطابقت ندارند')
        return false
      }

      try {
        const response = await registerService.register({
          username,
          phone,
          password,
          confirm_password,
        })

        if (response.status === 200) {
          toast.success('ثبت‌نام انجام شد. لطفاً کد تأیید را وارد کنید')
          this.step = 'otp'
          return true
        } else {
          toast.error(response.data.message || 'ثبت‌نام با خطا مواجه شد')
          return false
        }
      } catch (error) {
        let errMsg = 'خطا در ثبت‌نام'

        if (error.response?.data?.errors) {
          const errs = error.response.data.errors
          if (typeof errs === 'object') {
            errMsg = Object.values(errs).flat().join('، ')
          } else if (typeof errs === 'string') {
            errMsg = errs
          }
        } else if (error.response?.data?.message) {
          errMsg = error.response.data.message
        }

        toast.error(errMsg)
        return false
      }
    },

    async verifyAndActivate() {
      try {
        const response = await otpService.verifyOtp({
          phone: this.registerUser.phone,
          code: this.otpCode,
        })

        if (response.status === 200) {
          toast.success('حساب با موفقیت فعال شد')
          this.resetRegisterData()
          return true
        } else {
          toast.error(response.data.message || 'کد تأیید اشتباه است')
          return false
        }
      } catch (error) {
        let errMsg = 'خطا در تأیید کد'

        if (error.response?.data?.errors) {
          const errs = error.response.data.errors
          errMsg = typeof errs === 'object' ? Object.values(errs).flat().join('، ') : errs
        } else if (error.response?.data?.message) {
          errMsg = error.response.data.message
        }

        toast.error(errMsg)
        return false
      }
    },
  },
})
