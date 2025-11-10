import { defineStore } from 'pinia'
import { footerService } from '@/services/FooterService'
import axios from 'axios'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

export const useFooterStore = defineStore('footer', {
  state: () => ({
    contact: {
      phone: '',
      email: '',
      address: '',
    },
    links: [],
    services: [],
    badges: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchFooter() {
      this.loading = true
      try {
        const response = await footerService.getFooter()
        const data = response.data

        this.contact = data.contact || { phone: '', email: '', address: '' }
        this.links = data.links || []
        this.services = data.services || []
        this.badges = data.badges || []

        this.error = null
      } catch (err) {
        this.error = err
        toast.error(`خطا در دریافت فوتر: ${err?.message || 'خطایی رخ داده است'}`)
      } finally {
        this.loading = false
      }
    },


    async saveFooter() {
      try {
        const payload = {
          contact: this.contact,
          links: this.links,
          services: this.services,
          badges: this.badges,
        }

        await footerService.updateFooter(payload)
        return true
      } catch (err) {
        toast.error(`خطا در ذخیره‌سازی: ${err?.message || 'خطایی هنگام ذخیره اطلاعات رخ داد'}`)
        return false
      }
    },

    async uploadBadgeFile(file, index) {
      if (!file) return
      try {
        const formData = new FormData()
        formData.append('file', file)

        const response = await footerService.updateFooter()

        const imageUrl = response.data.url
        this.badges[index] = { image: imageUrl }
        toast.success('تصویر با موفقیت آپلود شد.')
        return imageUrl
      } catch (error) {
        toast.error('آپلود تصویر با خطا مواجه شد.')
        throw error
      }
    },


    addFooterItem(section, item = {}) {
      if (Array.isArray(this[section])) {
        const id = Date.now()
        this[section].push({ ...item, id })
      }
    },

    removeFooterItem(section, id) {
      if (Array.isArray(this[section])) {
        this[section] = this[section].filter(item => item.id !== id)
      }
    },

    updateFooterItem(section, id, updatedItem) {
      if (Array.isArray(this[section])) {
        const index = this[section].findIndex(item => item.id === id)
        if (index !== -1) {
          this[section][index] = { ...this[section][index], ...updatedItem }
        }
      }
    },

    addBadge(data) {
      this.badges.push(data)
    },

    removeBadge(index) {
      this.badges.splice(index, 1)
    },
  },
})
