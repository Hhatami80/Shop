import api from './AxiosService'

export const otpService = {
  verifyOtp(data) {
    return api.post('/verify-otp', data)
  },
}
