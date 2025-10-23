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

    page: 1,
    totalPages: 1,
    search: '',
    status: 'all',
    perPage: 5,
  }),

  actions: {
    async fetchAllComments() {
     
      try {
        const res = await adminCommentService.getAll({
          page: this.page,
          search: this.search,
          status: this.status,
          per_page: this.perPage,
        })

        this.comments = res.data.comments

      
        if (res.data.total) {
          this.totalPages = Math.ceil(res.data.total / this.perPage)
        } else if (res.data.total_pages) {
          
          this.totalPages = res.data.total_pages
        } else {
          this.totalPages = 1
        }
      } catch (err) {
        console.error('خطا در دریافت نظرات:', err)
        this.error = 'خطا در دریافت نظرات'
      } finally {
        this.loading = false
      }
    },
    async approveComment(id) {
      await adminCommentService.approve(id)
      await this.fetchAllComments()
    },

    async deleteComment(id) {
      await adminCommentService.remove(id)
      await this.fetchAllComments()
    },

    async approveSelected() {
      if (this.selectedComments.length === 0) return
      await adminCommentService.approveBulk(this.selectedComments)
      this.selectedComments = []
      await this.fetchAllComments()
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
