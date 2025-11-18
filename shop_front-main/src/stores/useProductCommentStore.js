import { defineStore } from 'pinia'
import { userCommentService } from "@/services/userCommentService"

export const useProductCommentStore = defineStore('productComments', {
  state: () => ({
    comments: [],
    loading: false,
    error: null,
  }),
  actions: {
    // async fetchApprovedComments(productId) {
    //   this.loading = true
    //   try {
    //     const res = await productCommentService.getApproved(productId)
    //     this.comments = res.data.comment
    //   } catch (err) {
    //     this.error = err
    //   } finally {
    //     this.loading = false
    //   }
    // },
    async submitComment(productId, text, parent_id) {
      try {
        await userCommentService.addProductComment(
          productId,
          parent_id,
          text)
      } catch (err) {
        console.error(err)
      }
    }
  }
})
