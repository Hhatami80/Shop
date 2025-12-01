import catBannerService from '@/services/catBannerService'
import { defineStore } from 'pinia'

export const useCategoryBannerStore = defineStore('categoryBanner', {
  state: () => ({
    banners: [], // holds the banners for the current category
    loading: false,
  }),

  actions: {
    async fetchBanners(categoryId) {
      this.loading = true
      try {
        const res = await catBannerService.getBanners(categoryId)
        this.banners = res.data
      } finally {
        this.loading = false
      }
    },

    async updateBanner(categoryId, bannerId, formData) {
      this.loading = true
      try {
        const res = await catBannerService.updateBanner(categoryId, bannerId, formData)

        // Update local state in memory
        const index = this.banners.findIndex((b) => b.id === bannerId)
        if (index !== -1) {
          this.banners[index] = res.data // DRF returns updated object
        }

        return res.data
      } finally {
        this.loading = false
      }
    },

    async deleteBanner(categoryId, bannerId) {
      this.loading = true
      try {
        await catBannerService.deleteBanner(categoryId, bannerId)

        // Remove banner from local state
        this.banners = this.banners.filter((b) => b.id !== bannerId)
      } finally {
        this.loading = false
      }
    },

    async addBanner(categoryId, formData) {
      const res = await catBannerService.addBanner(categoryId, formData)
      this.banners.push(res.data)
    },
  },
})
