import api from "@/services/AxiosService"


export const adminService = {
    getAdminPageProducts() {
        return api.get("/admin/products")
    } 
}