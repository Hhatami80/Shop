import { defineStore } from 'pinia'
import { ChangePassService } from '@/services/ChangePassService'
import VueCookies from 'vue-cookies'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

export const ChangePassStore = defineStore('ChangePass', {
  state: () => ({
    loading: null,

    changePasswordUser: {
      current_password: '',
      confirm_password: '',
      password: '',
    },
  }),

  actions: {
    async changePassword() {
      try {
        if(!this.changePasswordUser.current_password && !this.changePasswordUser.confirm_password && !this.changePasswordUser.password ){
          toast.warning('فیلد ها خالی هستند')
        }
        else{
          this.loading = true
        console.log('changePassword called')
        const formData = new FormData()
        formData.append('current_password', this.changePasswordUser.current_password)
        formData.append('confirm_password', this.changePasswordUser.confirm_password)
        formData.append('password', this.changePasswordUser.password)
        if (this.changePasswordUser.password !== this.changePasswordUser.confirm_password) {
          toast.error('پسورد با تکرار ان یکسان نیست')
          return
        }
        const response = await ChangePassService.changePassword(formData)
        
        if (response.status == 200) {
          toast.success(' رمز با موفقیت عوض شد')
          this.changePasswordUser = {
            current_password: '',
            confirm_password: '',
            password: '',
          }
        }
        }
        
      } catch (error) {
        if (error.response.status === 422) {
          const errMsg = error.response.data.errors
          if (!this.changePasswordUser.current_password) {
            toast.warning(errMsg.current_password)
          }

          if (!this.changePasswordUser.confirm_password) {
            toast.warning(errMsg.confirm_password)
          } else {
            toast.warning(errMsg)
          }
        }
        console.log(error)
      } finally {
        this.loading = false
      }
    },
    resetPasswordData() {
      this.changePasswordUser = {
        current_password: null,
        confirm_password: null,
        password: null,
      }
    },
  },
})
