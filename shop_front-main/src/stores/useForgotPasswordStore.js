import { defineStore } from 'pinia'
import { ForgotPasswordService } from '@/services/ForgotPassword'

export const useForgotPasswordStore = defineStore('forgotPassword', {
  state: () => ({
    step: 'request',
    payload: '',
    code: '',
  }),

  actions: {
    async requestReset(payload) {
      try {
        const response = await ForgotPasswordService.requestPasswordReset(payload)
        this.payload = payload
        this.step = 'verify'
        return true
      } catch (error) {
        console.error('error requesting reset:', error)
        return false
      }
    },
    async verifyCode(code) {
      try {
        await ForgotPasswordService.verifyResetCode(this.payload, code)
        this.code = code
        this.step = 'reset'
        return true
      } catch (error) {
        console.log('error verifying code:', error)
        return false
      }
    },
    async ResetPassword(newPassword) {
      try {
        await ForgotPasswordService.resetPassword(this.payload, this.code, newPassword)
        this.$reset()
        return true
      } catch (error) {
        console.error('Error resetting password:', error)
        return false
      }
    },
  },
})
