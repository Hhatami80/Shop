import { defineStore } from 'pinia'
import { fetchFeatureSection, updateFeatureSection } from '@/services/FeatureSectionService'

export const useFeatureSectionStore = defineStore('FeatureSectionStore', {
  state: () => ({
    featureSection: null,
    loading: false,
    error: null,
    success: false
  }),

  actions: {
    async getFeatureSection() {
      this.loading = true
      this.error = null
      this.success = false
      try {
        const response = await fetchFeatureSection()
        this.featureSection = response.data
      } catch (err) {
        this.error = err.response?.data || err.message
      } finally {
        this.loading = false
      }
    },

    async updateMainBanner(formData) {
      this.loading = true
      this.error = null
      this.success = false
      try {
        await updateFeatureSection(formData, true)
        this.success = true
        await this.getFeatureSection()
      } catch (err) {
        this.error = err.response?.data || err.message
      } finally {
        this.loading = false
      }
    }
  }
})
