import api from './AxiosService'

export const ChangePassService = {
  async changePassword(payload) {
    return await api.put('/change-password', payload)
  },
}
