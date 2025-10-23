import api from './AxiosService'

export const ForgotPasswordService = {
    async requestPasswordReset(payload){
        return api.post('/request-reset' , {payload})
    },

    async verifyResetCode(payload , code){
        return api.post('/verify-reset' , {payload , code})
    },

    async resetPassword(payload , code , newPassword){
        return api.post('/reset-password' , {payload , code , password:newPassword,})
    },
}