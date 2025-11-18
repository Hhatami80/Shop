import api from "./AxiosService"

export const userCommentService = {
    addProductComment(product_id, parent_id, text, user) {
        return api.post(`/products/${product_id}/comments`, {
            parent_id: parent_id,
            text: text,
        })
    }
}