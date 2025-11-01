import { defineStore } from 'pinia'
import { loginService } from '@/services/LoginService'
import { toast } from 'vue3-toastify'
import VueCookies from 'vue-cookies'

export const useLoginStore = defineStore('login', {
  state: () => ({
    loginUser: { username: '', password: '' },
    user: null,
    token: null
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.user?.role === 'admin',
  },
  actions: {
    async login() {
      if (!this.loginUser.username || !this.loginUser.password) {
        toast.warning('فیلدها نباید خالی باشند')
        return false
      }

      try {
        const formData = new FormData()
        formData.append('username', this.loginUser.username)
        formData.append('password', this.loginUser.password)

        const response = await loginService.login(formData)
        if (response.status === 200) {
          this.token = response.data.token
          this.user = response.data.user
          VueCookies.set('token', this.token, '1d')
          VueCookies.set('user', this.user, '1d')
          return true
        }
      } catch (error) {
        if (error.response?.status === 422) {
          const errs = error.response.data.errors
          if (errs.username) toast.warning(errs.username)
          if (errs.password) toast.warning(errs.password)
          return false
        }
        toast.error('خطای ناشناخته رخ داد')
        return false
      }
    },

    logout() {
      VueCookies.remove('token')
      VueCookies.remove('user')
      this.token = null
      this.user = null
    },

    loadFromCookies() {
      this.token = VueCookies.get('token')
      const userCookie = VueCookies.get('user')
      try {
        if (typeof userCookie === 'string') {
          this.user = JSON.parse(userCookie)
        } else {
          this.user = userCookie
        }
      } catch {
        this.user = userCookie
      }
    }
  }
})
