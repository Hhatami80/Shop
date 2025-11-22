import { defineStore } from 'pinia'
import { adminCommentService } from '@/services/adminCommentService'
import toast from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

export const useAdminCommentStore = defineStore('adminComments', {
  state: () => ({
    comments: [],
    loading: false,
    error: null,
    selectedComments: [],
    unapproved_count: 0,

    page: 1,
    totalPages: 10,
    q: '',
    status: 'all',
    per_page: 5,
  }),

  actions: {
    async fetchAllComments({
      status = this.status,
      q = this.q,
      page = this.page,
      per_page = this.per_page,
    } = {}) {
      try {
        const res = await adminCommentService.getAll({
          status: status === 'all' ? '' : status,
          per_page,
          page,
          q,
        })

        this.comments = res.data.results.results
        this.unapproved_count = res.data.unapproved_count
      } catch (err) {
        console.error('خطا در دریافت نظرات:', err)
        this.error = 'خطا در دریافت نظرات'
      } finally {
        this.loading = false
      }
    },
    async approveComment(id) {
      await adminCommentService.approve(id)
      await this.fetchAllComments({ status: 'unapproved' })
    },

    async deleteComment(id) {
      await adminCommentService.remove(id)
      await this.fetchAllComments()
    },

    async approveSelected() {
      if (this.selectedComments.length === 0) return
      await adminCommentService.approveBulk(this.selectedComments)
      this.selectedComments = []
      await this.fetchAllComments({ status: 'unapproved' })
    },

    async deleteSelectedComments() {
      if (this.selectedComments.length === 0) return

      for (const id of this.selectedComments) {
        await adminCommentService.remove(id)
      }

      this.selectedComments = []
      await this.fetchAllComments()
    },
  },
})
