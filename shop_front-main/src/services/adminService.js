import api from "@/services/AxiosService"


export const adminService = {
    getAdminPageProducts() {
        return api.get("/admin/products")
    },
    removeProduct(productId) {
        return api.delete(`/product-delete/${productId}`)
    },
}