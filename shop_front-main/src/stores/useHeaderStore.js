import { defineStore } from 'pinia'
import { headerService } from '@/services/HeaderService'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

export const useHeaderStore = defineStore('header', {
  state: () => ({
    logoUrl: '',
    menuItems: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchHeader() {
      this.loading = true
      try {
        const response = await headerService.getHeader()
        const data = response.data

        this.logoUrl = data.site_logo || ''
        this.menuItems = (data.header || []).map((item, index) => ({
          id: item.id ?? crypto.randomUUID(),
          title: item.title || '',
          url: item.url || '',
        }))

        this.error = null
      } catch (err) {
        this.error = err
        toast.error(`خطا در دریافت هدر: ${err?.message || 'مشکلی در دریافت اطلاعات وجود دارد'}`)
      } finally {
        this.loading = false
      }
    },

    async saveHeader() {
      try {
        await headerService.updateHeader({
          logoUrl: this.logoUrl,
           header: this.menuItems.map((item, index) => ({
        ...item,
        order: index + 1, 
      })),
        })
        toast.success('هدر با موفقیت ذخیره شد')
        return true
      } catch (err) {
        toast.error(`ذخیره‌سازی هدر ناموفق بود: ${err.message}`)
        return false
      }
    },

    addMenuItem() {
      this.menuItems.push({
        id: Date.now(),
        title: '',
        url: '',
      })
    },

    removeMenuItem(index) {
      this.menuItems.splice(index, 1)
    },

    setLogoUrl(url) {
      this.logoUrl = url
    },

    async uploadLogo(file) {
      try {
        const response = await headerService.uploadLogo(file)
        const data = response.data.data

        if (data.site_logo) {
          this.setLogoUrl(data.site_logo)
          toast.success('لوگو با موفقیت آپلود شد')
        } else {
          toast.error('آپلود لوگو موفق نبود')
        }
      } catch (error) {
        toast.error(`خطا در آپلود لوگو: ${error.message}`)
      }
    },
    async fetchlogo() {
      this.loading = true
      try {
        const response = await headerService.getlogo()
        const data = response.data.data
        this.site_logo = data.site_logo
        this.error = null
      } catch (err) {
      } finally {
        this.loading = false
      }
    },
  },
})
