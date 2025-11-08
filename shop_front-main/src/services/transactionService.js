import api from "./AxiosService";

export const transactionService = {
  async getAll(params = {}) {
    return api.get("/transactions/", { params });
  },

  async getById(id) {
    return api.get(`/transactions/${id}/`);
  },

  async delete(id) {
    return api.delete(`/transactions/${id}/`);
  },
};
