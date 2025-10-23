import { defineStore } from 'pinia'
import { aboutService } from '@/services/aboutService'

export const useAboutUsStore = defineStore('about', {
  state: () => ({
    title: '',
    text: '',
    imageurl: '',
    loading: false,
    error: null,
  }),

  actions: {
    async fetchAbout() {
      this.loading = true
      this.error = null
      try {
        const { data } = await aboutService.fetchAboutData()
        this.title = data.data.title
        this.text = data.data.text
        this.imageurl = data.data.imageurl
      } catch (err) {
        this.error = 'خطا در بارگذاری اطلاعات'
        console.error(err)
      } finally {
        this.loading = false
      }
    },

    async saveAbout({ title, text, imageFile }) {
      try {
        const formData = new FormData()
        formData.append('title', title)
        formData.append('text', text)
        if (imageFile) {
          formData.append('imageurl', imageFile) 
        }
        

        await aboutService.updateAboutData(formData)
        await this.fetchAbout()
      } catch (err) {
        console.error(err)
        throw err
      }
    },
  },
})
