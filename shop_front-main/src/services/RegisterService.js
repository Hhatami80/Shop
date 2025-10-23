import api from './AxiosService'

export const registerService = {
  register(data) {
    return api.post('sign-up', data)
  },
}
