import { defineStore } from 'pinia'
import { adminCommentService } from '@/services/adminCommentService'

export const useProductCommentStore = defineStore('productComments', {
  state: () => ({
    comments: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchApprovedComments(productId) {
      this.loading = true
      try {
        const res = await productCommentService.getApproved(productId)
        this.comments = res.data.comment
      } catch (err) {
        this.error = err
      } finally {
        this.loading = false
      }
    },
    async submitComment(productId, text, rating) {
      try {
        await productCommentService.create({
          product_id: productId,
          text,
          rating
        })
      } catch (err) {
        console.error(err)
      }
    }
  }
})
