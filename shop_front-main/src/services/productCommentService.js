import api from "./AxiosService";

export const productCommentService = {
    getApproved(productId){
        return api.get(`/products/${productId}/comments/approved`)
    },
    
    create(payload){
        return api.post(`/products/comments`,payload)
    }
}